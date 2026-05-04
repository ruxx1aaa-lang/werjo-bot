#!/usr/bin/env python3
"""
اختبار بسيط للبوت
"""

import discord
from discord.ext import commands, tasks
import asyncio
import os
import random
from dotenv import load_dotenv

load_dotenv()

# إعداد البوت مع الـ Intents
intents = discord.Intents.all()  # جميع الصلاحيات للاختبار

bot = commands.Bot(command_prefix='!', intents=intents)

# مقولات عشوائية
RANDOM_QUOTES = [
    "✨ النجاح ليس نهاية المطاف، والفشل ليس قاتلاً، إنما الشجاعة للمتابعة هي التي تهم.",
    "🌟 لا تنتظر الفرصة المثالية، اصنعها بنفسك.",
    "💪 القوة لا تأتي من القدرة الجسدية، بل من الإرادة التي لا تقهر.",
    "🎯 الهدف ليس أن تكون ناجحاً، بل أن تكون ذا قيمة.",
    "🌈 بعد كل عاصفة، تأتي قوس قزح.",
    "🔥 لا تخف من البداية البطيئة، خف فقط من عدم البداية.",
    "💎 الضغط يصنع الماس، والتحديات تصنع الأبطال.",
    "🌱 كل خبير كان يوماً مبتدئاً، وكل محترف كان يوماً هاوياً.",
    "⭐ النجوم لا تضيء إلا في الظلام.",
    "🚀 لا حدود لما يمكنك تحقيقه إذا لم تهتم بمن يحصل على الفضل.",
    "🌸 الحياة مثل الزهرة، تحتاج للصبر لترى جمالها.",
    "💫 كن التغيير الذي تريد أن تراه في العالم.",
    "🎨 الإبداع هو الذكاء وهو يستمتع.",
    "🌊 لا تنتظر الموجة المثالية، تعلم كيف تركب أي موجة.",
    "🏆 الفوز ليس كل شيء، لكن الرغبة في الفوز هي كل شيء."
]

@bot.event
async def on_ready():
    print(f'✅ {bot.user} متصل!')
    print(f'🌐 متصل بـ {len(bot.guilds)} سيرفر')
    
    # بدء المقولات العشوائية
    random_quotes_task.start()

