# 🚂 دليل رفع Werjo Bot على Railway

## 📋 الملفات المطلوبة للـ Railway:

✅ جميع الملفات جاهزة ومُعدة مسبقاً:

- `requirements.txt` - المكتبات المطلوبة
- `Procfile` - أمر التشغيل
- `railway.json` - إعدادات Railway
- `runtime.txt` - إصدار Python
- `start.py` - ملف التشغيل الرئيسي

## 🚀 خطوات الرفع على Railway:

### 1. إنشاء حساب Railway
1. اذهب إلى [railway.app](https://railway.app)
2. سجل دخول باستخدام GitHub
3. اربط حسابك بـ GitHub

### 2. رفع الكود على GitHub
```bash
# إنشاء repository جديد
git init
git add .
git commit -m "Initial commit - Werjo Bot"

# ربط بـ GitHub (استبدل USERNAME و REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git
git branch -M main
git push -u origin main
```

### 3. إنشاء مشروع على Railway
1. اذهب إلى [railway.app/dashboard](https://railway.app/dashboard)
2. انقر على **"New Project"**
3. اختر **"Deploy from GitHub repo"**
4. اختر الـ repository الخاص بك
5. انقر **"Deploy Now"**

### 4. إعداد متغيرات البيئة
في لوحة تحكم Railway:

1. اذهب إلى تبويب **"Variables"**
2. أضف المتغيرات التالية:

```env
DISCORD_TOKEN=YOUR_BOT_TOKEN_HERE
GENERAL_CHANNEL_ID=معرف_القناة_هنا
TIMEZONE=Africa/Cairo
```

### 5. إعداد القناة
1. في Discord، فعّل **Developer Mode**
2. انقر بالزر الأيمن على القناة المطلوبة
3. اختر **"Copy ID"**
4. ضع المعرف في متغير `GENERAL_CHANNEL_ID`

## 🔧 إعدادات Railway المتقدمة:

### في ملف `railway.json`:
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python start.py",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### في ملف `Procfile`:
```
web: python start.py
```

## 📊 مراقبة البوت:

### في لوحة تحكم Railway:
1. **Deployments** - حالة النشر
2. **Logs** - سجلات التشغيل
3. **Metrics** - استهلاك الموارد
4. **Settings** - الإعدادات العامة

## 🔄 تحديث البوت:

لتحديث البوت، ما عليك سوى:
```bash
git add .
git commit -m "Update bot"
git push
```

Railway سيقوم بإعادة النشر تلقائياً!

## 💰 التكلفة:

- **Hobby Plan**: مجاني حتى $5 شهرياً
- **Pro Plan**: $20 شهرياً للاستخدام المكثف

البوت البسيط عادة لا يتجاوز الحد المجاني.

## 🛠️ استكشاف الأخطاء:

### البوت لا يبدأ:
1. تحقق من **Logs** في Railway
2. تأكد من صحة `DISCORD_TOKEN`
3. تأكد من وجود جميع الملفات

### رسائل لا تُرسل:
1. تحقق من `GENERAL_CHANNEL_ID`
2. تأكد من صلاحيات البوت في Discord
3. راجع الـ Logs للأخطاء

### استهلاك عالي للموارد:
1. راجع **Metrics** في Railway
2. تحقق من عدد السيرفرات المتصل بها البوت

## 🎯 نصائح للأداء الأمثل:

1. **استخدم Logging** بدلاً من print
2. **راقب الاستهلاك** في Metrics
3. **حدّث البوت بانتظام** للحصول على أحدث المميزات
4. **اعمل backup** للكود على GitHub

## 🔗 روابط مفيدة:

- [Railway Documentation](https://docs.railway.app/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Python on Railway](https://docs.railway.app/languages/python)

---

## 🎉 البوت جاهز للعمل على Railway!

بعد اتباع هذه الخطوات، سيكون Werjo Bot يعمل 24/7 على Railway وينشر المحبة في سيرفرك! 💕

**رابط دعوة البوت:**
```
https://discord.com/api/oauth2/authorize?client_id=1500644674216394903&permissions=2048&scope=bot
```