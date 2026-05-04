#!/usr/bin/env python3
"""
اختبار صحة التوكن
"""

import discord
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

async def test_token():
    """اختبار التوكن"""
    token = os.getenv('DISCORD_TOKEN')
    
    if not token:
        print("❌ لا يوجد توكن في متغيرات البيئة")
        return
    
    print(f"🔍 اختبار التوكن: {token[:20]}...")
    
    try:
        # إنشاء client بسيط للاختبار
        intents = discord.Intents.default()
        client = discord.Client(intents=intents)
        
        @client.event
        async def on_ready():
            print(f"✅ التوكن صحيح!")
            print(f"📛 اسم البوت: {client.user}")
            print(f"🆔 معرف البوت: {client.user.id}")
            await client.close()
        
        await client.start(token)
        
    except discord.LoginFailure:
        print("❌ التوكن غير صحيح أو منتهي الصلاحية")
        print("💡 يرجى:")
        print("   • التحقق من التوكن في Discord Developer Portal")
        print("   • إعادة إنشاء التوكن إذا لزم الأمر")
        print("   • التأكد من نسخ التوكن كاملاً")
    except Exception as e:
        print(f"❌ خطأ: {e}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(test_token())