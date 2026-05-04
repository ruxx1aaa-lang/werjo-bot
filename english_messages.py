import random

# Morning messages
MORNING_MESSAGES = [
    "🌅 Good morning, beautiful souls! ☕",
    "🌞 Rise and shine, amazing people! 🌸",
    "☀️ A new day full of hope and joy! 🎉",
    "🌻 Morning filled with roses and jasmine! 🌹",
    "🦋 A morning full of positive energy! ✨",
    "🌈 Morning of beautiful dreams! 💫",
    "🎵 Morning of music and joy! 🎶",
    "🌺 Morning of blessings and goodness! 🙏",
    "☕ Morning coffee with the sweetest people! 💕",
    "🌸 Morning of love and peace! 🕊️"
]

# Evening messages
EVENING_MESSAGES = [
    "🌙 Good evening, beautiful family! 🌟",
    "✨ Evening light on your kind hearts! 💖",
    "🌆 Evening of calm and comfort! 🛋️",
    "🌃 A peaceful night full of sweet dreams! 😴",
    "🌙 Evening of warmth and tenderness! 🤗",
    "⭐ Evening of blessings and serenity! 🙏",
    "🌌 A quiet night and rosy dreams! 💤",
    "🕯️ Evening of safety and tranquility! 💫",
    "🌸 Evening of fragrance and beauty! 🌹",
    "💜 Evening of love and affection! 💕"
]

# Love messages
LOVE_MESSAGES = [
    "💕 Always remember that you are loved! 🤗",
    "🌟 You are the stars of this server! ✨",
    "💖 Love brings us together in this beautiful place! 🏠",
    "🌈 Together we create the most beautiful memories! 📸",
    "🎉 Every day with you is a celebration! 🎊",
    "💫 You are the reason this place is beautiful! 🌸",
    "🤝 One hand and one heart! 💗",
    "🌻 Your smiles light up my day! 😊",
    "🎵 Your voices are beautiful music! 🎶",
    "🌺 Thank you for being part of our family! 👨‍👩‍👧‍👦"
]

# Encouragement messages
ENCOURAGEMENT_MESSAGES = [
    "💪 You are stronger than you imagine! 🔥",
    "🌟 Every dream can become reality! ✨",
    "🚀 There are no limits to your potential! 🌌",
    "🎯 Focus on your goals and you will achieve them! 🏆",
    "💎 You are precious treasures! 👑",
    "🌱 Every day is an opportunity to grow and develop! 🌳",
    "⚡ Your positive energy is contagious! 😄",
    "🎨 Your creativity knows no bounds! 🖌️",
    "🌊 Flow with life positively! 🏄‍♂️",
    "🔮 The future is bright with you! ☀️"
]

def get_random_morning_message():
    """Get random morning message"""
    return random.choice(MORNING_MESSAGES)

def get_random_evening_message():
    """Get random evening message"""
    return random.choice(EVENING_MESSAGES)

def get_random_love_message():
    """Get random love message"""
    return random.choice(LOVE_MESSAGES)

def get_random_encouragement_message():
    """Get random encouragement message"""
    return random.choice(ENCOURAGEMENT_MESSAGES)