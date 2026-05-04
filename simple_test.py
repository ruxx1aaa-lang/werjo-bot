#!/usr/bin/env python3
"""
اختبار بسيط للبوت
"""

import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

# إعداد البوت مع الـ Intents
intents = discord.Intents.all()  # جميع الصلاحيات للاختبار

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} متصل!')
    print(f'🌐 متصل بـ {len(bot.guilds)} سيرفر')

@bot.event
async def on_message(message):
    print(f'📨 رسالة: {message.content} من {message.author}')
    
    # تجاهل رسائل البوت نفسه
    if message.author == bot.user:
        return
    
    # معالجة الأوامر
    await bot.process_commands(message)

@bot.command(name='test')
async def test_command(ctx):
    print(f'🧪 تم استدعاء أمر test!')
    await ctx.send("✅ البوت يعمل!")

@bot.command(name='werjo')
async def werjo_command(ctx):
    print(f'🤖 تم استدعاء أمر werjo!')
    await ctx.send("🤖 Werjo Bot يعمل بشكل صحيح!")

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ لا يوجد توكن!")