from models.repositories import ThemeSettingsRepository

class ThemeService:
    def __init__(self):
        self.repository = ThemeSettingsRepository()
    
    def get_current_theme(self):
        setting = self.repository.get_by_key('theme.mode')
        return setting.setting_value if setting else 'dark'
    
    def save_theme(self, theme_mode):
        return self.repository.save_or_update('theme.mode', theme_mode)
    
    def initialize_default_theme(self):
        if not self.repository.get_by_key('theme.mode'):
            self.repository.save_or_update('theme.mode', 'dark')