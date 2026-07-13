# Plan 002: Harden the two Flask web panels

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat c8d53b2..HEAD -- import_builder/web_panel_v12.py product_extraction/web_panel_interactive.py`
> If either file changed since this plan was written, compare the "Current
> state" excerpts against the live code before proceeding; on a mismatch, treat
> it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED
- **Depends on**: none
- **Category**: security
- **Planned at**: commit `c8d53b2`, 2026-07-13

## Why this matters

Both Flask panels are developer tools, but each currently exposes the host to
remote compromise from anyone on the same network:

1. `import_builder/web_panel_v12.py` runs with `debug=True` **and**
   `host='0.0.0.0'`. Werkzeug's debugger executes arbitrary Python from
   tracebacks; bound to all interfaces it is remote code execution on the LAN.
2. Both panels stream files from **client-supplied paths** with no
   base-directory confinement — a crafted path reads any file the process can
   (including the on-disk `.env`).
3. One endpoint writes client JSON into a **Python source file** (`config_v9.py`)
   and re-imports it — a code-injection + persistence primitive.
4. The Flask `secret_key` falls back to a hardcoded constant when the env var is
   unset (the default), allowing session-cookie forgery.

These are the highest-severity findings in the audit. The fixes are small,
well-understood, and preserve the tools' intended local use.

## Current state

**File A — `import_builder/web_panel_v12.py`**

- Line 65 — hardcoded fallback secret key:
  ```python
  app.secret_key = os.environ.get('SECRET_KEY', 'woocommerce-generator-secret-key-2024')
  ```
- Line 66-69 — upload folder is a known, confined directory (use it as the jail root):
  ```python
  app.config['UPLOAD_FOLDER'] = str(IMPORT_BUILDER_UPLOADS_DIR)
  ...
  os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
  ```
- Lines 692-695 — path traversal in download:
  ```python
  @app.route('/download/<path:filename>')
  def download_file(filename):
      filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
      return send_file(filepath, as_attachment=True)
  ```
- Lines 697-742 — endpoint that rewrites `config_v9.py` from request JSON:
  ```python
  @app.route('/api/update-path', methods=['POST'])
  def update_path():
      data = request.get_json()
      ...
      new_path = data['path'].strip().rstrip('/\\')
      config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config_v9.py')
      ...
      new_content = _re.sub(
          r'^(SOURCE_IMAGES_BASE\s*=\s*)r?"[^"]*"',
          lambda m: f'SOURCE_IMAGES_BASE = r"{new_path}"',
          content, flags=_re.MULTILINE)
      with open(config_path, 'w', encoding='utf-8') as f:
          f.write(new_content)
      import importlib
      import config_v9
      config_v9.SOURCE_IMAGES_BASE = new_path
      ...
  ```
- Line 796 — debug + all-interfaces bind:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5000)
  ```

**File B — `product_extraction/web_panel_interactive.py`**

- Lines 377-388 — arbitrary file download (raw client path):
  ```python
  @app.route('/api/download/<path:filepath>')
  def download_file(filepath):
      file_path = Path(filepath)
      if not file_path.exists():
          return jsonify({'error': 'File not found'}), 404
      return send_file(str(file_path.absolute()), as_attachment=True)
  ```
- Lines 391-407 — same pattern for `/api/view/<path:filepath>` (renders `.html`
  inline via `mimetype='text/html'`).
- Line 426 — **already** `debug=False`, but binds all interfaces:
  ```python
  app.run(host='0.0.0.0', port=5000, debug=False)
  ```

**Convention**: `werkzeug` is already a dependency (`Werkzeug>=2.0.0` in
`import_builder/requirements.txt`). Use `werkzeug.utils.safe_join` for path
confinement — it is the standard, correct tool and returns `None` on escape.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Compile check A | `python -m py_compile import_builder/web_panel_v12.py` | exit 0, no output |
| Compile check B | `python -m py_compile product_extraction/web_panel_interactive.py` | exit 0, no output |
| Grep debug flags | `grep -rn "debug=True" import_builder/ product_extraction/` | no matches |
| Grep 0.0.0.0 binds | `grep -rn "0.0.0.0" import_builder/web_panel_v12.py product_extraction/web_panel_interactive.py` | no matches |

Run from repo root.

## Scope

**In scope** (the only files you should modify):
- `import_builder/web_panel_v12.py`
- `product_extraction/web_panel_interactive.py`
- `plans/README.md` (status row only)

