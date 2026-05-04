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
    embed = discord.Embed(
        title="📋 قائمة أوامر Werjo Bot",
        description="إليكم جميع الأوامر المتاحة:",
        color=0x00BFFF
    )
    
    commands_list = [
        ("!morning", "رسالة صباحية 🌅"),
        ("!evening", "رسالة مسائية 🌙"),
        ("!love", "رسالة محبة 💕"),
        ("!encourage", "رسالة تشجيع 💪"),
        ("!call", "الانضمام للقناة الصوتية 🎵"),
        ("!leave", "مغادرة القناة الصوتية 👋"),
        ("!setchannel", "تحديد قناة الرسائل (مشرفين) ⚙️"),
        ("!removechannel", "إلغاء قناة الرسائل (مشرفين) ❌"),
        ("!channelinfo", "معلومات القناة الحالية 📋"),
        ("!werjo", "عرض هذه القائمة 📋")
    ]
    
    for command, description in commands_list:
        embed.add_field(
            name=command,
            value=description,
            inline=True
        )
        
    embed.set_footer(text="مع الحب من Werjo Bot ❤️")
    await ctx.send(embed=embed)

@bot.command(name='morning')
async def morning_command(ctx):
    print(f'🌅 تم استدعاء أمر morning!')
    morning_messages = [
        "🌅 صباح الخير يا أحلى أعضاء! ☕",
        "🌞 صباح النور والسرور على الجميع! 🌸",
        "☀️ يوم جديد مليء بالأمل والفرح! 🎉",
        "🌻 صباح الورد والياسمين! 🌹",
        "🦋 صباح مليء بالطاقة الإيجابية! ✨"
    ]
    import random
    embed = discord.Embed(
        title="🌅 صباح الخير!",
        description=random.choice(morning_messages),
        color=0xFFD700
    )
    await ctx.send(embed=embed)

@bot.command(name='evening')
async def evening_command(ctx):
    print(f'🌙 تم استدعاء أمر evening!')
    evening_messages = [
        "🌙 مساء الخير يا أجمل عائلة! 🌟",
        "✨ مساء النور على قلوبكم الطيبة! 💖",
        "🌆 مساء الهدوء والراحة! 🛋️",
        "🌃 ليلة سعيدة مليئة بالأحلام الجميلة! 😴",
        "🌙 مساء الدفء والحنان! 🤗"
    ]
    import random
    embed = discord.Embed(
        title="🌙 مساء الخير!",
        description=random.choice(evening_messages),
        color=0x9932CC
    )
    await ctx.send(embed=embed)

@bot.command(name='love')
async def love_command(ctx):
    print(f'💕 تم استدعاء أمر love!')
    love_messages = [
        "💕 تذكروا دائماً أنكم محبوبون! 🤗",
        "🌟 أنتم نجوم هذا السيرفر! ✨",
        "💖 الحب يجمعنا في هذا المكان الجميل! 🏠",
        "🌈 معاً نصنع أجمل الذكريات! 📸",
        "🎉 كل يوم معكم هو احتفال! 🎊"
    ]
    import random
    embed = discord.Embed(
        description=random.choice(love_messages),
        color=0xFF69B4
    )
    await ctx.send(embed=embed)

@bot.command(name='encourage')
async def encourage_command(ctx):
    print(f'💪 تم استدعاء أمر encourage!')
    encourage_messages = [
        "💪 أنتم أقوى مما تتخيلون! 🔥",
        "🌟 كل حلم يمكن أن يصبح حقيقة! ✨",
        "🚀 لا حدود لإمكانياتكم! 🌌",
        "🎯 ركزوا على أهدافكم وستحققونها! 🏆",
        "💎 أنتم كنوز ثمينة! 👑"
    ]
    import random
    embed = discord.Embed(
        title="💪 رسالة تشجيع",
        description=random.choice(encourage_messages),
        color=0x00FF00
    )
    await ctx.send(embed=embed)

@bot.command(name='call')
async def call_command(ctx):
    print(f'🎵 تم استدعاء أمر call!')
    if ctx.author.voice is None:
        embed = discord.Embed(
            title="❌ لست في قناة صوتية",
            description="يجب أن تكون في قناة صوتية أولاً!",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return
    
    channel = ctx.author.voice.channel
    
    if ctx.voice_client is not None:
        embed = discord.Embed(
            title="🔄 الانتقال إلى قناتك",
            description=f"جاري الانتقال إلى {channel.mention}",
            color=0x00BFFF
        )
        await ctx.send(embed=embed)
        await ctx.voice_client.move_to(channel)
    else:
        embed = discord.Embed(
            title="🎵 الانضمام للقناة الصوتية",
            description=f"تم الانضمام إلى {channel.mention}",
            color=0x00FF00
        )
        await ctx.send(embed=embed)
        try:
            voice_client = await channel.connect(self_deaf=True)
        except Exception as e:
            await ctx.send(f"❌ خطأ في الاتصال: {e}")

@bot.command(name='leave')
async def leave_command(ctx):
    print(f'👋 تم استدعاء أمر leave!')
    if ctx.voice_client is None:
        embed = discord.Embed(
            title="❌ لست في قناة صوتية",
            description="لست متصل بأي قناة صوتية!",
            color=0xFF0000
        )
        await ctx.send(embed=embed)
        return
    
    embed = discord.Embed(
        title="👋 مغادرة القناة الصوتية",
        description="تم قطع الاتصال من القناة الصوتية",
        color=0x00BFFF
    )
    await ctx.send(embed=embed)
    await ctx.voice_client.disconnect()

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ لا يوجد توكن!")