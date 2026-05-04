# 🔧 حل مشكلة البوت

## المشكلة:
- روابط الدعوة لا تعمل
- البوت لا يستجيب

## الحل:

### 1. إنشاء بوت جديد:
1. اذهب إلى: https://discord.com/developers/applications
2. انقر "New Application"
3. اسم التطبيق: Werjo-Bot-New
4. اذهب إلى "Bot" → "Add Bot"
5. انسخ التوكن الجديد

### 2. تحديث التوكن في Railway:
1. اذهب إلى مشروعك في Railway
2. Variables → DISCORD_TOKEN
3. ضع التوكن الجديد

### 3. الحصول على رابط الدعوة:
1. في Discord Developer Portal
2. OAuth2 → URL Generator
3. Scopes: bot
4. Permissions: Send Messages, Embed Links, Read Message History
5. انسخ الرابط

### 4. إعدادات مهمة:
- فعّل Privileged Gateway Intents
- تأكد من أن البوت Public

## رابط دعوة مؤقت:
بعد إنشاء البوت الجديد، استبدل CLIENT_ID في هذا الرابط:
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID_HERE&permissions=2112&scope=bot