@tasks.loop(hours=1)
async def random_quotes_task():
    """إرسال مقولات عشوائية كل ساعة"""
    print("📝 إرسال مقولة عشوائية...")
    
    # البحث عن القناة المحددة أولاً
    target_channel = None
    
    try:
        if os.path.exists('channel_settings.txt'):
            with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print(f"📄 قراءة إعدادات القناة: {content}")
                
                if ':' in content:
                    guild_id, channel_id = content.split(':')
                    target_channel = bot.get_channel(int(channel_id))
                    print(f"🔍 البحث عن القناة {channel_id} في السيرفر {guild_id}")
    except Exception as e:
        print(f"خطأ في قراءة إعدادات القناة: {e}")
    
    # إذا وجدت القناة المحددة، أرسل إليها
    if target_channel:
        try:
            quote = random.choice(RANDOM_QUOTES)
            embed = discord.Embed(
                description=f"💭 **مقولة اليوم:**\n{quote}",
                color=0x00BFFF
            )
            embed.set_footer(text="Werjo Bot")
            
            await target_channel.send(embed=embed)
            print(f"✅ تم إرسال المقولة إلى {target_channel.name}")
            return
        except discord.Forbidden:
            print(f"❌ لا يمكن الإرسال في القناة المحددة - لا توجد صلاحيات")
        except discord.NotFound:
            print(f"❌ القناة المحددة لم تعد موجودة")
        except Exception as e:
            print(f"❌ خطأ في إرسال المقولة للقناة المحددة: {e}")
    
    # إذا لم توجد قناة محددة أو فشل الإرسال، ابحث عن قناة عامة
    print("🔍 البحث عن قناة عامة...")
    for guild in bot.guilds:
        channel = None
        
        # البحث عن قناة عامة
        for ch in guild.text_channels:
            if any(word in ch.name.lower() for word in ['general', 'عام', 'chat', 'main']):
                channel = ch
                break
        
        # إذا لم توجد قناة عامة، استخدم أول قناة متاحة
        if not channel and guild.text_channels:
            channel = guild.text_channels[0]
        
        if channel:
            try:
                quote = random.choice(RANDOM_QUOTES)
                embed = discord.Embed(
                    description=f"💭 **مقولة اليوم:**\n{quote}",
                    color=0x00BFFF
                )
                embed.set_footer(text="Werjo Bot")
                
                await channel.send(embed=embed)
                print(f"✅ تم إرسال المقولة إلى {channel.name} في {guild.name}")
            except discord.Forbidden:
                print(f"❌ لا يمكن الإرسال في {guild.name} - لا توجد صلاحيات")
            except Exception as e:
                print(f"❌ خطأ في إرسال المقولة: {e}")

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
    
    # الأوامر العامة
    embed.add_field(
        name="🎯 الأوامر العامة",
        value="**!morning** - رسالة صباحية 🌅\n"
              "**!evening** - رسالة مسائية 🌙\n"
              "**!love** - رسالة محبة 💕\n"
              "**!encourage** - رسالة تشجيع 💪\n"
              "**!quote** - مقولة ملهمة 💭",
        inline=False
    )
    
    # أوامر الصوت
    embed.add_field(
        name="🎵 أوامر الصوت",
        value="**!call** - الانضمام للقناة الصوتية 🎵\n"
              "**!leave** - مغادرة القناة الصوتية 👋",
        inline=False
    )
    
    # أوامر الإدارة
    embed.add_field(
        name="⚙️ أوامر الإدارة (مشرفين)",
        value="**!setchannel** - تحديد قناة الرسائل 📍\n"
              "**!removechannel** - إلغاء قناة الرسائل ❌\n"
              "**!channelinfo** - معلومات القناة الحالية 📋\n"
              "**!debug** - معلومات التشخيص 🔧",
        inline=False
    )
    
    # معلومات إضافية
    embed.add_field(
        name="ℹ️ معلومات إضافية",
        value="• المقولات العشوائية ترسل كل ساعة تلقائياً\n"
              "• استخدم `!setchannel` لتحديد قناة معينة للرسائل\n"
              "• البوت يحتاج صلاحيات إدارة القنوات للأوامر الإدارية",
        inline=False
    )
        
    embed.set_footer(text="Werjo Bot")
    await ctx.send(embed=embed)

@bot.command(name='morning')
async def morning_command(ctx):
    print(f'🌅 تم استدعاء أمر morning!')
    morning_messages = [
        "🌅 صباح الخير يا أحلى أعضاء! ☕",
        "🌞 صباح النور والسرور على الجميع! 🌸",
        "☀️ يوم جديد مليء بالأمل والفرح! 🎉",
        "🌻 صباح الورد والياسمين! 🌹",
        "🦋 صباح مليء بالطاقة الإيجابية! ✨",
        "🌈 صباح الأحلام الجميلة! 💫",
        "🎵 صباح الموسيقى والفرح! 🎶"
    ]
    import random
    await ctx.send(random.choice(morning_messages))

@bot.command(name='evening')
async def evening_command(ctx):
    print(f'🌙 تم استدعاء أمر evening!')
    evening_messages = [
        "🌙 مساء الخير يا أجمل عائلة! 🌟",
        "✨ مساء النور على قلوبكم الطيبة! 💖",
        "🌆 مساء الهدوء والراحة! 🛋️",
        "🌃 ليلة سعيدة مليئة بالأحلام الجميلة! 😴",
        "🌙 مساء الدفء والحنان! 🤗",
        "⭐ مساء البركة والسكينة! 🙏",
        "🌌 ليلة هادئة وأحلام وردية! 💤"
    ]
    import random
    await ctx.send(random.choice(evening_messages))

