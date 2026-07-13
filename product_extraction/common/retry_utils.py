"""
Shared retry / backoff helpers for network-facing operations.

Every stage of the pipeline touches the network (Selenium page loads, HTTP
image downloads, the Gemini API). Before this module each stage hand-rolled its
own retry loop with different counts, sleeps and (in)consistent handling of
timeouts vs. permanent errors. This module centralises that policy so an
interruption caused by a timeout or connection error is retried with
exponential backoff until it succeeds — while genuinely permanent errors (a
404, a malformed page) are surfaced instead of being retried forever.

Design notes:
- Errors are classified as TRANSIENT (worth retrying) or PERMANENT (give up
  immediately and let the caller record the dead-end). Anything unknown is
  treated as transient by default so a flaky connection never silently drops a
  product — the bounded attempt count is the backstop.
- Backoff is exponential with jitter to avoid hammering a struggling server.
- No hard dependency on selenium/requests: their exception types are matched by
  name so this module imports cleanly even if a stage doesn't use them.
"""

import logging
import random
import time
import os
import socket

logger = logging.getLogger("common.retry")


# ── Error classification ────────────────────────────────────────────────────

# Substrings (matched against the exception's type name, case-insensitive) that
# indicate a transient network condition worth retrying.
TRANSIENT_ERROR_NAMES = (
    "timeout",            # requests.Timeout, selenium TimeoutException, socket.timeout
    "connection",         # ConnectionError, ConnectionResetError, requests ConnectionError
    "chunkedencoding",    # requests.exceptions.ChunkedEncodingError
    "readtimeout",
    "connecttimeout",
    "webdriverexception", # selenium: renderer disconnected, session lost, etc.
    "maxretryerror",      # urllib3
    "protocolerror",      # urllib3 / http.client
    "remotedisconnected",
    "temporarilyunavailable",
    "serviceunavailable",
    "ratelimit",
    "resourceexhausted",  # Gemini 429
    "deadlineexceeded",   # Gemini timeout
    "internalservererror",
    "unavailable",
)

# Substrings that indicate a permanent condition — retrying will never help.
PERMANENT_ERROR_NAMES = (
    "nosuchelement",       # selenium: element genuinely absent (page structure)
    "invalidargument",
    "invalidselector",
    "filenotfound",
    "notfound",            # HTTP 404 wrappers
    "permissiondenied",
    "unauthorized",
)

# HTTP status codes considered transient when carried on an exception/response.
TRANSIENT_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}

# Environment-configurable defaults
MAX_ATTEMPTS_DEFAULT = int(os.getenv('RETRY_MAX_ATTEMPTS', '4'))
BASE_DELAY_DEFAULT = float(os.getenv('RETRY_BASE_DELAY', '2.0'))
CAP_DELAY_DEFAULT = float(os.getenv('RETRY_CAP', '60.0'))
JITTER_DEFAULT = float(os.getenv('RETRY_JITTER', '0.3'))


# Optional class-based exception mapping for higher fidelity. Import libraries
# only if available; fallback to name-based matching otherwise.
TRANSIENT_EXCEPTION_CLASSES = set()
PERMANENT_EXCEPTION_CLASSES = set()
try:
    import requests
    TRANSIENT_EXCEPTION_CLASSES.add(requests.exceptions.ConnectionError)
    TRANSIENT_EXCEPTION_CLASSES.add(requests.exceptions.Timeout)
    PERMANENT_EXCEPTION_CLASSES.add(requests.exceptions.InvalidURL)
except Exception:
    pass
try:
    import urllib3
    TRANSIENT_EXCEPTION_CLASSES.add(urllib3.exceptions.ProtocolError)
    TRANSIENT_EXCEPTION_CLASSES.add(urllib3.exceptions.ReadTimeoutError)
except Exception:
    pass
try:
    from selenium.common.exceptions import WebDriverException, NoSuchElementException, InvalidSelectorException
    TRANSIENT_EXCEPTION_CLASSES.add(WebDriverException)
    PERMANENT_EXCEPTION_CLASSES.add(NoSuchElementException)
    PERMANENT_EXCEPTION_CLASSES.add(InvalidSelectorException)
except Exception:
    pass
# socket timeouts are transient
TRANSIENT_EXCEPTION_CLASSES.add(socket.timeout)


def _status_code_of(exc):
    """Best-effort extraction of an HTTP status code from an exception."""
    resp = getattr(exc, "response", None)
    if resp is not None:
        code = getattr(resp, "status_code", None)
        if isinstance(code, int):
            return code
    code = getattr(exc, "status_code", None)
    if isinstance(code, int):
        return code
    return None


