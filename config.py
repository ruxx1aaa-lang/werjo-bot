import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة (للتطوير المحلي فقط)
if os.path.exists('.env'):
    load_dotenv()

# إعدادات البوت - تعمل مع Railway و متغيرات البيئة
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GENERAL_CHANNEL_ID = int(os.getenv('GENERAL_CHANNEL_ID', '0'))
TIMEZONE = os.getenv('TIMEZONE', 'Africa/Cairo')

# ألوان الـ Embeds
COLORS = {
    'morning': 0xFFD700,  # ذهبي للصباح
    'evening': 0x9932CC,  # بنفسجي للمساء
    'love': 0xFF69B4,     # وردي للمحبة
    'success': 0x00FF00,  # أخضر للنجاح
    'info': 0x00BFFF      # أزرق للمعلومات
}

# أوقات الرسائل (24 ساعة)
MORNING_TIME = "08:00"
EVENING_TIME = "20:00"