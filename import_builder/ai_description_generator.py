#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ماژول تولید توضیحات با AI
استفاده از Gemini API (رایگان)
"""

import os
import json

# تلاش برای import کردن google-generativeai
try:
    import google.generativeai as genai
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False
    print("⚠️  For AI descriptions, install: pip install google-generativeai")


class AIDescriptionGenerator:
    """کلاس تولید توضیحات با هوش مصنوعی"""
    
    def __init__(self, api_key=None):
        """
        مقداردهی اولیه
        api_key: کلید API گوگل جمینی (اختیاری - از env می‌خونه)
        """
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.model = None
        self.enabled = False  # ✅ Added for compatibility
        
        if HAS_GEMINI and self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
                self.enabled = True  # ✅ Added
                print("✅ AI Description Generator initialized successfully (Google Gemini)!")
            except Exception as e:
                print(f"⚠️  Failed to initialize Gemini: {e}")
                self.model = None
        elif not HAS_GEMINI:
            print("⚠️  google-generativeai not installed. Run: pip install google-generativeai")
        elif not self.api_key:
            print("⚠️  GEMINI_API_KEY not found in environment")
            print("   Get free API key from: https://makersuite.google.com/app/apikey")
    
    def is_available(self):
        """چک کردن در دسترس بودن AI"""
        return self.model is not None
    
    def generate_description(self, product_info, description_type='complete'):
        """
        تولید توضیحات برای محصول
        
        Args:
            product_info: دیکشنری اطلاعات محصول
            description_type: نوع توضیحات ('short' یا 'complete')
        
        Returns:
            توضیحات تولید شده (string)
        """
        if not self.is_available():
            return self._generate_fallback_description(product_info, description_type)
        
        try:
            prompt = self._create_prompt(product_info, description_type)
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"⚠️  AI generation failed: {e}")
            return self._generate_fallback_description(product_info, description_type)
    
    def _create_prompt(self, product_info, description_type):
        """ساخت prompt برای AI"""
        
        product_name = product_info.get('نام_محصول', 'محصول')
        model = product_info.get('مدل', '')
        colors = product_info.get('رنگ', '')
        material = product_info.get('جنس_رویه', '')
        lining = product_info.get('جنس_آستر', '')
        usage = product_info.get('کاربرد', '')
        bag_type = product_info.get('نوع_کیف', '')
        closure = product_info.get('نحوه_بسته_شدن_کیف', '')
        suitable_for = product_info.get('مناسب_برای', '')
        inside_pockets = product_info.get('تعداد_جیب_داخلی', '')
        outside_pockets = product_info.get('تعداد_جیب_بیرونی', '')
        dimensions = product_info.get('ابعاد', '')
        
        if description_type == 'short':
            prompt = f"""
لطفاً یک توضیحات کوتاه و جذاب (حداکثر 2-3 جمله) برای این محصول به زبان فارسی بنویس:

نام محصول: {product_name}
مدل: {model}
رنگ‌های موجود: {colors}
جنس: {material}
کاربرد: {usage}
مناسب برای: {suitable_for}

توضیحات باید:
- جذاب و فروش‌محور باشد
- ویژگی‌های کلیدی را برجسته کند
- حداکثر 50 کلمه
- بدون استفاده از emoji
"""
        else:  # complete
            prompt = f"""
لطفاً یک توضیحات کامل و حرفه‌ای برای این محصول به زبان فارسی بنویس:

مشخصات محصول:
- نام: {product_name}
- مدل: {model}
- رنگ‌های موجود: {colors}
- جنس رویه: {material}
- جنس آستر: {lining}
- نوع: {bag_type}
- نحوه بسته شدن: {closure}
- کاربرد: {usage}
- مناسب برای: {suitable_for}
- تعداد جیب داخلی: {inside_pockets}
- تعداد جیب بیرونی: {outside_pockets}
- ابعاد: {dimensions}

توضیحات باید شامل:
1. معرفی کلی محصول (1 پاراگراف)
2. ویژگی‌های کلیدی و مواد استفاده شده (1 پاراگراف)
3. کاربردها و مناسبت‌های استفاده (1 پاراگراف)
4. جمع‌بندی و دعوت به خرید (1 جمله)

شرایط:
- زبان فروش‌محور و جذاب
- SEO-friendly (استفاده طبیعی از کلمات کلیدی)
- حدود 150-200 کلمه
- بدون استفاده از emoji
- فارسی رسمی و روان
"""
        
        return prompt
    
    def _generate_fallback_description(self, product_info, description_type):
        """
        تولید توضیحات ساده در صورت عدم دسترسی به AI
        """
        product_name = product_info.get('نام_محصول', 'محصول')
        model = product_info.get('مدل', '')
        colors = product_info.get('رنگ', '')
        material = product_info.get('جنس_رویه', '')
        usage = product_info.get('کاربرد', '')
        
        if description_type == 'short':
            return f"{product_name} مدل {model} با جنس {material} برای استفاده {usage}. این محصول در رنگ‌های {colors} موجود است."
        else:
            return f"""
{product_name} مدل {model} یک انتخاب عالی برای استفاده {usage} است. این محصول با جنس باکیفیت {material} ساخته شده و در رنگ‌های متنوع {colors} در دسترس می‌باشد.

با توجه به طراحی زیبا و کاربردی، این {product_name} می‌تواند همراه ایده‌آل شما در فعالیت‌های روزمره باشد. 

