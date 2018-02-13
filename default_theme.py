# Enumeration of all the possible theme_entries keys and default values.
import gtk

class Default_Theme():
	default_theme = {}
	
	def __init__(self):
		self.default_theme['name'] = "Classic"
		self.default_theme['author'] = "Unknown"
		self.default_theme['window_width_adjustment'] = 0.50
		self.default_theme['dialog_height'] = 64
		self.default_theme['button_height'] = 64
		self.default_theme['inner_border'] = 0
		self.default_theme['sleep_delay'] = 0.001
		self.default_theme['overall_opacity'] = 80
		self.default_theme['button_spacing'] = 0
		self.default_theme['icon_path'] = "/usr/share/images/bunsen/exit/dark"
		self.default_theme['button_image_cancel'] = "cancel-sm.png"
		self.default_theme['button_image_poweroff'] = "poweroff-sm.png"
		self.default_theme['button_image_reboot'] = "reboot-sm.png"
		self.default_theme['button_image_suspend'] = "sleep-sm.png"
		self.default_theme['button_image_logout'] = "logout-sm.png"
		self.default_theme['button_image_hybridsleep'] = "hibernate-sm.png"
		self.default_theme['button_image_hibernate'] = "hibernate-sm.png"
		self.default_theme['window_background_normal'] = '#696969'
		self.default_theme['button_background_normal'] = '#696969'
		self.default_theme['button_background_prelight'] = '#838383'
		self.default_theme['text_color_normal'] = '#000000'
		self.default_theme['text_color_prelight'] = '#ffffff'
		self.default_theme['tooltip_background'] = '#696969'
		self.default_theme['tooltip_foreground'] = '#000000'
		self.default_theme['border_color'] = '#000040'
		return
		
	def get_default_theme(self):
		return self.default_theme
	
	def __getitem__(self, key):
		return self.default_theme[key]