@bot.command(name='love')
async def love_command(ctx):
    print(f'💕 تم استدعاء أمر love!')
    love_messages = [
        "💕 تذكروا دائماً أنكم محبوبون! 🤗",
        "🌟 أنتم نجوم هذا السيرفر! ✨",
        "💖 الحب يجمعنا في هذا المكان الجميل! 🏠",
        "🌈 معاً نصنع أجمل الذكريات! 📸",
        "🎉 كل يوم معكم هو احتفال! 🎊",
        "💫 أنتم السبب في جمال هذا المكان! 🌸",
        "🤝 يد واحدة وقلب واحد! 💗"
    ]
    import random
    await ctx.send(random.choice(love_messages))

@bot.command(name='encourage')
async def encourage_command(ctx):
    print(f'💪 تم استدعاء أمر encourage!')
    encourage_messages = [
        "💪 أنتم أقوى مما تتخيلون! 🔥",
        "🌟 كل حلم يمكن أن يصبح حقيقة! ✨",
        "🚀 لا حدود لإمكانياتكم! 🌌",
        "🎯 ركزوا على أهدافكم وستحققونها! 🏆",
        "💎 أنتم كنوز ثمينة! 👑",
        "🌱 كل يوم فرصة للنمو والتطور! 🌳",
        "⚡ طاقتكم الإيجابية معدية! 😄"
    ]
    import random
    await ctx.send(random.choice(encourage_messages))

@bot.command(name='quote')
async def quote_command(ctx):
    print(f'💭 تم استدعاء أمر quote!')
    quote = random.choice(RANDOM_QUOTES)
    await ctx.send(f"💭 **مقولة ملهمة:**\n{quote}")

