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

# حالة الردود التلقائية (متوقفة افتراضياً)
AUTO_REACTIONS_ENABLED = False

# حالة الرسائل اليومية (متوقفة افتراضياً)
AUTO_DAILY_MESSAGES_ENABLED = False

# قاموس المشاعر والإيموجي المناسب
EMOTION_REACTIONS = {
    'happy': ['😊', '😄', '🎉', '❤️', '👍'],
    'sad': ['😢', '😔', '💔', '😞'],
    'love': ['❤️', '💕', '💖', '😍', '🥰'],
    'angry': ['😠', '😡', '💢'],
    'funny': ['😂', '🤣', '😆'],
    'thinking': ['🤔', '💭'],
    'celebrate': ['🎉', '🎊', '🥳', '🎈'],
    'support': ['💪', '👏', '🙌', '✨'],
    'thanks': ['🙏', '❤️', '😊'],
    'greeting': ['👋', '😊', '🌟'],
    'question': ['❓', '🤔'],
    'neutral': ['👍', '❤️']
}

# كلمات مفتاحية لكل مشاعر (عربي وإنجليزي)
EMOTION_KEYWORDS = {
    'happy': [
        'سعيد', 'فرحان', 'مبسوط', 'رائع', 'جميل', 'ممتاز', 'حلو', 'جميل', 'هايل',
        'happy', 'joy', 'great', 'awesome', 'wonderful', 'nice', 'good', 'excellent'
    ],
    'sad': [
        'حزين', 'زعلان', 'تعبان', 'مش مبسوط', 'مكتئب', 'حزن', 'زعل',
        'sad', 'unhappy', 'depressed', 'down', 'upset', 'crying', 'cry'
    ],
    'love': [
        'حب', 'بحب', 'احب', 'حبيب', 'قلبي', 'عشق', 'غرام', 'حبيبي', 'حبيبتي',
        'love', 'adore', 'heart', 'darling', 'sweetheart', '❤️', '💕'
    ],
    'angry': [
        'غضبان', 'زعلان', 'متضايق', 'مش عاجبني', 'غضب', 'عصبي',
        'angry', 'mad', 'furious', 'annoyed', 'frustrated'
    ],
    'funny': [
        'هههه', 'ههههه', 'هههههه', 'ضحك', 'مضحك', 'كوميدي', 'نكتة', 'lol', 'lmao',
        'haha', 'hahaha', 'funny', 'hilarious', 'joke', '😂', '🤣'
    ],
    'thinking': [
        'تفكير', 'فكرة', 'رأي', 'اعتقد', 'ممكن', 'يمكن',
        'think', 'thought', 'maybe', 'perhaps', 'wondering', 'hmm'
    ],
    'celebrate': [
        'مبروك', 'تهانينا', 'احتفال', 'عيد', 'نجاح', 'فوز',
        'congratulations', 'congrats', 'celebration', 'party', 'birthday', 'success'
    ],
    'support': [
        'تشجيع', 'قوة', 'تقدر', 'ممتاز', 'استمر', 'كمل', 'يلا',
        'support', 'encourage', 'strong', 'power', 'keep going', 'you can'
    ],
    'thanks': [
        'شكرا', 'شكراً', 'متشكر', 'ممنون', 'تسلم', 'الله يخليك',
        'thanks', 'thank you', 'thx', 'appreciate', 'grateful'
    ],
    'greeting': [
        'السلام عليكم', 'صباح الخير', 'مساء الخير', 'مرحبا', 'اهلا', 'هاي', 'هلو',
        'hello', 'hi', 'hey', 'greetings', 'good morning', 'good evening'
    ],
    'question': [
        'كيف', 'ليه', 'ازاي', 'متى', 'اين', 'ما', 'هل', '؟',
        'how', 'why', 'what', 'when', 'where', 'which', '?'
    ]
}

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
    print(f'⏸️ الرسائل اليومية متوقفة - استخدم !startdaily لتشغيلها')
    print(f'⏸️ الردود التلقائية متوقفة - استخدم !startreactions لتشغيلها')
    
    # بدء المهام اليومية (لكنها لن ترسل إلا إذا كانت مفعلة)
    if not daily_morning_task.is_running():
        daily_morning_task.start()
    
    if not daily_noon_task.is_running():
        daily_noon_task.start()
    
    if not daily_evening_task.is_running():
        daily_evening_task.start()

