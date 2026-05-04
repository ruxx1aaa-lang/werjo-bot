# 🚂 Werjo Bot - جاهز للرفع على Railway

## ✅ الملفات المُعدة للـ Railway:

### 📁 ملفات التشغيل:
- ✅ `start.py` - ملف التشغيل الرئيسي
- ✅ `bot.py` - كود البوت الكامل
- ✅ `config.py` - محدث لمتغيرات البيئة
- ✅ `messages.py` - رسائل البوت العربية

### ⚙️ ملفات إعداد Railway:
- ✅ `Procfile` - أمر التشغيل
- ✅ `railway.json` - إعدادات النشر
- ✅ `runtime.txt` - إصدار Python
- ✅ `requirements.txt` - المكتبات المحدثة

### 📋 ملفات التوثيق:
- ✅ `RAILWAY_DEPLOYMENT.md` - دليل النشر الكامل
- ✅ `.env.example` - مثال لمتغيرات البيئة
- ✅ `.gitignore` - محدث للـ Railway

## 🔧 متغيرات البيئة المطلوبة في Railway:

```env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
GENERAL_CHANNEL_ID=معرف_القناة_هنا
TIMEZONE=Africa/Cairo
```

## 🚀 خطوات سريعة للنشر:

### 1. رفع على GitHub:
```bash
git init
git add .
git commit -m "Werjo Bot - Ready for Railway"
git remote add origin https://github.com/YOUR_USERNAME/werjo-bot.git
git push -u origin main
```

### 2. نشر على Railway:
1. اذهب إلى [railway.app](https://railway.app)
2. **New Project** → **Deploy from GitHub**
3. اختر الـ repository
4. أضف متغيرات البيئة في تبويب **Variables**

### 3. دعوة البوت:
```
https://discord.com/api/oauth2/authorize?client_id=1500644674216394903&permissions=2048&scope=bot
```

## 🎯 مميزات Werjo Bot:

- 🌅 رسائل صباحية تلقائية (8:00 ص)
- 🌙 رسائل مسائية تلقائية (8:00 م)
- 💕 رسائل محبة عشوائية (كل ساعتين)
- 🎉 ترحيب بالأعضاء الجدد
- 📱 أوامر تفاعلية عربية
- 🎨 تصميم Embeds أنيق

## 📊 الأوامر المتاحة:

- `!صباح` - رسالة صباحية
- `!مساء` - رسالة مسائية
- `!حب` - رسالة محبة
- `!تشجيع` - رسالة تشجيع
- `!مساعدة` - قائمة الأوامر
- `!احصائيات` - إحصائيات (للمشرفين)

## 💡 نصائح مهمة:

1. **احصل على معرف القناة:**
   - فعّل Developer Mode في Discord
   - انقر بالزر الأيمن على القناة → Copy ID

2. **راقب الـ Logs في Railway:**
   - تحقق من حالة البوت
   - اكتشف الأخطاء بسرعة

3. **تحديث البوت:**
   - ادفع التغييرات لـ GitHub
   - Railway سيعيد النشر تلقائياً

## 🎉 جاهز للنشر!

جميع الملفات مُعدة ومُحسنة للعمل على Railway. البوت سيعمل 24/7 وينشر المحبة في سيرفرك! 💕

---

**تم إعداده بحب ❤️**  
*Werjo Bot - لنشر السعادة في كل مكان*