@bot.command(name='setchannel')
async def setchannel_command(ctx, channel: discord.TextChannel = None):
    """تحديد قناة الرسائل التلقائية"""
    print(f'⚙️ تم استدعاء أمر setchannel من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ **خطأ في الصلاحيات**\nتحتاج إلى صلاحية إدارة القنوات لاستخدام هذا الأمر!")
        print(f"❌ {ctx.author} ليس لديه صلاحية manage_channels")
        return
    
    # إذا لم يتم تحديد قناة، استخدم القناة الحالية
    if channel is None:
        channel = ctx.channel
    
    # التأكد من أن القناة في نفس السيرفر
    if channel.guild.id != ctx.guild.id:
        await ctx.send("❌ لا يمكن تحديد قناة من سيرفر آخر!")
        return
    
    # حفظ معرف القناة في ملف
    try:
        with open('channel_settings.txt', 'w', encoding='utf-8') as f:
            f.write(f"{ctx.guild.id}:{channel.id}")
        
        await ctx.send(f"✅ **تم تحديد القناة بنجاح!**\n📍 القناة: {channel.mention}\n🕐 ستصل المقولات العشوائية كل ساعة إلى هذه القناة")
        print(f"✅ تم حفظ القناة {channel.name} للسيرفر {ctx.guild.name}")
        
    except Exception as e:
        await ctx.send(f"❌ **خطأ في حفظ الإعدادات**\n```{str(e)}```")
        print(f"❌ خطأ في حفظ الإعدادات: {e}")

@bot.command(name='channelinfo')
async def channelinfo_command(ctx):
    """عرض معلومات القناة المحددة"""
    print(f'📋 تم استدعاء أمر channelinfo من {ctx.author}!')
    
    try:
        # قراءة إعدادات القناة
        if os.path.exists('channel_settings.txt'):
            with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                print(f"📄 محتوى الملف: {content}")
                
                if ':' in content:
                    guild_id, channel_id = content.split(':')
                    print(f"🔍 البحث عن السيرفر {guild_id} والقناة {channel_id}")
                    
                    if int(guild_id) == ctx.guild.id:
                        channel = bot.get_channel(int(channel_id))
                        if channel:
                            embed = discord.Embed(
                                title="📋 معلومات القناة المحددة",
                                color=0x00BFFF
                            )
                            embed.add_field(name="📍 القناة", value=channel.mention, inline=False)
                            embed.add_field(name="🕐 المقولات العشوائية", value="كل ساعة", inline=False)
                            embed.add_field(name="🆔 معرف القناة", value=f"`{channel.id}`", inline=False)
                            embed.set_footer(text="استخدم !setchannel لتغيير القناة")
                            
                            await ctx.send(embed=embed)
                            print(f"✅ تم عرض معلومات القناة {channel.name}")
                        else:
                            await ctx.send("⚠️ **القناة المحفوظة لم تعد موجودة!**\nاستخدم `!setchannel` لتحديد قناة جديدة.")
                            print("⚠️ القناة المحفوظة غير موجودة")
                    else:
                        await ctx.send("❌ **لا توجد قناة محددة لهذا السيرفر!**\nاستخدم `!setchannel` لتحديد قناة.")
                        print(f"❌ السيرفر المحفوظ {guild_id} لا يطابق السيرفر الحالي {ctx.guild.id}")
                else:
                    await ctx.send("❌ **ملف الإعدادات تالف!**\nاستخدم `!setchannel` لإعادة تحديد القناة.")
                    print("❌ تنسيق ملف الإعدادات خاطئ")
        else:
            await ctx.send("❌ **لا توجد قناة محددة!**\nاستخدم `!setchannel` لتحديد قناة للرسائل التلقائية.")
            print("❌ ملف الإعدادات غير موجود")
            
    except Exception as e:
        await ctx.send(f"❌ **خطأ في قراءة الإعدادات**\n```{str(e)}```")
        print(f"❌ خطأ في قراءة الإعدادات: {e}")

@bot.command(name='removechannel')
async def removechannel_command(ctx):
    """إلغاء قناة الرسائل التلقائية"""
    print(f'🗑️ تم استدعاء أمر removechannel من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ **خطأ في الصلاحيات**\nتحتاج إلى صلاحية إدارة القنوات لاستخدام هذا الأمر!")
        print(f"❌ {ctx.author} ليس لديه صلاحية manage_channels")
        return
    
    try:
        if os.path.exists('channel_settings.txt'):
            # قراءة الملف أولاً للتحقق من السيرفر
            with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            if ':' in content:
                guild_id, channel_id = content.split(':')
                if int(guild_id) == ctx.guild.id:
                    # حذف الملف
                    os.remove('channel_settings.txt')
                    await ctx.send("✅ **تم إلغاء قناة الرسائل التلقائية بنجاح!**\nلن تصل المقولات العشوائية بعد الآن.")
                    print(f"✅ تم حذف إعدادات القناة للسيرفر {ctx.guild.name}")
                else:
                    await ctx.send("❌ لا توجد قناة محددة لهذا السيرفر!")
                    print(f"❌ السيرفر المحفوظ لا يطابق السيرفر الحالي")
            else:
                # حذف الملف التالف
                os.remove('channel_settings.txt')
                await ctx.send("⚠️ تم حذف ملف الإعدادات التالف!")
                print("⚠️ تم حذف ملف إعدادات تالف")
        else:
            await ctx.send("❌ **لا توجد قناة محددة مسبقاً!**\nاستخدم `!setchannel` لتحديد قناة أولاً.")
            print("❌ لا يوجد ملف إعدادات للحذف")
            
    except Exception as e:
        await ctx.send(f"❌ **خطأ في حذف الإعدادات**\n```{str(e)}```")
        print(f"❌ خطأ في حذف الإعدادات: {e}")

@bot.command(name='call')
async def call_command(ctx):
    print(f'🎵 تم استدعاء أمر call!')
    if ctx.author.voice is None:
        await ctx.send("❌ يجب أن تكون في قناة صوتية أولاً!")
        return
    
    channel = ctx.author.voice.channel
    
    try:
        if ctx.voice_client is not None:
            await ctx.send(f"🔄 جاري الانتقال إلى {channel.mention}")
            await ctx.voice_client.move_to(channel)
        else:
            await ctx.send(f"🎵 تم الانضمام إلى {channel.mention}")
            # الاتصال مع Deafen و Mute
            voice_client = await channel.connect(self_deaf=True, self_mute=True)
            
        # التأكد من أن البوت Deafened
        if ctx.voice_client:
            await ctx.guild.change_voice_state(channel=channel, self_mute=True, self_deaf=True)
            
    except Exception as e:
        await ctx.send(f"❌ خطأ في الاتصال: {e}")

@bot.command(name='debug')
async def debug_command(ctx):
    """أمر تشخيص المشاكل (للمطورين)"""
    print(f'🔧 تم استدعاء أمر debug من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.administrator:
        await ctx.send("❌ هذا الأمر مخصص للمشرفين فقط!")
        return
    
    embed = discord.Embed(
        title="🔧 معلومات التشخيص",
        color=0xFF9900
    )
    
    # معلومات البوت
    embed.add_field(
        name="🤖 معلومات البوت",
        value=f"الاسم: {bot.user.name}\nالمعرف: {bot.user.id}\nالخوادم: {len(bot.guilds)}",
        inline=False
    )
    
    # معلومات الصلاحيات
    permissions = ctx.channel.permissions_for(ctx.guild.me)
    embed.add_field(
        name="🔐 صلاحيات البوت",
        value=f"إرسال الرسائل: {'✅' if permissions.send_messages else '❌'}\n"
              f"إدارة الرسائل: {'✅' if permissions.manage_messages else '❌'}\n"
              f"الاتصال الصوتي: {'✅' if permissions.connect else '❌'}\n"
              f"التحدث: {'✅' if permissions.speak else '❌'}",
        inline=False
    )
    
    # معلومات القناة المحددة
    channel_info = "❌ لا توجد قناة محددة"
    try:
        if os.path.exists('channel_settings.txt'):
            with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if ':' in content:
                    guild_id, channel_id = content.split(':')
                    if int(guild_id) == ctx.guild.id:
                        channel = bot.get_channel(int(channel_id))
                        if channel:
                            channel_info = f"✅ {channel.mention} (ID: {channel.id})"
                        else:
                            channel_info = f"⚠️ القناة المحفوظة غير موجودة (ID: {channel_id})"
                    else:
                        channel_info = f"❌ القناة محفوظة لسيرفر آخر (ID: {guild_id})"
    except Exception as e:
        channel_info = f"❌ خطأ في قراءة الإعدادات: {e}"
    
    embed.add_field(
        name="📍 القناة المحددة",
        value=channel_info,
        inline=False
    )
    
    # معلومات المهام
    embed.add_field(
        name="⏰ المهام التلقائية",
        value=f"المقولات العشوائية: {'🟢 نشط' if random_quotes_task.is_running() else '🔴 متوقف'}",
        inline=False
    )
    
    embed.set_footer(text="استخدم هذه المعلومات لحل المشاكل")
    
    await ctx.send(embed=embed)

@bot.command(name='leave')
async def leave_command(ctx):
    print(f'👋 تم استدعاء أمر leave!')
    if ctx.voice_client is None:
        await ctx.send("❌ لست متصل بأي قناة صوتية!")
        return
    
    await ctx.send("👋 تم قطع الاتصال من القناة الصوتية")
    await ctx.voice_client.disconnect()

if __name__ == "__main__":
    token = os.getenv('DISCORD_TOKEN')
    if token:
        bot.run(token)
    else:
        print("❌ لا يوجد توكن!")