#!/usr/bin/env python3
"""
🤖 Werjo Bot - Railway Deployment
ملف التشغيل المخصص لمنصة Railway
"""

import os
import sys
import asyncio
import logging
from bot import WerjoBot

# إعداد التسجيل للـ Railway
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

def get_env_variable(var_name, default=None):
    """الحصول على متغير البيئة مع معالجة الأخطاء"""
    value = os.getenv(var_name, default)
    if not value and var_name == 'DISCORD_TOKEN':
        logger.error(f"❌ متغير البيئة {var_name} غير موجود!")
        sys.exit(1)
    return value

def main():
    """تشغيل البوت على Railway"""
    logger.info("🚀 بدء تشغيل Werjo Bot على Railway...")
    
    # الحصول على متغيرات البيئة
    discord_token = get_env_variable('DISCORD_TOKEN')
    channel_id = get_env_variable('GENERAL_CHANNEL_ID', '0')
    timezone = get_env_variable('TIMEZONE', 'Africa/Cairo')
    
    logger.info(f"✅ تم تحميل الإعدادات:")
    logger.info(f"   - المنطقة الزمنية: {timezone}")
    logger.info(f"   - معرف القناة: {channel_id}")
    
    # إنشاء البوت
    bot = WerjoBot()
    
    try:
        logger.info("🔗 جاري الاتصال بـ Discord...")
        bot.run(discord_token)
    except KeyboardInterrupt:
        logger.info("⏹️ تم إيقاف البوت بواسطة المستخدم")
    except Exception as e:
        logger.error(f"❌ خطأ في تشغيل البوت: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()