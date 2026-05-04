#!/usr/bin/env python3
"""
🤖 Werjo Bot - ملف التشغيل المبسط
مخصص للتشغيل على منصات الاستضافة مثل Railway
"""

import os
import sys
import asyncio
import logging
from bot import WerjoBot

# إعداد التسجيل
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def main():
    """تشغيل البوت"""
    logger.info("🤖 Werjo Bot - Discord Love Bot")
    logger.info("=" * 40)
    
    # الحصول على التوكن من متغيرات البيئة
    discord_token = os.getenv('DISCORD_TOKEN')
    
    if not discord_token:
        logger.error("❌ خطأ: يرجى تعيين DISCORD_TOKEN في متغيرات البيئة")
        sys.exit(1)
    
    logger.info("✅ التوكن موجود")
    logger.info("🚀 جاري تشغيل البوت...")
    
    # إنشاء البوت
    bot = WerjoBot()
    
    try:
        # تشغيل البوت
        bot.run(discord_token)
    except KeyboardInterrupt:
        logger.info("⏹️ تم إيقاف البوت")
    except Exception as e:
        logger.error(f"❌ خطأ: {e}")
        logger.error("💡 تأكد من:")
        logger.error("   • صحة التوكن")
        logger.error("   • دعوة البوت للسيرفر")
        logger.error("   • صلاحيات البوت")
        sys.exit(1)

if __name__ == "__main__":
    main()