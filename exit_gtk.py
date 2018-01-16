import pygtk
pygtk.require('2.0')
import gtk
import gobject
import logging
import collections
from colored_image_button import ColoredImageButton

exit_log = logging.getLogger('Bunsen-Exit-Log')


class ExitGtk:
	exit_bus = ''
	color_button = None
	window = None

	def _key_press_event(self, widget, event):
		keyval = event.keyval
		keyval_name = gtk.gdk.keyval_name(keyval)
		state = event.state
		alt = (state & gtk.gdk.MOD1_MASK)
		# Cancel shortcut
		if alt and keyval_name == 'c':
			self.destroy()
		# Logout Shortcut
		elif alt and keyval_name == 'l':
			self.send_to_dbus('Logout')
		# Suspend shortcut
		elif alt and keyval_name == 's':
			self.send_to_dbus('Suspend')
		# Reboot Shortcut
		elif alt and keyval_name == 'b':
			self.send_to_dbus('Reboot')
		# Poweroff shortcut
		elif alt and keyval_name == 'p':
			self.send_to_dbus('PowerOff')
		# Hibernate Shortcut
		elif alt and keyval_name == 'i':
			self.send_to_dbus('Hibernate')
		# Hybrid Sleep Shortcut
		elif alt and keyval_name == 'y':
			self.send_to_dbus('HybridSleep')
		# Cancel Shortcut
		elif keyval_name == 'Escape':
			self.destroy()
		elif keyval_name == 'Alt':
			self.show_button_labels()
		else:
			return False
		return True
		
	def destroy(self, widget=None, event=None, data=None):
		self.window.hide_all()
		gtk.main_quit()

	def __init__(self, button_values, exit_bus, theme, theme_entries, style_path):
		self.theme_entries = theme_entries
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		# Format the window.
		self.window.set_name('Bunsen Exit')
		self.window.set_decorated(False)
		self.window.connect("delete_event", self.destroy)
		self.window.connect("destroy_event", self.destroy)
		self.window.connect("key-press-event", self._key_press_event)
		self.window.set_resizable(False)
		self.window.set_keep_above(True)
		self.window.stick()
		self.window.set_position(gtk.WIN_POS_CENTER)
		windowicon = self.window.render_icon(gtk.STOCK_QUIT, gtk.ICON_SIZE_DIALOG)
		self.window.set_icon(windowicon)
		self.window.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['window_background_normal']))
		button_box = gtk.HButtonBox()
		button_box.set_layout(gtk.BUTTONBOX_SPREAD)
		for key, value in button_values.iteritems():
			# Format the keys into dbus actions
			if key == 'cancel':
				key = 'Cancel'
			elif key == 'logout':
				key = 'Logout'
			elif key == 'suspend':
				key = 'Suspend'
			elif key == 'poweroff':
				key = 'PowerOff'
			elif key == 'reboot':
				key = 'Reboot'
			elif key == 'hibernate':
				key = 'Hibernate'
			elif key == 'hybridsleep':
				key = 'HybridSleep'
			# only add buttons that are to be shown
			if value == 'show':
				exit_log.info('Creating button for ' + key)
				self.add_buttons(key, self.theme_entries, button_box)
				gobject.type_register(ColoredImageButton)
		self.window.add(button_box)
		self.window.show_all()
		return

	def main(self, button_visibility, style, theme, theme_entries):
		gtk.main()


	def query_tooltip_custom_cb(self, widget, x, y, keyboard_tip, tooltip, tooltip_label, tooltip_window, key):
		bg_color = gtk.gdk.color_parse(self.theme_entries['window_background_normal'])
		fg_color = self.theme_entries['text_color_normal']
		label_markup = '<span foreground="' + fg_color + '">' + key + '</span>'
		#tooltip.modify_bg(gtk.STATE_NORMAL, bg_color)
		# create the label
		tooltip_label.set_markup(label_markup)
		tooltip_window.modify_bg(gtk.STATE_NORMAL, bg_color)
		tooltip_label.show()
		tooltip_window.show()
		return True

	def add_buttons(self, key, theme_entries, button_box):
		# iconpath refers to a theme_entry in bl-exitrc.
		# It needs to refer to  a valid path. Checks for path exists
		# and points to an image need to be added. 
		if 'iconpath' in self.theme_entries:
			icon_path = self.theme_entries[ 'iconpath' ]
			image_key = 'buttonimage' + key.lower()
			button_image = icon_path + "/" + self.theme_entries[ image_key ]
			exit_log.debug("Loading theme entry " + key + " from " + button_image)
			self.color_button = ColoredImageButton(key, button_image, self.theme_entries)
			self.color_button.set_name(key)
			frame = gtk.Frame()
			frame.set_border_width(2)
			frame.add(self.color_button)
			button_box.add(frame)
		else:
			exit_log.warn("Icon path not found. Defaulting to button labels.")
			self.color_button = gtk.Button()
			self.color_button.set_name(key)
			self.color_button.set_relief(gtk.RELIEF_NONE)
			self.color_button.set_label(key)
			button_box.add(self.button)
		self.color_button.set_border_width(0)
		tooltip_label = gtk.Label()
		tooltip_window = gtk.Window(gtk.WINDOW_POPUP)
		bg_color = gtk.gdk.color_parse(theme_entries['window_background_normal'])
		fg_color = self.theme_entries['text_color_normal']
		label_markup = '<span foreground="' + fg_color + '">' + key + '</span>'
		# create the label
		tooltip_label.set_markup(label_markup)
		tooltip_window.modify_bg(gtk.STATE_NORMAL, bg_color)
		self.color_button.set_tooltip_window(tooltip_window)
		tooltip_window.add(tooltip_label)
		self.color_button.connect("query-tooltip", self.query_tooltip_custom_cb, tooltip_label, tooltip_window, key)
		self.color_button.props.has_tooltip = True
		button_box.show()
		self.color_button.show()
		
		return
		
	def configure(self, theme, theme_entries):
		# There is probably something I need to do here.
		#self.configured_theme.set_details_from_config(self.cp, default_theme)
		if theme != None or theme_entries != None:
			msg = 'Loading theme \'' + theme_entries['name'] + ' by ' + theme_entries['author']
		else:
			msg = 'theme and theme_entries is set to None.'
		exit_log.info(msg)
		return