def is_transient_error(exc):
    """Return True when the exception looks worth retrying.

    Classification order:
    1. An HTTP status code on the exception wins (404 -> permanent, 503 -> transient).
    2. Exception type name matched against the permanent list -> permanent.
    3. Exception type name matched against the transient list -> transient.
    4. Unknown -> transient (the attempt cap is the safety net).
    """
    # First, class-based checks (high fidelity if libraries available)
    try:
        if any(isinstance(exc, cls) for cls in PERMANENT_EXCEPTION_CLASSES):
            return False
        if any(isinstance(exc, cls) for cls in TRANSIENT_EXCEPTION_CLASSES):
            return True
    except Exception:
        # Fall back to name-based classification
        pass

    status = _status_code_of(exc)
    if status is not None:
        if status in TRANSIENT_HTTP_STATUS:
            return True
        if 400 <= status < 500:
            return False  # 4xx (except the transient ones above) won't fix itself

    name = type(exc).__name__.lower()
    if any(token in name for token in PERMANENT_ERROR_NAMES):
        return False
    if any(token in name for token in TRANSIENT_ERROR_NAMES):
        return True

    # Also scan the message for well-known transient phrases.
    msg = str(exc).lower()
    if any(token in msg for token in ("timed out", "timeout", "connection reset",
                                      "connection aborted", "connection refused",
                                      "temporarily unavailable", "try again")):
        return True

    # Default: treat as transient so a flaky network never drops an item silently.
    return True


class PermanentError(Exception):
    """Wrap an error the caller has decided is a permanent dead-end."""


# ── Backoff ─────────────────────────────────────────────────────────────────

def backoff_delay(attempt, base=2.0, cap=60.0, jitter=0.3):
    """Exponential backoff (seconds) for a 1-based attempt number, with jitter.

    attempt=1 -> ~base, attempt=2 -> ~2*base, capped at `cap`. Jitter is a
    fractional +/- spread so concurrent workers don't retry in lockstep.
    """
    raw = min(cap, base * (2 ** (attempt - 1)))
    spread = raw * jitter
    return max(0.0, raw + random.uniform(-spread, spread))


def retry_call(func, *args, max_attempts=4, base_delay=2.0, cap=60.0,
               on_retry=None, label="operation", **kwargs):
    """Call ``func(*args, **kwargs)`` retrying transient failures with backoff.

    Args:
        func: callable to invoke.
        max_attempts: total attempts before giving up (>=1).
        base_delay: base seconds for exponential backoff.
        cap: maximum backoff sleep.
        on_retry: optional callback ``(attempt, exc, delay)`` invoked before
            each sleep — handy for stage-specific recovery (e.g. restart the
            Selenium driver) or logging.
        label: human-readable name used in log messages.

    Returns:
        Whatever ``func`` returns on success.

    Raises:
        The last exception if all attempts are exhausted, or immediately if the
        error is classified as permanent.
    """
    last_exc = None
    # Use env/config defaults if caller didn't override
    if max_attempts is None:
        max_attempts = MAX_ATTEMPTS_DEFAULT
    if base_delay is None:
        base_delay = BASE_DELAY_DEFAULT
    if cap is None:
        cap = CAP_DELAY_DEFAULT
    if 'jitter' in kwargs:
        jitter = kwargs.pop('jitter')
    else:
        jitter = JITTER_DEFAULT

    for attempt in range(1, max_attempts + 1):
        try:
            return func(*args, **kwargs)
        except Exception as exc:  # noqa: BLE001 - deliberately broad; we classify below
            last_exc = exc
            transient = is_transient_error(exc)

            if not transient:
                logger.warning(
                    f"[retry] {label}: permanent error ({type(exc).__name__}: "
                    f"{str(exc)[:120]}) — not retrying"
                )
                raise

            if attempt >= max_attempts:
                logger.error(
                    f"[retry] {label}: giving up after {max_attempts} attempts "
                    f"({type(exc).__name__}: {str(exc)[:120]})"
                )
                raise

            delay = backoff_delay(attempt, base=base_delay, cap=cap, jitter=jitter)
            logger.warning(
                f"[retry] {label}: attempt {attempt}/{max_attempts} failed "
                f"({type(exc).__name__}: {str(exc)[:100]}) — retrying in {delay:.1f}s"
            )
            if on_retry is not None:
                try:
                    on_retry(attempt, exc, delay)
                except Exception as cb_exc:  # noqa: BLE001
                    logger.warning(f"[retry] {label}: on_retry callback raised: {cb_exc}")
            time.sleep(delay)

    # Unreachable, but keeps type-checkers happy.
    if last_exc:
        raise last_exc


def with_retry(max_attempts=4, base_delay=2.0, cap=60.0, label=None):
    """Decorator form of :func:`retry_call`.

    Example:
        @with_retry(max_attempts=5, label="download image")
        def download(url): ...
    """
    def decorator(func):
        fn_label = label or func.__name__

        def wrapper(*args, **kwargs):
            return retry_call(
                func, *args,
                max_attempts=max_attempts, base_delay=base_delay, cap=cap,
                label=fn_label, **kwargs
            )

        wrapper.__name__ = getattr(func, "__name__", "wrapped")
        wrapper.__doc__ = func.__doc__
        return wrapper

    return decorator
