# -*- coding: utf-8 -*-
"""
Price History Manager
Manages product price change history
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import HISTORY_SETTINGS, HISTORY_COLUMNS


class PriceHistoryManager:
    """Manages price change history"""
    
    def __init__(self, reports_dir):
        self.reports_dir = Path(reports_dir)
        self.history_file = self.reports_dir / HISTORY_SETTINGS['history_filename']
        self.archive_dir = self.reports_dir / HISTORY_SETTINGS['archive_folder']
        
        # Create archive folder
        if HISTORY_SETTINGS['archive_old_data']:
            self.archive_dir.mkdir(exist_ok=True)
    
    def load_history(self):
        """Load existing history"""
        if self.history_file.exists():
            try:
                df = pd.read_excel(self.history_file)
                print(f"[OK] Loaded {len(df)} history records")
                sys.stdout.flush()
                return df
            except Exception as e:
                print(f"[WARNING] Could not load history: {e}")
                sys.stdout.flush()
                return pd.DataFrame(columns=HISTORY_COLUMNS)
        return pd.DataFrame(columns=HISTORY_COLUMNS)
    
    def add_price_change(self, sku, product_name, old_price, new_price, 
                        change_type, persian_date):
        """
        Add a price change to the history

        change_type: 'increase', 'decrease', 'new', 'removed'
        """
        if not HISTORY_SETTINGS['enable_history']:
            return
        
        # Calculate the change
        if old_price and new_price:
            change_amount = new_price - old_price
            change_percent = (change_amount / old_price) * 100 if old_price > 0 else 0
        else:
            change_amount = new_price if new_price else 0
            change_percent = 0
        
        # Build the new record
        new_record = {
            'sku': sku,
            'product_name': product_name,
            'change_date': datetime.now().strftime('%Y-%m-%d'),
            'persian_date': persian_date,
            'old_price': old_price if old_price else 0,
            'new_price': new_price if new_price else 0,
            'change_amount': change_amount,
            'change_percent': f"{change_percent:+.2f}%",
            'change_type': change_type,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return new_record
    
    def save_history(self, new_records):
        """Save history with a record-count limit"""
        if not HISTORY_SETTINGS['enable_history'] or not new_records:
            return
        
        # Load existing history
        history_df = self.load_history()
        
        # Add the new records
        new_df = pd.DataFrame(new_records)
        history_df = pd.concat([history_df, new_df], ignore_index=True)
        
        # Limit the number of records per product
        max_records = HISTORY_SETTINGS['max_records_per_product']
        
        if 'sku' in history_df.columns:
            # Keep the latest N records per SKU
            history_df = history_df.sort_values('timestamp', ascending=False)
            history_df = history_df.groupby('sku').head(max_records)
            history_df = history_df.sort_values(['sku', 'timestamp'], ascending=[True, False])
        
        # Save
        try:
            history_df.to_excel(self.history_file, index=False, engine='openpyxl')
            print(f"\n[OK] History saved: {len(history_df)} total records")
            print(f"    -> {len(new_records)} new records added")
            print(f"    -> Max {max_records} records per product")
            sys.stdout.flush()
        except Exception as e:
            print(f"[ERROR] Could not save history: {e}")
            sys.stdout.flush()
    
    def create_daily_snapshot(self, current_df):
        """Create a daily snapshot"""
        if not HISTORY_SETTINGS['keep_daily_snapshots']:
            return
        
        today = datetime.now().strftime('%Y-%m-%d')
        snapshot_file = self.archive_dir / f'snapshot_{today}.xlsx'
        
        if not snapshot_file.exists():
            try:
                current_df.to_excel(snapshot_file, index=False, engine='openpyxl')
                print(f"[OK] Daily snapshot created: {snapshot_file.name}")
                sys.stdout.flush()
            except Exception as e:
                print(f"[WARNING] Could not create snapshot: {e}")
                sys.stdout.flush()
        
        # Delete old snapshots
        self.cleanup_old_snapshots()
    
    def cleanup_old_snapshots(self):
        """Delete snapshots older than N days"""
        if not self.archive_dir.exists():
            return
        
        max_days = HISTORY_SETTINGS['keep_daily_snapshots']
        cutoff_date = datetime.now().timestamp() - (max_days * 24 * 60 * 60)
        
        deleted_count = 0
        for file in self.archive_dir.glob('snapshot_*.xlsx'):
            if file.stat().st_mtime < cutoff_date:
                try:
                    file.unlink()
                    deleted_count += 1
                except Exception as e:
                    print(f"[WARNING] Could not delete old snapshot: {e}")
                    sys.stdout.flush()
        
        if deleted_count > 0:
            print(f"[OK] Cleaned up {deleted_count} old snapshots")
            sys.stdout.flush()
    
    def get_product_history(self, sku):
        """Get the history of a specific product"""
        history_df = self.load_history()
        if 'sku' in history_df.columns:
            product_history = history_df[history_df['sku'] == sku].sort_values('timestamp', ascending=False)
            return product_history
        return pd.DataFrame()
    
    def get_statistics(self):
        """History statistics"""
        history_df = self.load_history()
        
        if history_df.empty:
            return {
                'total_records': 0,
                'total_products': 0,
                'date_range': None
            }
        
        stats = {
            'total_records': len(history_df),
            'total_products': history_df['sku'].nunique() if 'sku' in history_df.columns else 0,
            'date_range': f"{history_df['change_date'].min()} to {history_df['change_date'].max()}" if 'change_date' in history_df.columns else None,
            'price_increases': len(history_df[history_df['change_type'] == 'increase']) if 'change_type' in history_df.columns else 0,
            'price_decreases': len(history_df[history_df['change_type'] == 'decrease']) if 'change_type' in history_df.columns else 0,
            'new_products': len(history_df[history_df['change_type'] == 'new']) if 'change_type' in history_df.columns else 0,
        }
        
        return stats