برای خرید و کسب اطلاعات بیشتر با ما تماس بگیرید.
"""
    
    def generate_seo_meta(self, product_info):
        """
        تولید عنوان و توضیحات SEO
        
        Returns:
            tuple: (seo_title, seo_description)
        """
        product_name = product_info.get('نام_محصول', 'محصول')
        model = product_info.get('مدل', '')
        colors = product_info.get('رنگ', '')
        
        # عنوان SEO (حداکثر 60 کاراکتر)
        seo_title = f"{product_name} {model} | فروشگاه آنلاین"
        
        # توضیحات SEO (حداکثر 160 کاراکتر)
        color_list = colors.split(',')[0].strip() if colors else ''
        seo_desc = f"خرید {product_name} {model} با بهترین قیمت. رنگ {color_list} و سایر رنگ‌ها موجود. ارسال سریع به سراسر کشور."
        
        return seo_title, seo_desc
    
    def generate_for_woocommerce(self, product_info):
        """
        Generate all descriptions in WooCommerce format
        Compatible with woocommerce_generator
        
        Args:
            product_info: dict with:
                - product_name: نام محصول
                - model: کد محصول
                - colors: لیست رنگ‌ها
                - attributes: dict ویژگی‌ها
                - category: دسته‌بندی
        
        Returns:
            dict with: title, short_description, description, meta_description, focus_keyword
        """
        # Convert to old format
        old_format = {
            'نام_محصول': product_info.get('product_name', ''),
            'مدل': product_info.get('model', ''),
            'رنگ': ' | '.join(product_info.get('colors', [])),
            'جنس_رویه': product_info.get('attributes', {}).get('outer-material', ''),
            'جنس_آستر': product_info.get('attributes', {}).get('lining-material', ''),
            'کاربرد': product_info.get('attributes', {}).get('application', ''),
            'نوع_کیف': product_info.get('attributes', {}).get('bag-type', ''),
            'نحوه_بسته_شدن_کیف': product_info.get('attributes', {}).get('closure-style', ''),
            'مناسب_برای': product_info.get('attributes', {}).get('suitable-for', ''),
            'تعداد_جیب_داخلی': product_info.get('attributes', {}).get('number-of-inside-pockets', ''),
            'تعداد_جیب_بیرونی': product_info.get('attributes', {}).get('number-of-outside-pockets', ''),
            'ابعاد': product_info.get('attributes', {}).get('dimention', ''),
        }
        
        # Generate descriptions
        short_desc = self.generate_description(old_format, 'short')
        full_desc = self.generate_description(old_format, 'complete')
        seo_title, seo_desc = self.generate_seo_meta(old_format)
        
        product_name = product_info.get('product_name', '')
        model = product_info.get('model', '')
        
        return {
            'title': seo_title[:60],
            'short_description': short_desc[:300],
            'description': full_desc,
            'meta_description': seo_desc[:155],
            'focus_keyword': f"{product_name} کد {model}"
        }
    
    def batch_generate(self, products_df, progress_callback=None):
        """
        تولید توضیحات برای تعداد زیاد محصول
        
        Args:
            products_df: DataFrame محصولات
            progress_callback: تابع callback برای نمایش پیشرفت
        
        Returns:
            DataFrame با توضیحات اضافه شده
        """
        if not self.is_available():
            print("⚠️  AI not available, using fallback descriptions")
        
        total = len(products_df)
        
        for idx, row in products_df.iterrows():
            # تولید توضیحات کوتاه
            if pd.isna(row.get('توضیحات_کوتاه')) or row.get('توضیحات_کوتاه') == '':
                short_desc = self.generate_description(row.to_dict(), 'short')
                products_df.at[idx, 'توضیحات_کوتاه'] = short_desc
            
            # تولید توضیحات کامل
            if pd.isna(row.get('توضیحات_کامل')) or row.get('توضیحات_کامل') == '':
                complete_desc = self.generate_description(row.to_dict(), 'complete')
                products_df.at[idx, 'توضیحات_کامل'] = complete_desc
            
            # callback برای نمایش پیشرفت
            if progress_callback:
                progress_callback(idx + 1, total)
        
        return products_df


# تابع کمکی برای استفاده آسان
def generate_product_descriptions(products_df, api_key=None):
    """
    تابع ساده برای تولید توضیحات
    
    Usage:
        df = pd.read_excel('products.xlsx')
        df_with_desc = generate_product_descriptions(df)
    """
    generator = AIDescriptionGenerator(api_key)
    
    if not generator.is_available():
        print("⚠️  AI not available. Set GEMINI_API_KEY environment variable.")
        print("Get free API key from: https://makersuite.google.com/app/apikey")
        response = input("\nContinue with basic descriptions? (y/n): ")
        if response.lower() != 'y':
            return products_df
    
    print("\n🤖 Generating AI descriptions...")
    
    def progress(current, total):
        percent = (current / total) * 100
        print(f"Progress: {current}/{total} ({percent:.1f}%)", end='\r')
    
    result = generator.batch_generate(products_df, progress)
    print("\n✅ Descriptions generated!")
    
    return result


if __name__ == "__main__":
    # تست ماژول
    print("AI Description Generator Module")
    print("================================")
    
    # نمونه تست
    test_product = {
        'نام_محصول': 'کیف زنانه',
        'مدل': '5654',
        'رنگ': 'قرمز, مشکی, سبز',
        'جنس_رویه': 'چرم مصنوعی',
        'جنس_آستر': 'پلی‌استر',
        'کاربرد': 'روزمره',
        'نوع_کیف': 'دستی',
        'مناسب_برای': 'زنانه'
    }
    
    generator = AIDescriptionGenerator()
    
    if generator.is_available():
        print("\n📝 Generating short description...")
        short = generator.generate_description(test_product, 'short')
        print(f"\nShort: {short}")
        
        print("\n📝 Generating complete description...")
        complete = generator.generate_description(test_product, 'complete')
        print(f"\nComplete: {complete}")
    else:
        print("\n⚠️  AI not available (using fallback)")
        short = generator.generate_description(test_product, 'short')
        print(f"\nFallback Short: {short}")
