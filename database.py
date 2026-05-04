import json
import os
from typing import Optional

class ServerDatabase:
    """قاعدة بيانات بسيطة لحفظ إعدادات السيرفرات"""
    
    def __init__(self, db_file: str = "server_settings.json"):
        self.db_file = db_file
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """تحميل البيانات من الملف"""
        if os.path.exists(self.db_file):
            try:
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}
        return {}
    
    def _save_data(self):
        """حفظ البيانات في الملف"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ البيانات: {e}")
    
    def set_channel(self, guild_id: int, channel_id: int):
        """تحديد قناة الرسائل لسيرفر معين"""
        guild_str = str(guild_id)
        if guild_str not in self.data:
            self.data[guild_str] = {}
        
        self.data[guild_str]['channel_id'] = channel_id
        self._save_data()
    
    def get_channel(self, guild_id: int) -> Optional[int]:
        """الحصول على قناة الرسائل لسيرفر معين"""
        guild_str = str(guild_id)
        if guild_str in self.data and 'channel_id' in self.data[guild_str]:
            return self.data[guild_str]['channel_id']
        return None
    
    def remove_channel(self, guild_id: int):
        """إزالة قناة الرسائل لسيرفر معين"""
        guild_str = str(guild_id)
        if guild_str in self.data and 'channel_id' in self.data[guild_str]:
            del self.data[guild_str]['channel_id']
            if not self.data[guild_str]:  # إذا كان السيرفر فارغ
                del self.data[guild_str]
            self._save_data()
    
    def get_all_channels(self) -> dict:
        """الحصول على جميع القنوات المحفوظة"""
        channels = {}
        for guild_id, settings in self.data.items():
            if 'channel_id' in settings:
                channels[int(guild_id)] = settings['channel_id']
        return channels