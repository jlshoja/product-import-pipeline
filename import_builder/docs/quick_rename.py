#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Quick Image Renamer
تغییر نام سریع عکس‌ها برای WooCommerce
بدون نیاز به فایل‌های دیگر
"""

import os
import shutil
from pathlib import Path

def rename_images_simple(source_folder, output_folder=None):
    """
    تغییر نام ساده عکس‌ها
    
    قانون:
    1a → product1-main
    1b → product1-color1
    1c → product1-color2
    1d → product1-gallery1
    ...
    """
    
    source = Path(source_folder)
    
    if output_folder is None:
        output = source.parent / "renamed_for_woocommerce"
    else:
        output = Path(output_folder)
    
    output.mkdir(exist_ok=True)
    
    # دریافت اطلاعات از کاربر
    print("\n" + "="*70)
    print("📸 Quick Image Renamer for WooCommerce")
    print("="*70)
    
    print(f"\n📁 Source: {source}")
    print(f"📂 Output: {output}")
    
    # پیدا کردن محصولات
    products = {}
    extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
    
    for file in source.iterdir():
        if file.suffix.lower() in extensions:
            # استخراج شماره محصول
            name = file.stem
            
            # بررسی فرمت (مثلاً 1a, 2b, 100c)
            import re
            match = re.match(r'(\d+)([a-z])', name.lower())
            
            if match:
                product_num = int(match.group(1))
                letter = match.group(2)
                
                if product_num not in products:
                    products[product_num] = []
                
                products[product_num].append((letter, file))
    
    if not products:
        print("\n❌ No images found matching pattern (1a, 2b, etc.)")
        return
    
    print(f"\n✅ Found {len(products)} products")
    print(f"   Total images: {sum(len(v) for v in products.values())}")
    
    # دریافت اطلاعات محصولات
    print("\n" + "-"*70)
    print("Enter product information:")
    print("-"*70)
    
    product_info = {}
    
    for product_num in sorted(products.keys()):
        print(f"\n📦 Product {product_num}:")
        print(f"   Images: {', '.join(sorted([l for l, _ in products[product_num]]))}")
        
        name = input(f"   Product name (EN): ").strip() or f"product{product_num}"
        model = input(f"   Model: ").strip() or str(product_num)
        
        # تعداد رنگ‌ها
        num_images = len(products[product_num])
        print(f"   Total images: {num_images}")
        
        if num_images > 1:
            num_colors = input(f"   How many colors? [default: {num_images-1}]: ").strip()
            num_colors = int(num_colors) if num_colors else num_images - 1
        else:
            num_colors = 0
        
        product_info[product_num] = {
            'name': name,
            'model': model,
            'num_colors': num_colors,
            'images': sorted(products[product_num], key=lambda x: x[0])
        }
    
    # پردازش و تغییر نام
    print("\n" + "="*70)
    print("🔄 Renaming images...")
    print("="*70)
    
    results = []
    
    for product_num, info in product_info.items():
        name = info['name']
        model = info['model']
        num_colors = info['num_colors']
        images = info['images']
        
        for idx, (letter, file) in enumerate(images):
            # تعیین نوع عکس
            if idx == 0:
                # اولین عکس = main
                new_name = f"{name}-{model}-main{file.suffix}"
                img_type = "main"
            
            elif idx <= num_colors:
                # عکس‌های رنگ
                new_name = f"{name}-{model}-color{idx}{file.suffix}"
                img_type = f"color{idx}"
            
            else:
                # عکس‌های گالری
                gallery_num = idx - num_colors
                if gallery_num == 1 and idx == len(images) - 1:
                    # فقط یک عکس گالری
                    new_name = f"{name}-{model}-gallery{file.suffix}"
                else:
                    new_name = f"{name}-{model}-gallery{gallery_num:02d}{file.suffix}"
                img_type = f"gallery{gallery_num}"
            
            # کپی فایل
            new_path = output / new_name
            
            try:
                shutil.copy2(file, new_path)
                print(f"  ✅ {file.name:<20} → {new_name:<40} ({img_type})")
                results.append({
                    'old': file.name,
                    'new': new_name,
                    'product': product_num,
                    'type': img_type
                })
            except Exception as e:
                print(f"  ❌ {file.name:<20} → Error: {e}")
    
    # خلاصه
    print("\n" + "="*70)
    print("📊 Summary")
    print("="*70)
    print(f"  Products: {len(product_info)}")
    print(f"  Images processed: {len(results)}")
    print(f"  Output folder: {output}")
    
    # ساخت فایل راهنما
    guide_file = output / "README.txt"
    with open(guide_file, 'w', encoding='utf-8') as f:
        f.write("Renamed Images for WooCommerce\n")
        f.write("="*70 + "\n\n")
        
        f.write("Products:\n")
        f.write("-"*70 + "\n")
        for product_num, info in product_info.items():
            f.write(f"\nProduct {product_num}: {info['name']} - Model {info['model']}\n")
            for result in results:
                if result['product'] == product_num:
                    f.write(f"  {result['old']:<20} → {result['new']:<40} ({result['type']})\n")
        
        f.write("\n" + "="*70 + "\n")
        f.write("\nNext Steps:\n")
        f.write("1. Check renamed images in this folder\n")
        f.write("2. Upload to server: /wp-content/uploads/products/\n")
        f.write("3. Use URLs in CSV:\n")
        f.write("   https://yoursite.com/wp-content/uploads/products/[filename]\n")
    
    print(f"\n✅ README saved: {guide_file}")
    
    print("\n💡 Next steps:")
    print(f"  1. Check renamed images in: {output}")
    print(f"  2. Upload to server (FileZilla/cPanel)")
    print(f"  3. Update CSV with URLs")
    
    return results


def create_csv_template(results, output_folder, base_url):
    """
    ساخت CSV ساده با URL های عکس‌ها
    """
    csv_file = Path(output_folder) / "image_urls.csv"
    
    with open(csv_file, 'w', encoding='utf-8') as f:
        f.write("filename,url,product,type\n")
        
        for result in results:
            filename = result['new']
            url = base_url.rstrip('/') + '/' + filename
            product = result['product']
            img_type = result['type']
            
            f.write(f"{filename},{url},{product},{img_type}\n")
    
    print(f"\n✅ CSV template saved: {csv_file}")
    return csv_file


if __name__ == "__main__":
    import sys
    
    print("="*70)
    print("🚀 Quick Image Renamer for WooCommerce")
    print("="*70)
    
    # دریافت مسیر پوشه
    default_source = r"E:\Luxbaz\Product images"
    
    source = input(f"\nSource folder [{default_source}]: ").strip()
    if not source:
        source = default_source
    
    if not os.path.exists(source):
        print(f"\n❌ Folder not found: {source}")
        sys.exit(1)
    
    # پردازش
    results = rename_images_simple(source)
    
    if results:
        # ساخت CSV
        base_url = input("\nBase URL [https://luxbaz.com/wp-content/uploads/products/]: ").strip()
        if not base_url:
            base_url = "https://luxbaz.com/wp-content/uploads/products/"
        
        output = Path(source).parent / "renamed_for_woocommerce"
        create_csv_template(results, output, base_url)
        
        print("\n🎉 Done!")
    else:
        print("\n⚠️  No images processed")