def analyze_emotion(text):
    """تحليل المشاعر في النص"""
    text_lower = text.lower()
    
    # حساب نقاط لكل مشاعر
    emotion_scores = {}
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        score = 0
        for keyword in keywords:
            if keyword in text_lower:
                score += 1
        if score > 0:
            emotion_scores[emotion] = score
    
    # إذا لم يتم العثور على أي مشاعر، استخدم neutral
    if not emotion_scores:
        return 'neutral'
    
    # إرجاع المشاعر الأعلى نقاطاً
    return max(emotion_scores, key=emotion_scores.get)

@tasks.loop(hours=24)
async def daily_morning_task():
    """إرسال رسالة صباحية يومياً في الساعة 8 صباحاً"""
    global AUTO_DAILY_MESSAGES_ENABLED
    
    # التحقق من أن الرسائل اليومية مفعلة
    if not AUTO_DAILY_MESSAGES_ENABLED:
        return
    
    # التحقق من الوقت (8 صباحاً)
    from datetime import datetime
    import pytz
    
    # استخدام توقيت القاهرة
    cairo_tz = pytz.timezone('Africa/Cairo')
    now = datetime.now(cairo_tz)
    
    if now.hour != 8:
        return
    
    print("🌅 إرسال رسالة صباحية...")
    
    morning_messages = [
        "🌅 صباح الخير يا أحلى أعضاء! ☕",
        "🌞 صباح النور والسرور على الجميع! 🌸",
        "☀️ يوم جديد مليء بالأمل والفرح! 🎉",
        "🌻 صباح الورد والياسمين! 🌹",
        "🦋 صباح مليء بالطاقة الإيجابية! ✨",
        "🌈 صباح الأحلام الجميلة! 💫",
        "🎵 صباح الموسيقى والفرح! 🎶"
    ]
    
    await send_daily_message(random.choice(morning_messages), "🌅 رسالة صباحية")

@tasks.loop(hours=24)
async def daily_noon_task():
    """إرسال مقولة يومية في الساعة 2 ظهراً"""
    global AUTO_DAILY_MESSAGES_ENABLED
    
    # التحقق من أن الرسائل اليومية مفعلة
    if not AUTO_DAILY_MESSAGES_ENABLED:
        return
    
    # التحقق من الوقت (2 ظهراً)
    from datetime import datetime
    import pytz
    
    # استخدام توقيت القاهرة
    cairo_tz = pytz.timezone('Africa/Cairo')
    now = datetime.now(cairo_tz)
    
    if now.hour != 14:
        return
    
    print("💭 إرسال مقولة اليوم...")
    
    quote = random.choice(RANDOM_QUOTES)
    await send_daily_message(f"💭 **مقولة اليوم:**\n{quote}", "💭 مقولة اليوم")

@tasks.loop(hours=24)
async def daily_evening_task():
    """إرسال رسالة مسائية يومياً في الساعة 8 مساءً"""
    global AUTO_DAILY_MESSAGES_ENABLED
    
    # التحقق من أن الرسائل اليومية مفعلة
    if not AUTO_DAILY_MESSAGES_ENABLED:
        return
    
    # التحقق من الوقت (8 مساءً)
    from datetime import datetime
    import pytz
    
    # استخدام توقيت القاهرة
    cairo_tz = pytz.timezone('Africa/Cairo')
    now = datetime.now(cairo_tz)
    
    if now.hour != 20:
        return
    
    print("🌙 إرسال رسالة مسائية...")
    
    evening_messages = [
        "🌙 مساء الخير يا أجمل عائلة! 🌟",
        "✨ مساء النور على قلوبكم الطيبة! 💖",
        "🌆 مساء الهدوء والراحة! 🛋️",
        "🌃 ليلة سعيدة مليئة بالأحلام الجميلة! 😴",
        "🌙 مساء الدفء والحنان! 🤗",
        "⭐ مساء البركة والسكينة! 🙏",
        "🌌 ليلة هادئة وأحلام وردية! 💤"
    ]
    
    await send_daily_message(random.choice(evening_messages), "🌙 رسالة مسائية")

