# Enumeration of all the possible theme_entries keys and default values.
import gtk

class Default_Theme():
	default_theme = {}
	
	def __init__(self):
		self.default_theme['name'] = "Unknown"
		self.default_theme['author'] = "Unknown"
		self.default_theme['window_width_adjustment'] = 0.50
		self.default_theme['dialog_height'] = 130
		self.default_theme['button_height'] = 130
		self.default_theme['inner_border'] = 0
		self.default_theme['sleep_delay'] = 0.001
		self.default_theme['overall_opacity'] = 80
		self.default_theme['button_spacing'] = 0
		self.default_theme['icon_path'] = "/usr/share/images/bunsen/exit/dark"
		self.default_theme['button_image_cancel'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['button_image_poweroff'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['button_image_reboot'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['button_image_suspend'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['button_image_logout'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['button_image_hybridsleep'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['button_image_hibernate'] = gtk.STOCK_DIALOG_ERROR
		self.default_theme['window_background_normal'] = '#838383'
		self.default_theme['button_background_normal'] = '#838383'
		self.default_theme['button_background_prelight'] = '#838383'
		self.default_theme['text_color_normal'] = '#00ffff'
		self.default_theme['text_color_prelight'] = '#000000'
		self.default_theme['tooltip_background'] = '#838383'
		self.default_theme['tooltip_foreground'] = '#000000'
		self.default_theme['border_color'] = '#000040'
		return
		
	def get_default_theme(self):
		return self.default_theme
		

