#!/usr/bin/env python3
"""
🤖 بوت المحبة - Discord Love Bot
ملف التشغيل الرئيسي مع معالجة أفضل للأخطاء
"""

import asyncio
import sys
import os
from bot import WerjoBot
from config import DISCORD_TOKEN, GENERAL_CHANNEL_ID

def check_requirements():
    """فحص المتطلبات الأساسية"""
    errors = []
    
    # فحص التوكن
    if not DISCORD_TOKEN or DISCORD_TOKEN == "your_bot_token_here":
        errors.append("❌ لم يتم تعيين DISCORD_TOKEN في ملف .env")
    
    # فحص معرف القناة
    if not GENERAL_CHANNEL_ID or GENERAL_CHANNEL_ID == 0:
        errors.append("❌ لم يتم تعيين GENERAL_CHANNEL_ID في ملف .env")
    
    # فحص وجود ملف .env
    if not os.path.exists('.env'):
        errors.append("❌ ملف .env غير موجود")
    
    return errors

def print_banner():
    """طباعة شعار البوت"""
    banner = """
    ╔══════════════════════════════════════╗
    ║           🤖 Werjo Bot              ║
    ║        Discord Love Bot            ║
    ║                                    ║
    ║     لنشر المحبة والإيجابية 💕        ║
    ╚══════════════════════════════════════╝
    """
    print(banner)

async def main():
    """الدالة الرئيسية لتشغيل البوت"""
    print_banner()
    
    # فحص المتطلبات
    print("🔍 جاري فحص المتطلبات...")
    errors = check_requirements()
    
    if errors:
        print("\n💥 تم العثور على أخطاء في الإعداد:")
        for error in errors:
            print(f"   {error}")
        print("\n📋 يرجى مراجعة ملف README.md لمعرفة كيفية الإعداد الصحيح")
        return
    
    print("✅ جميع المتطلبات متوفرة!")
    print("🚀 جاري تشغيل البوت...")
    
    # إنشاء وتشغيل البوت
    bot = WerjoBot()
    
    try:
        await bot.start(DISCORD_TOKEN)
    except KeyboardInterrupt:
        print("\n⏹️  تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        print(f"\n💥 خطأ في تشغيل البوت: {e}")
        print("📋 يرجى التأكد من:")
        print("   • صحة التوكن")
        print("   • اتصال الإنترنت") 
        print("   • صلاحيات البوت في السيرفر")
    finally:
        if not bot.is_closed():
            await bot.close()
        print("👋 تم إغلاق البوت بأمان")

if __name__ == "__main__":
    try:
        # تشغيل البوت
        if sys.platform == "win32":
            # إعداد خاص بـ Windows
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
        
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 وداعاً!")
    except Exception as e:
        print(f"\n💥 خطأ غير متوقع: {e}")
        sys.exit(1)