async def send_daily_message(message, title):
    """إرسال رسالة يومية للقناة المحددة"""
    target_channel = None
    
    try:
        if os.path.exists('channel_settings.txt'):
            with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
                if ':' in content:
                    guild_id, channel_id = content.split(':')
                    target_channel = bot.get_channel(int(channel_id))
    except Exception as e:
        print(f"خطأ في قراءة إعدادات القناة: {e}")
    
    if target_channel:
        try:
            embed = discord.Embed(
                description=message,
                color=0xFFD700
            )
            embed.set_footer(text="Werjo Bot")
            
            await target_channel.send(embed=embed)
            print(f"✅ تم إرسال {title} إلى {target_channel.name}")
        except Exception as e:
            print(f"❌ خطأ في إرسال {title}: {e}")
    else:
        print(f"⚠️ لا توجد قناة محددة لإرسال {title}")

@bot.event
async def on_message(message):
    # تجاهل رسائل البوت نفسه
    if message.author == bot.user:
        return
    
    print(f'📨 رسالة من {message.author}: {message.content[:50]}...')
    
    # إضافة ردود فعل تلقائية إذا كانت مفعلة
    if AUTO_REACTIONS_ENABLED and message.content and len(message.content.strip()) > 0:
        try:
            # التحقق من صلاحيات البوت
            if not message.channel.permissions_for(message.guild.me).add_reactions:
                print(f'❌ لا توجد صلاحية add_reactions في القناة {message.channel.name}')
            else:
                # تحليل جميع المشاعر في النص (multi emotions)
                text_lower = message.content.lower()
                detected_emotions = {}  # استخدام dict لتتبع المشاعر والكلمات المكتشفة
                
                # البحث عن جميع المشاعر الموجودة في النص
                for emotion, keywords in EMOTION_KEYWORDS.items():
                    for keyword in keywords:
                        if keyword in text_lower:
                            if emotion not in detected_emotions:
                                detected_emotions[emotion] = []
                            detected_emotions[emotion].append(keyword)
                
                # إذا تم اكتشاف مشاعر، أضف ردود فعل متعددة
                if detected_emotions:
                    emotions_list = list(detected_emotions.keys())
                    print(f'🎭 المشاعر المكتشفة ({len(emotions_list)}): {", ".join(emotions_list)}')
                    
                    # إضافة ردود فعل لكل مشاعر مكتشفة
                    added_reactions = []
                    max_reactions = min(len(emotions_list), 5)  # حد أقصى 5 ردود فعل
                    
                    for emotion in emotions_list[:max_reactions]:
                        if emotion in EMOTION_REACTIONS:
                            # اختيار إيموجي عشوائي من المشاعر
                            available_emojis = [e for e in EMOTION_REACTIONS[emotion] if e not in added_reactions]
                            
                            if available_emojis:
                                emoji = random.choice(available_emojis)
                                try:
                                    await message.add_reaction(emoji)
                                    added_reactions.append(emoji)
                                    print(f'✅ تم إضافة {emoji} للمشاعر: {emotion}')
                                    await asyncio.sleep(0.3)  # تأخير بسيط بين كل إيموجي
                                except discord.HTTPException as e:
                                    print(f'⚠️ خطأ في إضافة {emoji}: {e}')
                                    # إذا فشل الإيموجي، جرب واحد تاني
                                    if len(available_emojis) > 1:
                                        emoji = random.choice([e for e in available_emojis if e != emoji])
                                        try:
                                            await message.add_reaction(emoji)
                                            added_reactions.append(emoji)
                                            print(f'✅ تم إضافة {emoji} بديل للمشاعر: {emotion}')
                                        except:
                                            pass
                    
                    if added_reactions:
                        print(f'✅ إجمالي الردود المضافة: {len(added_reactions)} - {" ".join(added_reactions)}')
                    else:
                        print(f'⚠️ لم يتم إضافة أي ردود فعل')
                else:
                    print(f'⏭️ لم يتم اكتشاف مشاعر محددة - تم تجاهل الرسالة')
                    
        except discord.Forbidden as e:
            print(f'❌ لا يمكن إضافة رد فعل - لا توجد صلاحيات: {e}')
        except discord.HTTPException as e:
            print(f'❌ خطأ HTTP في إضافة رد الفعل: {e}')
        except Exception as e:
            print(f'❌ خطأ غير متوقع في إضافة رد الفعل: {type(e).__name__}: {e}')
            import traceback
            traceback.print_exc()
    
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
              "**!startdaily** - تشغيل الرسائل اليومية 🌅\n"
              "**!stopdaily** - إيقاف الرسائل اليومية ⏸️\n"
              "**!dailystatus** - حالة الرسائل اليومية 📊\n"
              "**!startreactions** - تشغيل الردود التلقائية 🎭\n"
              "**!stopreactions** - إيقاف الردود التلقائية ⏸️\n"
              "**!reactionsstatus** - حالة الردود التلقائية 📊\n"
              "**!testreaction** - اختبار تحليل المشاعر 🧪\n"
              "**!checkreactions** - فحص صلاحيات الردود 🔍\n"
              "**!debug** - معلومات التشخيص 🔧",
        inline=False
    )
    
    # معلومات إضافية
    embed.add_field(
        name="ℹ️ معلومات إضافية",
        value="• الرسائل اليومية: 3 رسائل فقط (صباح، ظهر، مساء)\n"
              "• استخدم `!setchannel` لتحديد قناة ثم `!startdaily` لتشغيل الرسائل\n"
              "• استخدم `!startreactions` لتشغيل الردود التلقائية الذكية\n"
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
    embed = discord.Embed(
        description=f"💭 **مقولة ملهمة:**\n{quote}",
        color=0x00BFFF
    )
    embed.set_footer(text="Werjo Bot")
    await ctx.send(embed=embed)

@bot.command(name='startdaily')
async def startdaily_command(ctx):
    """تشغيل الرسائل اليومية التلقائية"""
    global AUTO_DAILY_MESSAGES_ENABLED
    
    print(f'▶️ تم استدعاء أمر startdaily من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ **خطأ في الصلاحيات**\nتحتاج إلى صلاحية إدارة القنوات لاستخدام هذا الأمر!")
        return
    
    if AUTO_DAILY_MESSAGES_ENABLED:
        await ctx.send("⚠️ **الرسائل اليومية مفعلة بالفعل!**")
        return
    
    # التحقق من وجود قناة محددة
    if not os.path.exists('channel_settings.txt'):
        await ctx.send("❌ **يجب تحديد قناة أولاً!**\nاستخدم `!setchannel` لتحديد القناة التي ستصل إليها الرسائل.")
        return
    
    AUTO_DAILY_MESSAGES_ENABLED = True
    
    embed = discord.Embed(
        title="✅ تم تشغيل الرسائل اليومية!",
        description="سيقوم البوت الآن بإرسال **3 رسائل يومياً** تلقائياً:",
        color=0x00FF00
    )
    
    embed.add_field(
        name="🌅 رسالة صباحية",
        value="**الوقت:** 8:00 صباحاً (توقيت القاهرة)\n**المحتوى:** رسالة تحفيزية لبداية اليوم",
        inline=False
    )
    
    embed.add_field(
        name="💭 مقولة اليوم",
        value="**الوقت:** 2:00 ظهراً (توقيت القاهرة)\n**المحتوى:** مقولة ملهمة واحدة",
        inline=False
    )
    
    embed.add_field(
        name="🌙 رسالة مسائية",
        value="**الوقت:** 8:00 مساءً (توقيت القاهرة)\n**المحتوى:** رسالة هادئة لنهاية اليوم",
        inline=False
    )
    
    embed.add_field(
        name="💡 ملاحظة",
        value="الرسائل ستصل تلقائياً كل يوم في الأوقات المحددة (3 رسائل فقط)",
        inline=False
    )
    
    embed.set_footer(text="استخدم !stopdaily لإيقاف الرسائل اليومية")
    
    await ctx.send(embed=embed)
    print("✅ تم تفعيل الرسائل اليومية")

@bot.command(name='stopdaily')
async def stopdaily_command(ctx):
    """إيقاف الرسائل اليومية التلقائية"""
    global AUTO_DAILY_MESSAGES_ENABLED
    
    print(f'⏸️ تم استدعاء أمر stopdaily من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ **خطأ في الصلاحيات**\nتحتاج إلى صلاحية إدارة القنوات لاستخدام هذا الأمر!")
        return
    
    if not AUTO_DAILY_MESSAGES_ENABLED:
        await ctx.send("⚠️ **الرسائل اليومية متوقفة بالفعل!**")
        return
    
    AUTO_DAILY_MESSAGES_ENABLED = False
    await ctx.send("⏸️ **تم إيقاف الرسائل اليومية!**\nلن تصل الرسائل الصباحية والمسائية تلقائياً بعد الآن.")
    print("⏸️ تم إيقاف الرسائل اليومية")

@bot.command(name='dailystatus')
async def dailystatus_command(ctx):
    """عرض حالة الرسائل اليومية"""
    global AUTO_DAILY_MESSAGES_ENABLED
    
    print(f'📊 تم استدعاء أمر dailystatus من {ctx.author}!')
    
    status = "🟢 مفعلة" if AUTO_DAILY_MESSAGES_ENABLED else "🔴 متوقفة"
    
    embed = discord.Embed(
        title="📊 حالة الرسائل اليومية",
        color=0x00FF00 if AUTO_DAILY_MESSAGES_ENABLED else 0xFF0000
    )
    
    embed.add_field(
        name="الحالة",
        value=status,
        inline=False
    )
    
    if AUTO_DAILY_MESSAGES_ENABLED:
        embed.add_field(
            name="🌅 الرسالة الصباحية",
            value="8:00 صباحاً",
            inline=True
        )
        embed.add_field(
            name="💭 مقولة اليوم",
            value="2:00 ظهراً",
            inline=True
        )
        embed.add_field(
            name="🌙 الرسالة المسائية",
            value="8:00 مساءً",
            inline=True
        )
        
        # عرض القناة المحددة
        try:
            if os.path.exists('channel_settings.txt'):
                with open('channel_settings.txt', 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if ':' in content:
                        guild_id, channel_id = content.split(':')
                        if int(guild_id) == ctx.guild.id:
                            channel = bot.get_channel(int(channel_id))
                            if channel:
                                embed.add_field(
                                    name="📍 القناة",
                                    value=channel.mention,
                                    inline=False
                                )
        except:
            pass
    else:
        embed.add_field(
            name="ملاحظة",
            value="استخدم `!startdaily` لتشغيل الرسائل اليومية",
            inline=False
        )
    
    embed.set_footer(text="Werjo Bot")
    await ctx.send(embed=embed)

@bot.command(name='startreactions')
async def startreactions_command(ctx):
    """تشغيل الردود التلقائية"""
    global AUTO_REACTIONS_ENABLED
    
    print(f'▶️ تم استدعاء أمر startreactions من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ **خطأ في الصلاحيات**\nتحتاج إلى صلاحية إدارة القنوات لاستخدام هذا الأمر!")
        return
    
    # التحقق من صلاحيات البوت
    bot_permissions = ctx.channel.permissions_for(ctx.guild.me)
    if not bot_permissions.add_reactions:
        await ctx.send("❌ **البوت لا يملك صلاحية إضافة ردود الفعل!**\nيرجى منح البوت صلاحية `Add Reactions` في إعدادات السيرفر.")
        return
    
    if AUTO_REACTIONS_ENABLED:
        await ctx.send("⚠️ **الردود التلقائية مفعلة بالفعل!**")
        return
    
    AUTO_REACTIONS_ENABLED = True
    
    embed = discord.Embed(
        title="✅ تم تشغيل الردود التلقائية!",
        description="سيقوم البوت الآن بإضافة ردود فعل **متعددة** على الرسائل التي تحتوي على كلمات مفتاحية محددة:",
        color=0x00FF00
    )
    
    embed.add_field(name="😊 سعادة", value="سعيد، فرحان، رائع، جميل", inline=True)
    embed.add_field(name="😢 حزن", value="حزين، زعلان، تعبان", inline=True)
    embed.add_field(name="❤️ حب", value="حب، قلبي، حبيب", inline=True)
    embed.add_field(name="😂 ضحك", value="هههه، ضحك، مضحك", inline=True)
    embed.add_field(name="🎉 احتفال", value="مبروك، احتفال، نجاح", inline=True)
    embed.add_field(name="💪 تشجيع", value="قوة، تقدر، استمر", inline=True)
    
    embed.add_field(
        name="💡 ملاحظات مهمة",
        value="• البوت يضيف ردود **فقط** على الرسائل التي تحتوي على الكلمات المفتاحية\n"
              "• يمكن إضافة **حتى 5 ردود فعل** على نفس الرسالة\n"
              "• كل مشاعر مكتشفة تحصل على إيموجي خاص بها\n"
              "• الرسائل العادية بدون كلمات مفتاحية **لن تحصل على ردود**",
        inline=False
    )
    
    embed.add_field(
        name="🧪 اختبر الآن",
        value="جرب: `أنا سعيد ومبسوط ومبروك عليك` → سيضيف 3 ردود مختلفة!",
        inline=False
    )
    
    embed.set_footer(text="استخدم !stopreactions لإيقاف الردود التلقائية")
    
    await ctx.send(embed=embed)
    print("✅ تم تفعيل الردود التلقائية")

@bot.command(name='stopreactions')
async def stopreactions_command(ctx):
    """إيقاف الردود التلقائية"""
    global AUTO_REACTIONS_ENABLED
    
    print(f'⏸️ تم استدعاء أمر stopreactions من {ctx.author}!')
    
    # فحص الصلاحيات
    if not ctx.author.guild_permissions.manage_channels:
        await ctx.send("❌ **خطأ في الصلاحيات**\nتحتاج إلى صلاحية إدارة القنوات لاستخدام هذا الأمر!")
        return
    
    if not AUTO_REACTIONS_ENABLED:
        await ctx.send("⚠️ **الردود التلقائية متوقفة بالفعل!**")
        return
    
    AUTO_REACTIONS_ENABLED = False
    await ctx.send("⏸️ **تم إيقاف الردود التلقائية!**\nلن يضيف البوت ردود فعل تلقائية بعد الآن.")
    print("⏸️ تم إيقاف الردود التلقائية")

@bot.command(name='reactionsstatus')
async def reactionsstatus_command(ctx):
    """عرض حالة الردود التلقائية"""
    global AUTO_REACTIONS_ENABLED
    
    print(f'📊 تم استدعاء أمر reactionsstatus من {ctx.author}!')
    
    status = "🟢 مفعلة" if AUTO_REACTIONS_ENABLED else "🔴 متوقفة"
    
    embed = discord.Embed(
        title="📊 حالة الردود التلقائية",
        color=0x00FF00 if AUTO_REACTIONS_ENABLED else 0xFF0000
    )
    
    embed.add_field(
        name="الحالة",
        value=status,
        inline=False
    )
    
    if AUTO_REACTIONS_ENABLED:
        embed.add_field(
            name="المشاعر المدعومة",
            value="😊 سعادة • 😢 حزن • ❤️ حب • 😂 ضحك\n🎉 احتفال • 💪 تشجيع • 🙏 شكر • 👋 تحية",
            inline=False
        )
    else:
        embed.add_field(
            name="ملاحظة",
            value="استخدم `!startreactions` لتشغيل الردود التلقائية",
            inline=False
        )
    
    embed.set_footer(text="Werjo Bot")
    await ctx.send(embed=embed)

@bot.command(name='testreaction')
async def testreaction_command(ctx, *, text: str = None):
    """اختبار تحليل المشاعر"""
    print(f'🧪 تم استدعاء أمر testreaction من {ctx.author}!')
    
    if not text:
        await ctx.send("❌ **يرجى كتابة نص للاختبار!**\nمثال: `!testreaction أنا سعيد جداً اليوم`")
        return
    
    # تحليل جميع المشاعر في النص
    text_lower = text.lower()
    detected_emotions = []
    
    for emotion, keywords in EMOTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                if emotion not in detected_emotions:
                    detected_emotions.append(emotion)
                break
    
    embed = discord.Embed(
        title="🧪 نتيجة تحليل المشاعر",
        description=f"**النص:** {text}",
        color=0x00BFFF
    )
    
    if detected_emotions:
        emotions_text = ", ".join([f"**{e}**" for e in detected_emotions])
        embed.add_field(
            name="المشاعر المكتشفة",
            value=emotions_text,
            inline=False
        )
        
        # عرض الردود المحتملة لكل مشاعر
        all_reactions = []
        for emotion in detected_emotions[:3]:
            if emotion in EMOTION_REACTIONS:
                emoji = random.choice(EMOTION_REACTIONS[emotion])
                all_reactions.append(emoji)
        
        if all_reactions:
            embed.add_field(
                name="الردود المحتملة",
                value=" ".join(all_reactions),
                inline=False
            )
            
            # محاولة إضافة ردود فعل على رسالة الأمر نفسها
            try:
                for emoji in all_reactions:
                    await ctx.message.add_reaction(emoji)
                    await asyncio.sleep(0.3)
                
                embed.add_field(
                    name="✅ اختبار الإضافة",
                    value=f"تم إضافة {len(all_reactions)} ردود فعل على رسالتك!",
                    inline=False
                )
            except discord.Forbidden:
                embed.add_field(
                    name="❌ خطأ في الصلاحيات",
                    value="البوت لا يملك صلاحية إضافة ردود الفعل!",
                    inline=False
                )
            except Exception as e:
                embed.add_field(
                    name="❌ خطأ",
                    value=f"حدث خطأ: {str(e)}",
                    inline=False
                )
    else:
        embed.add_field(
            name="⚠️ لم يتم اكتشاف مشاعر",
            value="النص لا يحتوي على كلمات مفتاحية معروفة",
            inline=False
        )
    
    embed.set_footer(text="Werjo Bot")
    await ctx.send(embed=embed)

@bot.command(name='checkreactions')
async def checkreactions_command(ctx):
    """فحص صلاحيات الردود التلقائية"""
    print(f'🔍 تم استدعاء أمر checkreactions من {ctx.author}!')
    
    embed = discord.Embed(
        title="🔍 فحص صلاحيات الردود التلقائية",
        color=0x00BFFF
    )
    
    # فحص صلاحيات البوت
    bot_permissions = ctx.channel.permissions_for(ctx.guild.me)
    
    permissions_status = []
    permissions_status.append(f"إضافة ردود الفعل: {'✅' if bot_permissions.add_reactions else '❌'}")
    permissions_status.append(f"قراءة الرسائل: {'✅' if bot_permissions.read_messages else '❌'}")
    permissions_status.append(f"قراءة تاريخ الرسائل: {'✅' if bot_permissions.read_message_history else '❌'}")
    
    embed.add_field(
        name="صلاحيات البوت",
        value="\n".join(permissions_status),
        inline=False
    )
    
    # حالة الردود التلقائية
    status = "🟢 مفعلة" if AUTO_REACTIONS_ENABLED else "🔴 متوقفة"
    embed.add_field(
        name="حالة الردود التلقائية",
        value=status,
        inline=False
    )
    
    # اختبار إضافة رد فعل
    try:
        await ctx.message.add_reaction("✅")
        embed.add_field(
            name="اختبار الإضافة",
            value="✅ البوت يستطيع إضافة ردود الفعل!",
            inline=False
        )
    except discord.Forbidden:
        embed.add_field(
            name="اختبار الإضافة",
            value="❌ البوت لا يستطيع إضافة ردود الفعل!\nيرجى منح البوت صلاحية `Add Reactions`",
            inline=False
        )
    except Exception as e:
        embed.add_field(
            name="اختبار الإضافة",
            value=f"❌ خطأ: {str(e)}",
            inline=False
        )
    
    embed.set_footer(text="Werjo Bot")
    await ctx.send(embed=embed)

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
    reactions_status = "🟢 مفعل" if AUTO_REACTIONS_ENABLED else "🔴 متوقف"
    daily_status = "🟢 مفعل" if AUTO_DAILY_MESSAGES_ENABLED else "🔴 متوقف"
    
    embed.add_field(
        name="⏰ المهام التلقائية",
        value=f"الردود التلقائية: {reactions_status}\nالرسائل اليومية: {daily_status}",
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