**Out of scope** (do NOT touch):
- `import_builder/config_v9.py` — the update-path feature must stop writing to
  it, but do not change the config file itself.
- Any template/static files, other routes not listed here.
- The upload/processing business logic — only the security-relevant lines change.

## Git workflow

- Branch: `advisor/002-flask-hardening`
- One commit per file is fine; short imperative messages (see `git log`).
- Do NOT push or open a PR unless the operator instructs it.

## Steps

### Step 1: Bind both panels to loopback and disable the debugger

In `import_builder/web_panel_v12.py:796`, change to:
```python
    app.run(debug=False, host='127.0.0.1', port=5000)
```

In `product_extraction/web_panel_interactive.py:426`, change to:
```python
    app.run(host='127.0.0.1', port=5000, debug=False)
```

**Verify**: `grep -rn "0.0.0.0\|debug=True" import_builder/web_panel_v12.py product_extraction/web_panel_interactive.py` → no matches.

### Step 2: Require a real secret key (no hardcoded fallback)

In `import_builder/web_panel_v12.py:65`, replace the fallback with a
fail-fast-or-ephemeral pattern:
```python
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(32)
```
This uses a random per-process key when `SECRET_KEY` is unset (sessions won't
survive a restart, which is fine for a local tool) and never signs with a known
constant. The old committed constant `'woocommerce-generator-secret-key-2024'`
must not remain anywhere in the file.

**Verify**: `grep -n "woocommerce-generator-secret-key" import_builder/web_panel_v12.py` → no matches.

### Step 3: Confine both download endpoints to their intended directory

In `import_builder/web_panel_v12.py:692-695`, use `safe_join` against the
upload folder:
```python
from werkzeug.utils import safe_join  # add near the top imports if not present

@app.route('/download/<path:filename>')
def download_file(filename):
    filepath = safe_join(app.config['UPLOAD_FOLDER'], filename)
    if filepath is None or not os.path.isfile(filepath):
        return jsonify({'error': 'File not found'}), 404
    return send_file(filepath, as_attachment=True)
```

In `product_extraction/web_panel_interactive.py`, both `/api/download` (377) and
`/api/view` (391) currently accept an unconfined absolute path. Confine them to
the reports/output directory the panel legitimately serves. First determine that
directory: search the file for where it lists/serves reports (grep the file for
`reports`, `outputs`, `send_file`, and any existing base-path constant like
`ROOT_DIR`, `REPORTS_DIR`, `OUTPUTS_DIR`). Define a single `SERVE_ROOT` base
(reuse an existing constant if one already points at the reports/output tree)
and rewrite both endpoints:
```python
from werkzeug.utils import safe_join

@app.route('/api/download/<path:filepath>')
def download_file(filepath):
    full = safe_join(str(SERVE_ROOT), filepath)
    if full is None or not Path(full).is_file():
        return jsonify({'error': 'File not found'}), 404
    return send_file(full, as_attachment=True)

@app.route('/api/view/<path:filepath>')
def view_file(filepath):
    full = safe_join(str(SERVE_ROOT), filepath)
    if full is None or not Path(full).is_file():
        return jsonify({'error': 'File not found'}), 404
    if Path(full).suffix.lower() == '.html':
        return send_file(full, mimetype='text/html')
    return send_file(full, as_attachment=True)
```
If the front-end passes absolute paths today, they will now be interpreted
relative to `SERVE_ROOT`. If you cannot identify a single correct `SERVE_ROOT`
from the code, that is a STOP condition — report what the endpoints are used for
rather than guessing.

**Verify**: `python -m py_compile product_extraction/web_panel_interactive.py import_builder/web_panel_v12.py` → exit 0.

### Step 4: Stop writing request data into a Python source file

The `/api/update-path` endpoint (`import_builder/web_panel_v12.py:697-742`) must
no longer write into `config_v9.py`. Replace the file-rewrite with a JSON
sidecar the config reads at runtime. Two parts:

