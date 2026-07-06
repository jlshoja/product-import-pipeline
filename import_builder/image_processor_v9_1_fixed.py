#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Image Processor - Version 9.1 FIXED
✅ Fixed: Integration with new naming system
✅ Fixed: Product name manager support
✅ Updated: 2024-12-22

با 3 روش انتقال تصاویر:
1. تغییر نام لوکال (بدون انتقال)
2. آپلود FTP به سرور
3. آماده‌سازی برای WP All Import
"""

import os
import shutil
import pandas as pd
from pathlib import Path
from ftplib import FTP
import re

# ✅ Import New Modules
try:
    from product_name_manager import ProductNameManager
    HAS_PRODUCT_MANAGER = True
except ImportError:
    HAS_PRODUCT_MANAGER = False
    print("⚠️ product_name_manager.py not found")

try:
    from color_manager import ColorManager
    HAS_COLOR_MANAGER = True
except ImportError:
    HAS_COLOR_MANAGER = False
    print("⚠️ color_manager.py not found")

try:
    from image_naming_v9_fixed import generate_image_names_v9_fixed
    HAS_FIXED_NAMING = True
except ImportError:
    HAS_FIXED_NAMING = False
    print("⚠️ image_naming_v9_fixed.py not found")

class ImageProcessorFixed:
    """
    پردازشگر عکس‌ها با 3 روش مختلف
    """
    
    def __init__(self, source_folder, base_url, method='local_rename'):
        """
        مقداردهی اولیه
        
        Args:
            source_folder: پوشه محلی عکس‌ها
            base_url: URL پایه برای لینک‌ها
            method: روش انتقال
                - 'local_rename': فقط در لوکال تغییر نام بده
                - 'ftp': آپلود با FTP
                - 'wp_import': آماده برای WP All Import
        """
        self.source_folder = Path(source_folder)
        self.base_url = base_url.rstrip('/') + '/'
        self.method = method
        
        # پوشه خروجی با نام‌های جدید (در کنار source)
        self.output_folder = self.source_folder.parent / "renamed_images"
        self.output_folder.mkdir(exist_ok=True)
        
        # تنظیمات FTP (اگر نیاز باشد)
        self.ftp_host = None
        self.ftp_user = None
        self.ftp_pass = None
        self.ftp_remote_path = None
        
        # آمار
        self.stats = {
            'total': 0,
            'renamed': 0,
            'uploaded': 0,
            'errors': 0,
            'missing': 0
        }
        
        # ✅ Initialize Managers
        if HAS_PRODUCT_MANAGER:
            self.product_manager = ProductNameManager()
            print(f"📦 Product Manager: ✅ Loaded")
        else:
            self.product_manager = None
            print(f"📦 Product Manager: ⚠️ Not available")
        
        if HAS_COLOR_MANAGER:
            self.color_manager = ColorManager()
            print(f"🎨 Color Manager: ✅ Loaded")
        else:
            self.color_manager = None
            print(f"🎨 Color Manager: ⚠️ Not available")
        
        print(f"✅ Image Processor initialized")
        print(f"📁 Source: {self.source_folder}")
        print(f"📂 Output: {self.output_folder}")
        print(f"🔗 Base URL: {self.base_url}")
        print(f"🔧 Method: {self.method}")
    
    def configure_ftp(self, host, user, password, remote_path='/public_html/wp-content/uploads/products'):
        """
        تنظیم اطلاعات FTP
        
        Args:
            host: آدرس سرور (مثل ftp.luxbaz.com)
            user: نام کاربری FTP
            password: رمز عبور
            remote_path: مسیر روی سرور
        """
        self.ftp_host = host
        self.ftp_user = user
        self.ftp_pass = password
        self.ftp_remote_path = remote_path
        print(f"✅ FTP configured: {user}@{host}")
    
    def find_source_image(self, source_name):
        """
        پیدا کردن عکس منبع
        
        Args:
            source_name: نام فایل منبع (مثلاً "1a")
        
        Returns:
            Path object یا None
        """
        extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.JPG', '.JPEG', '.PNG']
        
        for ext in extensions:
            file_path = self.source_folder / f"{source_name}{ext}"
            if file_path.exists():
                return file_path
        
        return None
    
    def detect_source_extension(self, product_index):
        """
        تشخیص پسوند عکس‌های یک محصول
        
        Args:
            product_index: شماره یا SKU محصول (مثلاً 4729)
        
        Returns:
            str: پسوند (مثلاً '.jpg') یا '.jpg' پیش‌فرض
        """
        main_image = f"{product_index}a"
        source_path = self.find_source_image(main_image)
        
        if source_path:
            return source_path.suffix
        
        return '.jpg'  # پیش‌فرض
    
    def rename_local(self, source_name, target_name):
        """
        تغییر نام فایل در پوشه لوکال
        
        Args:
            source_name: نام منبع (مثل "1a")
            target_name: نام مقصد (مثل "women-bag-5654-red.jpg")
        
        Returns:
            tuple: (success: bool, output_path or error_message)
        """
        source_path = self.find_source_image(source_name)
        
        if not source_path:
            return False, f"Source not found: {source_name}"
        
        try:
            target_path = self.output_folder / target_name
            shutil.copy2(source_path, target_path)
            self.stats['renamed'] += 1
            return True, target_path
        
        except Exception as e:
            self.stats['errors'] += 1
            return False, str(e)
    
    def upload_ftp(self, local_path, remote_name):
        """
        آپلود فایل به سرور با FTP
        
        Args:
            local_path: مسیر فایل لوکال
            remote_name: نام فایل روی سرور
        
        Returns:
            tuple: (success: bool, message)
        """
        if not all([self.ftp_host, self.ftp_user, self.ftp_pass]):
            return False, "FTP not configured"
        
        try:
            ftp = FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            
            # رفتن به پوشه مقصد
            try:
                ftp.cwd(self.ftp_remote_path)
            except:
                # اگر پوشه نبود، بسازیم
                self._create_ftp_directory(ftp, self.ftp_remote_path)
                ftp.cwd(self.ftp_remote_path)
            
            # آپلود فایل
            with open(local_path, 'rb') as f:
                ftp.storbinary(f'STOR {remote_name}', f)
            
            ftp.quit()
            self.stats['uploaded'] += 1
            return True, "Uploaded"
        
        except Exception as e:
            self.stats['errors'] += 1
            return False, str(e)
    
    def _create_ftp_directory(self, ftp, path):
        """ساخت پوشه در FTP (recursive)"""
        parts = path.strip('/').split('/')
        for i, part in enumerate(parts):
            current_path = '/' + '/'.join(parts[:i+1])
            try:
                ftp.cwd(current_path)
            except:
                ftp.mkd(current_path)
    
    def process_image_mapping(self, mapping):
        """
        پردازش نگاشت عکس‌ها
        
        Args:
            mapping: dict {source_name: target_name}
                مثال: {'1a': 'women-bag-5654-main.jpg'}
        
        Returns:
            dict: {target_name: url}
        """
        results = {}
        
        print(f"\n{'='*70}")
        print(f"🖼️  Processing {len(mapping)} images")
        print(f"{'='*70}\n")
        
        for source_name, target_name in mapping.items():
            self.stats['total'] += 1
            
            # پیدا کردن عکس
            source_path = self.find_source_image(source_name)
            
            if not source_path:
                print(f"  ⚠️  Missing: {source_name}")
                self.stats['missing'] += 1
                results[target_name] = None
                continue
            
            # روش 1: فقط تغییر نام لوکال
            if self.method == 'local_rename':
                success, output = self.rename_local(source_name, target_name)
                
                if success:
                    url = self.base_url + target_name
                    print(f"  ✅ {source_name:<15} → {target_name:<40}")
                    results[target_name] = url
                else:
                    print(f"  ❌ {source_name:<15} → Error: {output}")
                    results[target_name] = None
            
            # روش 2: تغییر نام + آپلود FTP
            elif self.method == 'ftp':
                # اول rename
                success, output = self.rename_local(source_name, target_name)
                
                if not success:
                    print(f"  ❌ {source_name:<15} → Rename error: {output}")
                    results[target_name] = None
                    continue
                
                # بعد آپلود
                success, message = self.upload_ftp(output, target_name)
                
                if success:
                    url = self.base_url + target_name
                    print(f"  ✅ {source_name:<15} → {target_name:<40} [FTP]")
                    results[target_name] = url
                else:
                    print(f"  ❌ {source_name:<15} → Upload error: {message}")
                    results[target_name] = None
            
            # روش 3: برای WP All Import
            elif self.method == 'wp_import':
                success, output = self.rename_local(source_name, target_name)
                
                if success:
                    # در CSV از مسیر لوکال استفاده می‌کنیم
                    # WP All Import خودش آپلود می‌کنه
                    local_path = str(output).replace('\\', '/')
                    print(f"  ✅ {source_name:<15} → {target_name:<40} [Ready]")
                    results[target_name] = local_path
                else:
                    print(f"  ❌ {source_name:<15} → Error: {output}")
                    results[target_name] = None
        
        return results
    
    def update_csv_with_images(self, csv_file, image_results):
        """
        بروزرسانی CSV با آدرس عکس‌ها
        
        Args:
            csv_file: مسیر فایل CSV
            image_results: dict از process_image_mapping
        
        Returns:
            str: مسیر فایل جدید
        """
        df = pd.read_csv(csv_file, encoding='utf-8-sig')
        
        # ستون‌های مربوط به عکس
        image_columns = ['images', 'gallery_images']
        
        for col in image_columns:
            if col not in df.columns:
                continue
            
            def update_value(value):
                if pd.isna(value) or value == '':
                    return value
                
                # اگر چند عکس داشتیم
                if '|' in str(value):
                    images = str(value).split('|')
                    updated = []
                    for img in images:
                        img = img.strip()
                        # استخراج نام فایل
                        filename = img.split('/')[-1]
                        new_url = image_results.get(filename, img)
                        updated.append(new_url if new_url else img)
                    return '|'.join(updated)
                else:
                    # یک عکس
                    filename = str(value).split('/')[-1]
                    new_url = image_results.get(filename, value)
                    return new_url if new_url else value
            
            df[col] = df[col].apply(update_value)
        
        # ذخیره فایل جدید
        output_file = csv_file.replace('.csv', '_with_images.csv')
        df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ CSV updated: {output_file}")
        return output_file
    
    def print_stats(self):
        """نمایش آمار"""
        print(f"\n{'='*70}")
        print(f"📊 Image Processing Statistics")
        print(f"{'='*70}")
        print(f"  Total images: {self.stats['total']}")
        print(f"  ✅ Renamed: {self.stats['renamed']}")
        print(f"  ⬆️  Uploaded: {self.stats['uploaded']}")
        print(f"  ⚠️  Missing: {self.stats['missing']}")
        print(f"  ❌ Errors: {self.stats['errors']}")
        print(f"{'='*70}\n")
    
    def generate_mapping_from_excel(self, excel_file):
        """
        ✅ NEW: Generate image mapping from Excel using new naming system
        
        Args:
            excel_file: مسیر فایل Excel ورودی
        
        Returns:
            dict: {source_name: target_name}
        """
        if not HAS_FIXED_NAMING:
            print("⚠️ Fixed naming not available, cannot generate mapping")
            return {}
        
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        # Expand by colors
        expanded_rows = []
        for idx, row in df.iterrows():
            colors_str = str(row.get('رنگ', '')).strip()
            if pd.isna(colors_str) or not colors_str or colors_str == 'nan':
                expanded_rows.append(row.to_dict())
                continue
            
            colors = [c.strip() for c in re.split(r'\s*[-|,]\s*', colors_str) if c.strip()]
            if not colors:
                expanded_rows.append(row.to_dict())
                continue
            
            for color in colors:
                new_row = row.to_dict().copy()
                new_row['رنگ'] = color
                expanded_rows.append(new_row)
        
        df_expanded = pd.DataFrame(expanded_rows)
        
        # Generate mapping
        complete_mapping = {}
        grouped = df_expanded.groupby('sku')
        
        for sku, group in grouped:
            product_index = sku  # استفاده از SKU به عنوان product_index
            first_row = group.iloc[0]
            
            product_name = str(first_row.get('نام_محصول', '')).strip()
            model = str(first_row.get('مدل', '')).strip()
            
            # Get colors
            all_colors = [str(row['رنگ']).strip() for _, row in group.iterrows() if pd.notna(row.get('رنگ'))]
            
            # Translate colors
            if self.color_manager:
                colors_en = [self.color_manager.translate_color(c) for c in all_colors]
            else:
                colors_en = [c.replace(' ', '-').lower() for c in all_colors]
            
            # Get gallery count
            num_gallery = int(first_row.get('تعداد_عکس_گالری', 0)) if pd.notna(first_row.get('تعداد_عکس_گالری')) else 0
            
            # Generate names
            total_images = 1 + len(colors_en) + num_gallery
            image_info = generate_image_names_v9_fixed(
                product_index=product_index,
                product_name_fa=product_name,
                model=model,
                colors=colors_en,
                num_total_images=total_images,
                image_extension='.webp'
            )
            
            complete_mapping.update(image_info['mapping'])
        
        return complete_mapping


# ===========================
# CLI Usage Example
# ===========================

if __name__ == "__main__":
    import sys
    
    print("="*70)
    print("🖼️  Image Processor - Version 9.1 FIXED")
    print("="*70)
    
    if len(sys.argv) < 3:
        print("\nUsage:")
        print("  python image_processor_v9_1_fixed.py <excel_file> <method>")
        print("\nMethods:")
        print("  local_rename - Rename locally only")
        print("  ftp - Rename and upload via FTP")
        print("  wp_import - Prepare for WP All Import")
        print("\nExample:")
        print("  python image_processor_v9_1_fixed.py products.xlsx local_rename")
        sys.exit(1)
    
    excel_file = sys.argv[1]
    method = sys.argv[2] if len(sys.argv) > 2 else 'local_rename'
    
    if not os.path.exists(excel_file):
        print(f"❌ File not found: {excel_file}")
        sys.exit(1)
    
    # Initialize processor
    processor = ImageProcessorFixed(
        source_folder=r"E:\Luxbaz\Product images",
        base_url="https://luxbaz.com/wp-content/uploads/products/",
        method=method
    )
    
    # Configure FTP if needed
    if method == 'ftp':
        ftp_host = input("FTP Host: ")
        ftp_user = input("FTP User: ")
        ftp_pass = input("FTP Password: ")
        processor.configure_ftp(ftp_host, ftp_user, ftp_pass)
    
    # Generate mapping from Excel
    print("\n🔄 Generating image mapping from Excel...")
    mapping = processor.generate_mapping_from_excel(excel_file)
    
    if not mapping:
        print("❌ No mapping generated!")
        sys.exit(1)
    
    print(f"✅ Generated mapping for {len(mapping)} images")
    
    # Process images
    results = processor.process_image_mapping(mapping)
    
    # Show stats
    processor.print_stats()
    
    print("✅ Processing completed!")
