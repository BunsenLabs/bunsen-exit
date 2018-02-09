# Enumeration of all the possible theme_entries keys and default values.
import gtk
from enum import Enum

class Default_Theme(Enum):
	name = "Unknown"
	author = "Unknown"
	window_width_adjustment = 0.50
	dialog_height = 130
	button_height = 130
	inner_border = 0
	sleep_delay = 0.001
	overall_opacity = 80
	button_spacing = 0
	icon_path = None
	button_image_cancel = gtk.STOCK_DIALOG_ERROR
	button_image_poweroff = gtk.STOCK_DIALOG_ERROR
	button_image_reboot = gtk.STOCK_DIALOG_ERROR
	button_image_suspend = gtk.STOCK_DIALOG_ERROR
	button_image_logout = gtk.STOCK_DIALOG_ERROR
	button_image_hybridsleep = gtk.STOCK_DIALOG_ERROR
	button_image_hibernate = gtk.STOCK_DIALOG_ERROR
	window_background_normal = '#838383'
	button_background_normal = '#838383'
	button_background_prelight = '#838383'
	text_color_normal = '#00ffff'
	text_color_prelight = '#000000'
	tooltip_background = '#838383'
	tooltip_foreground = '#000000'
	border_color = '#000040'
	