**4a.** Rewrite the endpoint to validate the path and persist it to
`import_builder/runtime_path_override.json` (a data file, never executed):
```python
@app.route('/api/update-path', methods=['POST'])
def update_path():
    data = request.get_json()
    if not data or 'path' not in data:
        return jsonify({'error': 'No path provided'}), 400
    new_path = str(data['path']).strip().rstrip('/\\')
    # Validate: must be an existing directory, no newlines/control chars
    if not new_path or '\n' in new_path or '\r' in new_path or not os.path.isdir(new_path):
        return jsonify({'error': 'Path must be an existing directory'}), 400
    override_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'runtime_path_override.json')
    with open(override_file, 'w', encoding='utf-8') as f:
        json.dump({'SOURCE_IMAGES_BASE': new_path}, f)
    # Update in-memory globals for the running process
    global SOURCE_IMAGES_FOLDER, SOURCE_IMAGES_BASE
    SOURCE_IMAGES_BASE = new_path
    # ... keep whatever downstream refresh (get_latest_images_folder) the old code did,
    #     but sourced from new_path — do NOT re-import or rewrite config_v9.py
    ...
    return jsonify({'success': True, 'path': new_path})
```
Ensure `import json` is present at the top of the file. Preserve the endpoint's
existing success-response fields (folder existence, image count) by computing
them from `new_path` the same way the old code did — just without the file
rewrite and `importlib` re-import.

**4b.** So the override actually takes effect on the next run, make
`config_v9.py`'s `SOURCE_IMAGES_BASE` read the sidecar **if present**. Since
`config_v9.py` is out of scope for editing in this plan, DO NOT edit it here —
instead, in the web panel, load the override at startup where the module-level
`SOURCE_IMAGES_BASE` global is first established, so the running panel honors it.
If making the override authoritative requires editing `config_v9.py`, STOP and
report — that is a scope boundary to confirm with the operator, not to cross
silently.

**Verify**: `grep -n "config_v9.py'" import_builder/web_panel_v12.py` shows no
`open(...config_v9.py..., 'w')` write remains; `grep -n "_re.sub" import_builder/web_panel_v12.py`
→ no match (the source-rewrite regex is gone).

### Step 5: Update the status row

In `plans/README.md`, change plan 002's status to `DONE`.

**Verify**: `grep "002" plans/README.md` shows `DONE`.

## Test plan

There is no test harness for the Flask panels, and they require a browser +
live data to exercise. Verification is therefore static + manual:

- **Static**: all `grep` checks in the steps return the expected empty/զpresent
  results; `py_compile` passes for both files.
- **Manual smoke (operator, optional)**: start `import_builder` panel, confirm
  it now prints `http://127.0.0.1:5000`, that a normal download still works, and
  that `GET /download/..%2f..%2f.env` returns 404 rather than a file.
- Do NOT add new test dependencies for this plan; if plan 001's `tests/` exists,
  no baseline test covers these endpoints.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python -m py_compile import_builder/web_panel_v12.py product_extraction/web_panel_interactive.py` exits 0
- [ ] `grep -rn "debug=True" import_builder/ product_extraction/` returns no matches
- [ ] `grep -rn "0.0.0.0" import_builder/web_panel_v12.py product_extraction/web_panel_interactive.py` returns no matches
- [ ] `grep -n "woocommerce-generator-secret-key" import_builder/web_panel_v12.py` returns no matches
- [ ] `grep -n "_re.sub" import_builder/web_panel_v12.py` returns no matches (config-rewrite removed)
- [ ] `safe_join` appears in both files
- [ ] No files outside the in-scope list are modified (`git status`)
- [ ] `plans/README.md` status row for 002 shows DONE

## STOP conditions

Stop and report back (do not improvise) if:

- The live code at any cited line does not match the "Current state" excerpts
  (the file drifted since this plan was written).
- You cannot identify a single correct `SERVE_ROOT` base directory for the
  `web_panel_interactive.py` endpoints from the surrounding code.
- Making the `/api/update-path` override authoritative on the next pipeline run
  genuinely requires editing `config_v9.py` (out of scope) — report the coupling.
- Removing `debug=True` reveals the panel relied on the reloader/debugger to
  function (it should not, but if startup breaks, report the traceback).

## Maintenance notes

- The `/api/update-path` feature now persists to `runtime_path_override.json`.
  A reviewer should confirm no code path still trusts a `config_v9.py` rewrite,
  and that the override file is gitignored (it is machine-specific state — add
  it to `.gitignore` if not already covered).
- If these panels are ever intentionally exposed beyond localhost, they need
  real authentication first — loopback binding is the current security boundary.
- `os.urandom(32)` secret means sessions reset on restart; if persistent
  sessions are ever needed, set `SECRET_KEY` in the environment, never in code.
