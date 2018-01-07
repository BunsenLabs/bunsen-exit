import pygtk
pygtk.require('2.0')
import gtk
import logging
import collections
import colored_button

exit_log = logging.getLogger('Bunsen-Exit-Log')


class ExitGtk:
	style_entries = [ ]
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

	def __init__(self, button_values, exit_bus, theme, theme_entries, style_entries, style_path):
		self.style_entries = style_entries
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
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
				self.add_buttons(key, theme_entries, button_box, style_entries)
		self.window.add(button_box)
		# Set the style
		if style_path:
			self.set_style(style_path)
		self.window.show_all()
		return

	def main(self, button_visibility, style, theme, theme_entries):
		gtk.main()


	def query_tooltip_custom_cb(self, widget, x, y, keyboard_tip, tooltip, style_entries):
		if 'NORMAL' in style_entries:
			color = gtk.gdk.color_parse(style_entries[ 'NORMAL' ])
			window = widget.get_tooltip_window()
			window.modify_bg(gtk.STATE_NORMAL, color)
		return True

	def add_buttons(self, key, theme_entries, button_box, style_entries):
		# iconpath refers to a theme_entry in bl-exitrc.
		# It needs to refer to  a valid path. Checks for path exists
		# and points to an image need to be added. 
		if 'iconpath' in theme_entries:
			icon_path = theme_entries[ 'iconpath' ]
			image_key = 'buttonimage' + key.lower()
			button_image = icon_path + "/" + theme_entries[ image_key ]
			exit_log.debug("Loading theme entry " + key + " from " + button_image)
			self.color_button = colored_button.ColoredButton(key, button_image)
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
		tooltip_window = gtk.Window(gtk.WINDOW_POPUP)
		tooltip_button = gtk.Label(key)
		tooltip_window.add(tooltip_button)
		tooltip_button.show()
		self.color_button.set_tooltip_window(tooltip_window)
		self.color_button.connect("query-tooltip", self.query_tooltip_custom_cb, style_entries)
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

	def set_style(self, style_path):
		try:
			gtk.rc_parse(style_path)
			settings = gtk.settings_get_for_screen(self.window.get_screen())
			gtk.rc_reset_styles(settings)
		except IOError as err:
			exit_log.debug(err)
			pass
		return
