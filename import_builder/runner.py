#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Import Builder - Automated Runner
Runs WooCommerce CSV generation without web interface.
"""

import os
import sys
import re
from pathlib import Path
from datetime import datetime

_this_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(_this_dir))

from paths import ROOT_DIR, IMPORT_BUILDER_UPLOADS_DIR

_DATE_FOLDER_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}$')


def _get_latest_dated_folder(base_path):
    """Find the latest date-stamped subfolder (format: 2026-07-12_13-29-57)."""
    if not base_path.exists():
        return base_path
    dated = [
        f.name for f in base_path.iterdir()
        if f.is_dir() and _DATE_FOLDER_PATTERN.match(f.name)
    ]
    if not dated:
        return base_path
    return base_path / sorted(dated)[-1]


def main():
    input_file = ROOT_DIR / "data" / "outputs" / "product.csv"
    source_images_base = ROOT_DIR / "data" / "outputs" / "processed_images"
    source_images = _get_latest_dated_folder(source_images_base)
    dest_images = ROOT_DIR / "data" / "outputs" / "renamed_images" / datetime.now().strftime('%Y-%m-%d_%H-%M-%S')

    if not input_file.exists():
        print(f"ERROR: Input file not found: {input_file}")
        return False

    if not source_images.exists() or not any(source_images.iterdir()):
        print(f"ERROR: No processed images found in: {source_images}")
        return False

    print(f"Source images: {source_images}")

    # Change to import_builder directory so relative paths (sku_list.txt etc.) resolve correctly
    original_cwd = os.getcwd()
    os.chdir(str(_this_dir))

    try:
        from woocommerce_generator_v12 import process_products_v12

        dest_images.mkdir(parents=True, exist_ok=True)

        df_output, mappings = process_products_v12(
            input_file=str(input_file),
            process_images=True,
            source_images_folder=str(source_images),
            dest_images_folder=str(dest_images),
        )

        if df_output is None:
            print("ERROR: Import builder processing failed.")
            return False

        # Save a convenience copy to data/outputs/
        output_copy = ROOT_DIR / "data" / "outputs" / "woocommerce_import.csv"
        df_output.to_csv(str(output_copy), index=False, encoding='utf-8-sig')
        print(f"\nCopy saved: {output_copy}")

        return True

    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        os.chdir(original_cwd)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
