"""
Central configuration registry.

Phase B:
Read-only adapters.
"""

CONFIG_REGISTRY = {
    "application": {
        "module": "product_extraction.config.settings",
        "loader": "get_config",
    },
    "history": {
        "module": "product_extraction.config.history_config",
        "settings": "HISTORY_SETTINGS",
        "columns": "HISTORY_COLUMNS",
    },
}
