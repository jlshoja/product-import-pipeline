# -*- coding: utf-8 -*-
"""
Price History Manager
مدیریت سوابق تغییرات قیمت محصولات
"""

import pandas as pd
from pathlib import Path
from datetime import datetime
import shutil
import sys
sys.path.append(str(Path(__file__).parent.parent))

from config.history_config import HISTORY_SETTINGS, HISTORY_COLUMNS


class PriceHistoryManager:
    """مدیریت سوابق تغییرات قیمت"""
    
    def __init__(self, reports_dir):
        self.reports_dir = Path(reports_dir)
        self.history_file = self.reports_dir / HISTORY_SETTINGS['history_filename']
        self.archive_dir = self.reports_dir / HISTORY_SETTINGS['archive_folder']
        
        # ایجاد پوشه بایگانی
        if HISTORY_SETTINGS['archive_old_data']:
            self.archive_dir.mkdir(exist_ok=True)
    
    def load_history(self):
        """بارگذاری سوابق موجود"""
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
        اضافه کردن یک تغییر قیمت به سوابق
        
        change_type: 'افزایش', 'کاهش', 'جدید', 'حذف'
        """
        if not HISTORY_SETTINGS['enable_history']:
            return
        
        # محاسبه تغییرات
        if old_price and new_price:
            change_amount = new_price - old_price
            change_percent = (change_amount / old_price) * 100 if old_price > 0 else 0
        else:
            change_amount = new_price if new_price else 0
            change_percent = 0
        
        # ساخت رکورد جدید
        new_record = {
            'sku': sku,
            'نام_محصول': product_name,
            'تاریخ_تغییر': datetime.now().strftime('%Y-%m-%d'),
            'تاریخ_شمسی': persian_date,
            'قیمت_قبلی': old_price if old_price else 0,
            'قیمت_جدید': new_price if new_price else 0,
            'تغییر_تومان': change_amount,
            'تغییر_درصد': f"{change_percent:+.2f}%",
            'نوع_تغییر': change_type,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return new_record
    
    def save_history(self, new_records):
        """ذخیره سوابق با محدودیت تعداد"""
        if not HISTORY_SETTINGS['enable_history'] or not new_records:
            return
        
        # بارگذاری سوابق موجود
        history_df = self.load_history()
        
        # اضافه کردن رکوردهای جدید
        new_df = pd.DataFrame(new_records)
        history_df = pd.concat([history_df, new_df], ignore_index=True)
        
        # محدود کردن تعداد رکوردها برای هر محصول
        max_records = HISTORY_SETTINGS['max_records_per_product']
        
        if 'sku' in history_df.columns:
            # نگهداری آخرین N رکورد برای هر SKU
            history_df = history_df.sort_values('timestamp', ascending=False)
            history_df = history_df.groupby('sku').head(max_records)
            history_df = history_df.sort_values(['sku', 'timestamp'], ascending=[True, False])
        
        # ذخیره
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
        """ایجاد snapshot روزانه"""
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
        
        # حذف snapshot های قدیمی
        self.cleanup_old_snapshots()
    
    def cleanup_old_snapshots(self):
        """حذف snapshot های قدیمی‌تر از N روز"""
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
        """دریافت سوابق یک محصول خاص"""
        history_df = self.load_history()
        if 'sku' in history_df.columns:
            product_history = history_df[history_df['sku'] == sku].sort_values('timestamp', ascending=False)
            return product_history
        return pd.DataFrame()
    
    def get_statistics(self):
        """آمار سوابق"""
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
            'date_range': f"{history_df['تاریخ_تغییر'].min()} to {history_df['تاریخ_تغییر'].max()}" if 'تاریخ_تغییر' in history_df.columns else None,
            'price_increases': len(history_df[history_df['نوع_تغییر'] == 'افزایش']) if 'نوع_تغییر' in history_df.columns else 0,
            'price_decreases': len(history_df[history_df['نوع_تغییر'] == 'کاهش']) if 'نوع_تغییر' in history_df.columns else 0,
            'new_products': len(history_df[history_df['نوع_تغییر'] == 'جدید']) if 'نوع_تغییر' in history_df.columns else 0,
        }
        
        return stats
