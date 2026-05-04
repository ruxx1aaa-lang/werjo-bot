#!/usr/bin/env python3
"""
اختبار سريع للبوت للتأكد من أنه يتصل بنجاح
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# إعداد البوت للاختبار (بدون صلاحيات خاصة)
intents = discord.Intents.default()
intents.message_content = False  # تعطيل هذه الصلاحية مؤقتاً

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'🎉 البوت متصل بنجاح!')
    print(f'📛 اسم البوت: {bot.user}')
    print(f'🆔 معرف البوت: {bot.user.id}')
    print(f'🌐 متصل بـ {len(bot.guilds)} سيرفر')
    
    # طباعة أسماء السيرفرات والقنوات
    if bot.guilds:
        print('📋 السيرفرات المتصل بها:')
        for guild in bot.guilds:
            print(f'   • {guild.name} (ID: {guild.id})')
            # طباعة أول 3 قنوات نصية
            text_channels = [ch for ch in guild.channels if isinstance(ch, discord.TextChannel)][:3]
            if text_channels:
                print(f'     القنوات النصية:')
                for channel in text_channels:
                    print(f'       - #{channel.name} (ID: {channel.id})')
    
    print('\n✅ البوت جاهز للعمل!')
    print('💡 لاستخدام Werjo Bot الكامل، قم بتحديث GENERAL_CHANNEL_ID في ملف .env')
    print('⏹️  اضغط Ctrl+C لإيقاف البوت')

@bot.command(name='test')
async def test_command(ctx):
    """أمر اختبار بسيط"""
    embed = discord.Embed(
        title="🧪 اختبار Werjo Bot",
        description="Werjo Bot يعمل بشكل مثالي! 🎉",
        color=0x00FF00
    )
    embed.add_field(
        name="📍 معلومات القناة",
        value=f"القناة: #{ctx.channel.name}\nالمعرف: {ctx.channel.id}",
        inline=False
    )
    await ctx.send(embed=embed)

if __name__ == "__main__":
    if not DISCORD_TOKEN:
        print("❌ خطأ: التوكن غير موجود!")
    else:
        print("🚀 جاري تشغيل البوت للاختبار...")
        try:
            bot.run(DISCORD_TOKEN)
        except Exception as e:
            print(f"❌ خطأ: {e}")