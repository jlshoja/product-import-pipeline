"""
Central file registry.

Phase A:
Read-only registry.
No consumers migrated yet.
"""

FILES = {
    "archive_urls": "archive_urls.xlsx",
    "extracted_products": "extracted_products.xlsx",
    "product_details": "product_details_complete.xlsx",
    "tracking": "product_tracking_LATEST.xlsx",
    "checkpoint": "checkpoint.xlsx",
    "price_history": "price_history.xlsx",
    "color_mapping": "color_mapping.xlsx",
    "product_names": "product_names.xlsx",
    "standard_categories": "standard_categories.xlsx",
    "standard_colors": "standar_colors.xlsx",
    "pricing_sample": "pricing_sample.xlsx",
    "word_index": "word index.xlsx",
}


def get_file(name):
    """
    Return registered filename by key.
    """
    return FILES[name]


def has_file(name):
    """
    Check whether a file key exists.
    """
    return name in FILES


def get_all_files():
    """
    Return a copy of the registry.
    """
    return FILES.copy()
