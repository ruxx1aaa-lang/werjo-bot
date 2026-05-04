import discord
from discord.ext import commands, tasks
import asyncio
import datetime
import pytz
import random
from config import *
from messages import *
from database import ServerDatabase

# إعداد البوت مع الـ Intents
intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

class WerjoBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix='!',
            intents=intents,
            help_command=None,
            activity=discord.Activity(type=discord.ActivityType.watching, name="💕 Werjo Bot")
        )
        self.db = ServerDatabase()  # قاعدة البيانات
        
    async def setup_hook(self):
        """إعداد البوت عند البدء"""
        print("🤖 جاري إعداد البوت...")
        # بدء المهام المجدولة
        self.daily_messages.start()
        self.random_love_messages.start()
        
    async def on_ready(self):
        """عند اتصال البوت بنجاح"""
        print(f'✅ {self.user} متصل ومستعد لنشر المحبة!')
        print(f'🌐 متصل بـ {len(self.guilds)} سيرفر')
        
        # إرسال رسالة ترحيب
        channel = self.get_channel(GENERAL_CHANNEL_ID)
        if channel:
            embed = discord.Embed(
                title="💖 Werjo Bot متصل!",
                description="مرحباً بكم! أنا Werjo Bot هنا لنشر المحبة والإيجابية 🌟",
                color=COLORS['love']
            )
            embed.add_field(
                name="🎯 مهمتي",
                value="• رسائل صباحية ومسائية يومية\n• رسائل محبة عشوائية\n• نشر الإيجابية والفرح",
                inline=False
            )
            embed.add_field(
                name="⚙️ إعداد القناة",
                value="استخدم `!setchannel` لتحديد قناة الرسائل التلقائية",
                inline=False
            )
            embed.set_footer(text="مع الحب من Werjo Bot ❤️")
            await channel.send(embed=embed)

    @tasks.loop(minutes=1)
    async def daily_messages(self):
        """إرسال الرسائل اليومية"""
        now = datetime.datetime.now(pytz.timezone(TIMEZONE))
        current_time = now.strftime("%H:%M")
        
        # الحصول على جميع القنوات المحفوظة
        channels = self.db.get_all_channels()
        
        # إذا لم توجد قنوات محفوظة، استخدم القناة الافتراضية
        if not channels and GENERAL_CHANNEL_ID:
            channels = {0: GENERAL_CHANNEL_ID}  # 0 كمعرف وهمي
        
        # رسالة الصباح
        if current_time == MORNING_TIME:
            embed = discord.Embed(
                title="🌅 رسالة الصباح",
                description=get_random_morning_message(),
                color=COLORS['morning']
            )
            embed.add_field(
                name="☀️ نصيحة اليوم",
                value=get_random_encouragement_message(),
                inline=False
            )
            embed.set_footer(text=f"الوقت: {now.strftime('%Y-%m-%d %H:%M')}")
            
            for guild_id, channel_id in channels.items():
                channel = self.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send to channel {channel_id}")
                    except Exception as e:
                        print(f"Error sending morning message: {e}")
            
        # رسالة المساء
        elif current_time == EVENING_TIME:
            embed = discord.Embed(
                title="🌙 رسالة المساء",
                description=get_random_evening_message(),
                color=COLORS['evening']
            )
            embed.add_field(
                name="✨ تأمل المساء",
                value="تذكروا إنجازاتكم اليوم واشكروا الله على نعمه 🙏",
                inline=False
            )
            embed.set_footer(text=f"الوقت: {now.strftime('%Y-%m-%d %H:%M')}")
            
            for guild_id, channel_id in channels.items():
                channel = self.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send to channel {channel_id}")
                    except Exception as e:
                        print(f"Error sending evening message: {e}")

    @tasks.loop(hours=2)
    async def random_love_messages(self):
        """إرسال رسائل محبة عشوائية كل ساعتين"""
        # احتمال 30% لإرسال رسالة
        if random.random() < 0.3:
            embed = discord.Embed(
                description=get_random_love_message(),
                color=COLORS['love']
            )
            
            # الحصول على جميع القنوات المحفوظة
            channels = self.db.get_all_channels()
            
            # إذا لم توجد قنوات محفوظة، استخدم القناة الافتراضية
            if not channels and GENERAL_CHANNEL_ID:
                channels = {0: GENERAL_CHANNEL_ID}
            
            for guild_id, channel_id in channels.items():
                channel = self.get_channel(channel_id)
                if channel:
                    try:
                        await channel.send(embed=embed)
                    except discord.Forbidden:
                        print(f"Cannot send to channel {channel_id}")
                    except Exception as e:
                        print(f"Error sending love message: {e}")

    @commands.command(name='setchannel')
    @commands.has_permissions(manage_channels=True)
    async def set_channel_command(self, ctx, channel: discord.TextChannel = None):
        """Set automatic messages channel (Admins only)"""
        if channel is None:
            channel = ctx.channel
        
        # Save channel in database
        self.db.set_channel(ctx.guild.id, channel.id)
        
        embed = discord.Embed(
            title="✅ تم تحديد القناة بنجاح!",
            description=f"سيتم إرسال الرسائل التلقائية في {channel.mention}",
            color=COLORS['success']
        )
        embed.add_field(
            name="📋 الرسائل التلقائية تشمل:",
            value="• رسائل صباحية (8:00 ص)\n• رسائل مسائية (8:00 م)\n• رسائل محبة عشوائية",
            inline=False
        )
        embed.set_footer(text="يمكن للمشرفين فقط تغيير هذا الإعداد")
        await ctx.send(embed=embed)

    @commands.command(name='removechannel')
    @commands.has_permissions(manage_channels=True)
    async def remove_channel_command(self, ctx):
        """Remove automatic messages channel (Admins only)"""
        current_channel = self.db.get_channel(ctx.guild.id)
        
        if current_channel is None:
            embed = discord.Embed(
                title="❌ لا توجد قناة محددة",
                description="لم يتم تحديد قناة للرسائل التلقائية مسبقاً",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
            return
        
        # Remove channel from database
        self.db.remove_channel(ctx.guild.id)
        
        embed = discord.Embed(
            title="✅ تم إلغاء القناة بنجاح!",
            description="لن يتم إرسال رسائل تلقائية في هذا السيرفر",
            color=COLORS['success']
        )
        embed.add_field(
            name="💡 لإعادة التفعيل:",
            value="استخدم `!setchannel` لتحديد قناة جديدة",
            inline=False
        )
        await ctx.send(embed=embed)

    @commands.command(name='channelinfo')
    async def channel_info_command(self, ctx):
        """Show automatic messages channel information"""
        current_channel_id = self.db.get_channel(ctx.guild.id)
        
        embed = discord.Embed(
            title="📋 معلومات قناة الرسائل",
            color=COLORS['info']
        )
        
        if current_channel_id:
            channel = self.get_channel(current_channel_id)
            if channel:
                embed.add_field(
                    name="📍 القناة الحالية:",
                    value=f"{channel.mention} (`{channel.name}`)",
                    inline=False
                )
                embed.add_field(
                    name="🕐 أوقات الرسائل:",
                    value=f"• الصباح: {MORNING_TIME}\n• المساء: {EVENING_TIME}",
                    inline=True
                )
                embed.add_field(
                    name="💕 رسائل المحبة:",
                    value="كل ساعتين تقريباً",
                    inline=True
                )
            else:
                embed.add_field(
                    name="⚠️ تحذير:",
                    value="القناة المحفوظة غير موجودة أو محذوفة",
                    inline=False
                )
        else:
            embed.add_field(
                name="❌ لا توجد قناة محددة",
                value="استخدم `!setchannel` لتحديد قناة الرسائل",
                inline=False
            )
        
        embed.set_footer(text="يمكن للمشرفين تغيير هذه الإعدادات")
        await ctx.send(embed=embed)

    @commands.command(name='call')
    async def join_voice_command(self, ctx):
        """Join voice channel"""
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
                color=COLORS['info']
            )
            await ctx.send(embed=embed)
            await ctx.voice_client.move_to(channel)
        else:
            embed = discord.Embed(
                title="🎵 الانضمام للقناة الصوتية",
                description=f"تم الانضمام إلى {channel.mention}",
                color=COLORS['success']
            )
            await ctx.send(embed=embed)
            voice_client = await channel.connect(self_deaf=True)

    @commands.command(name='leave')
    async def leave_voice_command(self, ctx):
        """Leave voice channel"""
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
            color=COLORS['info']
        )
        await ctx.send(embed=embed)
        await ctx.voice_client.disconnect()

    @commands.command(name='morning')
    async def morning_command(self, ctx):
        """Send morning message manually"""
        embed = discord.Embed(
            title="🌅 صباح الخير!",
            description=get_random_morning_message(),
            color=COLORS['morning']
        )
        await ctx.send(embed=embed)

    @commands.command(name='evening')
    async def evening_command(self, ctx):
        """Send evening message manually"""
        embed = discord.Embed(
            title="🌙 مساء الخير!",
            description=get_random_evening_message(),
            color=COLORS['evening']
        )
        await ctx.send(embed=embed)

    @commands.command(name='love')
    async def love_command(self, ctx):
        """Send love message"""
        embed = discord.Embed(
            description=get_random_love_message(),
            color=COLORS['love']
        )
        await ctx.send(embed=embed)

    @commands.command(name='encourage')
    async def encourage_command(self, ctx):
        """Send encouragement message"""
        embed = discord.Embed(
            title="💪 رسالة تشجيع",
            description=get_random_encouragement_message(),
            color=COLORS['success']
        )
        await ctx.send(embed=embed)

    @commands.command(name='werjo')
    async def help_command(self, ctx):
        """Show commands list"""
        embed = discord.Embed(
            title="📋 قائمة أوامر Werjo Bot",
            description="إليكم جميع الأوامر المتاحة:",
            color=COLORS['info']
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

    @commands.command(name='stats')
    @commands.has_permissions(administrator=True)
    async def stats_command(self, ctx):
        """عرض إحصائيات السيرفر (للمشرفين فقط)"""
        guild = ctx.guild
        embed = discord.Embed(
            title="📊 إحصائيات السيرفر",
            color=COLORS['info']
        )
        
        embed.add_field(name="👥 عدد الأعضاء", value=guild.member_count, inline=True)
        embed.add_field(name="📅 تاريخ الإنشاء", value=guild.created_at.strftime("%Y-%m-%d"), inline=True)
        embed.add_field(name="👑 المالك", value=guild.owner.mention if guild.owner else "غير معروف", inline=True)
        
        await ctx.send(embed=embed)

    async def on_member_join(self, member):
        """ترحيب بالأعضاء الجدد"""
        # البحث عن قناة محددة للسيرفر
        channel_id = self.db.get_channel(member.guild.id)
        
        if channel_id:
            channel = self.get_channel(channel_id)
        else:
            # استخدام القناة الافتراضية إذا لم توجد قناة محددة
            channel = self.get_channel(GENERAL_CHANNEL_ID)
        
        if not channel:
            return
            
        embed = discord.Embed(
            title="🎉 مرحباً بعضو جديد!",
            description=f"أهلاً وسهلاً {member.mention} في عائلتنا الجميلة! 💕",
            color=COLORS['love']
        )
        embed.add_field(
            name="🌟 نصيحة",
            value="لا تترددوا في التفاعل والمشاركة معنا!",
            inline=False
        )
        embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
        
        try:
            await channel.send(embed=embed)
        except discord.Forbidden:
            print(f"لا يمكن الإرسال في قناة الترحيب للسيرفر {member.guild.id}")
        except Exception as e:
            print(f"خطأ في إرسال رسالة الترحيب: {e}")

    async def on_command_error(self, ctx, error):
        """التعامل مع أخطاء الأوامر"""
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                title="❌ خطأ في الصلاحيات",
                description="عذراً، ليس لديك الصلاحية لاستخدام هذا الأمر",
                color=0xFF0000
            )
            embed.add_field(
                name="🔒 الصلاحيات المطلوبة:",
                value="إدارة القنوات (Manage Channels)",
                inline=False
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                title="❌ القناة غير موجودة",
                description="لم يتم العثور على القناة المحددة",
                color=0xFF0000
            )
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandNotFound):
            # تجاهل الأوامر غير الموجودة
            pass
        else:
            print(f"خطأ: {error}")

# تشغيل البوت
if __name__ == "__main__":
    bot = WerjoBot()
    
    if not DISCORD_TOKEN:
        print("❌ خطأ: لم يتم العثور على DISCORD_TOKEN في ملف .env")
        print("يرجى إضافة التوكن الخاص بالبوت في ملف .env")
    else:
        try:
            bot.run(DISCORD_TOKEN)
        except discord.LoginFailure:
            print("❌ خطأ في تسجيل الدخول: تأكد من صحة التوكن")
        except Exception as e:
            print(f"❌ خطأ في تشغيل البوت: {e}")