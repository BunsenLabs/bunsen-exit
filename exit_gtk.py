import pygtk
pygtk.require('2.0')
import gtk
import gobject
import logging
import collections
from colored_image_button import ColoredImageButton
import struct
from time import sleep
import dbus_interface
exit_log = logging.getLogger('Bunsen-Exit-Log')


class ExitGtk:
	color_button = None
	window = None
	#get a DBusInterface instance, so we can send message out.
	exit_bus = dbus_interface.DbusInterface()

	def _key_press_event(self, widget, event):
		keyval = event.keyval
		keyval_name = gtk.gdk.keyval_name(keyval)
		state = event.state
		alt = (state & gtk.gdk.MOD1_MASK)
		# Cancel shortcut
		if alt and keyval_name == 'l':
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
		# Attributes
		self.theme_entries = theme_entries
		self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
		try:
			self.dialog_height = int(self.theme_entries['dialog_height'])
		except:
			exit_log.warn("dialog_height not set. Settins a default of 64 pixels.")
			self.dialog_height = 64
		# Get the screen width under the cursor
		screen_width = 800 # fallback width
		try:
			display=gtk.gdk.Display(gtk.gdk.get_display())
			screen, x, y, flags=display.get_pointer()
			curmon = screen.get_monitor_at_point(x, y)
			_, _, screen_width, _ = screen.get_monitor_geometry(curmon)
		except:
			exit_log.info('Error constructing UI. Not running under X')
		finally:
			del x, y, display, screen, curmon
		exit_log.debug("Detected screen_width is " + str(screen_width))
		try:
			self.width_adjustment = float(self.theme_entries['window_width_adjustment'])
		except:
			exit_log.warn("window_width_adjustment not a float. Please check config. Defaulting to 0.5")
		if self.width_adjustment > 0:
			self.dialog_width = int( screen_width * self.width_adjustment)
		if self.dialog_width > screen_width:
			self.dialog_width = screen_width
		exit_log.debug("Dialog width is set to " + str(self.dialog_width))
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
		self.button_box = gtk.HButtonBox()
		self.button_box.set_layout(gtk.BUTTONBOX_SPREAD)
		try:
			self.inner_border = int(self.theme_entries['inner_border'])
		except:
			exit_log.warn("Could not parse value for inner_border. Expected an int. Check your config.")
			self.inner_border = 4
		self.button_box.set_size_request(self.dialog_width - self.inner_border, self.dialog_height- self.inner_border)
		try:
			self.button_box.set_spacing(int(self.theme_entries['button_spacing']))
		except:
			exit_log.warn("button_spacing is not set or is not an int. Please check your configuration. Expected an int.")
		# Get a count of the nuber of buttons to be shown
		num_buttons = 0
		for key, value in button_values.iteritems():
			if value == "show":
				num_buttons += 1
		# Now build the array of buttons
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
				self.add_buttons(key, self.theme_entries, self.button_box, num_buttons, self.dialog_width)
				gobject.type_register(ColoredImageButton)
		try:
			self.window.set_size_request(self.dialog_width, int(self.dialog_height))
		except:
			exit_log.warn("Cannot set window to the size requested.")
		self.window.add(self.button_box)
		self.window.set_opacity(0)
		self.window.show_all()
		try:
			self.overall_opacity = int(self.theme_entries['overall_opacity'])
		except:
			exit_log.warn("Problem with overall_opacity. Please check your config. Expected an int.")
			self.overall_opacity = 100
		try:
			self.sleep_delay = float(self.theme_entries['sleep_delay'])
		except:
			exit_log.warn("Problem with sleep_delay. Please check your config. Expected a float.")
		for i in range(1, self.overall_opacity):
			sleep(self.sleep_delay)
			while gtk.events_pending():
				gtk.main_iteration(False)
				self.window.set_opacity(float(i)/100.0)
		self.window.show_all()
		return

	def main(self, button_visibility, style, theme, theme_entries):
		gtk.main()


	def query_tooltip_custom_cb(self, widget, x, y, keyboard_tip, tooltip, key, tooltip_label, tooltip_window):
		fg_color = self.theme_entries['text_color_normal']
		label_markup = '<span foreground="' + fg_color + '">' + key + '</span>'
		tooltip_label.set_markup(label_markup)
		tooltip_label.show()
		return True

	def add_buttons(self, key, theme_entries, button_box, num_buttons, dialog_width):
		# iconpath refers to a theme_entry in bl-exitrc.
		# It needs to refer to  a valid path. Checks for path exists
		# and points to an image need to be added. 
		if 'iconpath' in self.theme_entries:
			icon_path = self.theme_entries[ 'iconpath' ]
			image_key = 'buttonimage' + key.lower()
			button_image = icon_path + "/" + self.theme_entries[ image_key ]
			exit_log.debug("Loading theme entry " + key + " from " + button_image)
			self.color_button = ColoredImageButton(key, button_image, self.theme_entries, num_buttons, dialog_width)
			self.color_button.set_name(key)
			button_box.pack_start(self.color_button, True, True, 0)
		else:
			exit_log.warn("Icon path not found. Defaulting to button labels.")
			self.color_button = gtk.Button()
			self.color_button.set_name(key)
			self.color_button.set_relief(gtk.RELIEF_NONE)
			self.color_button.set_label(key)
			button_box.pack_start(self.button, True, True, 0)
		# Add custom tooltips
		tooltip_window = gtk.Window(gtk.WINDOW_POPUP)
		tooltip_label = gtk.Label()
		tooltip_label.set_use_markup(True)
		bg_color = gtk.gdk.color_parse(self.theme_entries['window_background_normal'])
		tooltip_window.modify_bg(gtk.STATE_NORMAL, bg_color)
		self.color_button.connect("query-tooltip", self.query_tooltip_custom_cb, key, tooltip_label, tooltip_window)
		self.color_button.set_tooltip_window(tooltip_window)
		tooltip_window.add(tooltip_label)
		# Show the custom button
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

	def send_to_dbus(self, dbus_msg):
		exit_log.info("Executing action " + dbus_msg)
		if dbus_msg == 'Logout':
			self.exit_bus.logout()
		else:
			self.exit_bus.send_dbus(dbus_msg)
		return
