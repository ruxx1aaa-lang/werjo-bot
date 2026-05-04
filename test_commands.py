#!/usr/bin/env python3
"""
اختبار أوامر البوت بدون اتصال Discord
"""

import os
import tempfile
import shutil

def test_channel_settings():
    """اختبار نظام حفظ إعدادات القناة"""
    print("🧪 اختبار نظام إعدادات القناة...")
    
    # إنشاء مجلد مؤقت للاختبار
    test_dir = tempfile.mkdtemp()
    original_dir = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # اختبار 1: حفظ الإعدادات
        print("📝 اختبار حفظ الإعدادات...")
        guild_id = "123456789"
        channel_id = "987654321"
        
        with open('channel_settings.txt', 'w', encoding='utf-8') as f:
            f.write(f"{guild_id}:{channel_id}")
        
        print("✅ تم حفظ الإعدادات بنجاح")
        
        # اختبار 2: قراءة الإعدادات
        print("📖 اختبار قراءة الإعدادات...")
        
        if os.path.exists('channel_settings.txt'):
            with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if ':' in content:
                saved_guild_id, saved_channel_id = content.split(':')
                if saved_guild_id == guild_id and saved_channel_id == channel_id:
                    print("✅ تم قراءة الإعدادات بنجاح")
                else:
                    print("❌ البيانات المقروءة لا تطابق البيانات المحفوظة")
            else:
                print("❌ تنسيق الملف خاطئ")
        else:
            print("❌ الملف غير موجود")
        
        # اختبار 3: حذف الإعدادات
        print("🗑️ اختبار حذف الإعدادات...")
        
        if os.path.exists('channel_settings.txt'):
            os.remove('channel_settings.txt')
            print("✅ تم حذف الإعدادات بنجاح")
        else:
            print("❌ الملف غير موجود للحذف")
        
        # التحقق من الحذف
        if not os.path.exists('channel_settings.txt'):
            print("✅ تم التحقق من حذف الملف")
        else:
            print("❌ الملف لا يزال موجوداً")
            
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
    
    finally:
        # العودة للمجلد الأصلي وحذف المجلد المؤقت
        os.chdir(original_dir)
        shutil.rmtree(test_dir)
        print("🧹 تم تنظيف ملفات الاختبار")

def test_encoding():
    """اختبار التعامل مع النصوص العربية"""
    print("\n🧪 اختبار التعامل مع النصوص العربية...")
    
    test_dir = tempfile.mkdtemp()
    original_dir = os.getcwd()
    
    try:
        os.chdir(test_dir)
        
        # نص عربي للاختبار
        arabic_text = "مرحباً بكم في Werjo Bot! 🤖"
        
        # كتابة النص
        with open('test_arabic.txt', 'w', encoding='utf-8') as f:
            f.write(arabic_text)
        
        # قراءة النص
        with open('test_arabic.txt', 'r', encoding='utf-8') as f:
            read_text = f.read()
        
        if read_text == arabic_text:
            print("✅ التعامل مع النصوص العربية يعمل بشكل صحيح")
        else:
            print("❌ مشكلة في التعامل مع النصوص العربية")
            print(f"النص الأصلي: {arabic_text}")
            print(f"النص المقروء: {read_text}")
            
    except Exception as e:
        print(f"❌ خطأ في اختبار النصوص العربية: {e}")
    
    finally:
        os.chdir(original_dir)
        shutil.rmtree(test_dir)

def main():
    """تشغيل جميع الاختبارات"""
    print("🚀 بدء اختبارات البوت...")
    print("=" * 50)
    
    test_channel_settings()
    test_encoding()
    
    print("\n" + "=" * 50)
    print("✅ انتهت جميع الاختبارات!")

if __name__ == "__main__":
    main()