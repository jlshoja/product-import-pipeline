from pathlib import Path

# ============================================================
# Repository Root
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

# ============================================================
# Core Directories
# ============================================================

DATA_DIR = ROOT_DIR / "data"

REPORTS_DIR = ROOT_DIR / "reports" / "outputs"

TEMPLATES_DIR = ROOT_DIR / "reports" / "templates"

LOGS_DIR = ROOT_DIR / "logs"

# ============================================================
# Ensure Directories Exist
# ============================================================

for directory in (
    DATA_DIR,
    REPORTS_DIR,
    TEMPLATES_DIR,
    LOGS_DIR,
):
    directory.mkdir(parents=True, exist_ok=True)
