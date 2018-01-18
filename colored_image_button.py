import gtk
import pango
import dbus_interface
import logging

exit_log = logging.getLogger('Bunsen-Exit-Log')

class ColoredImageButton(gtk.EventBox):
	'''
	This class implements a ColoredButton. The objective here is to
	implement a button class that will image a button (if availale)
	or create a label on one, then 
	'''

	def __init__(self, key, button_image, theme_entries, num_buttons, dialog_width):
		'''
		widget must be a gtk.Label
		this is not checked in this simple version
		'''
		self.key = key
		self.button_image = button_image
		self.theme_entries = theme_entries
		self.attr = pango.AttrList()
		try:
			self.button_height = int(self.theme_entries['button_height']) + 16
		except:
			exit_log.warn('Unable to parse button_height. Setting to 60')
			self.button_height = 60
		try:
			self.button_spacing = int(self.theme_entries['button_spacing'])
		except:
			exit_log.warn("Unable to parse button_spacing. Setting to 2")
			self.button_spacing = 2
		self.button_width = (dialog_width / num_buttons) - self.button_spacing
		exit_log.debug("Setting button width to " + str(self.button_width))
		#initialize superclass EventBox
		super(ColoredImageButton, self).__init__()

		#get a DBusInterface instance, so we can send message out.
		self.exit_bus = dbus_interface.DbusInterface()

		#define which events should be reacted to, those constants can be found in pygtk docs
		self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
		self.add_events(gtk.gdk.LEAVE_NOTIFY_MASK)

		#activate focus
		self.set_can_focus(True)
		fg_color= self.theme_entries['text_color_normal']
		label_markup = '<span foreground="' + fg_color + '">' + self.key + '</span>'
		# create the label
		self.label = gtk.Label()
		self.label.set_use_markup(True)
		self.label.set_label(label_markup)
		self.label.modify_font(pango.FontDescription("FreeSans 12"))
		
		
		#colorize the button upon init
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_normal']))
		

		# Add the image_label box
		box = self.image_label_box(self.button_image, self.key, self.label)
		# We have to add a little to height to account for the height of the labels.
		box.set_size_request(self.button_width, self.button_height)
		
		self.add(box)
		# set events
		self.connect("button-release-event",self.clicked)
		self.connect("enter-notify-event", self.mouse_in)
		self.connect("leave-notify-event", self.mouse_out)
		self.connect("focus-in-event", self.focus_in)
		self.connect("focus-out-event", self.focus_out)

	def clicked(self, widget, data=None):
		if widget.name == 'Cancel':
			self.destroy()
		else:
			self.send_to_dbus(widget.name)
		return

	def focus_in(self, widget, event):
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_prelight']))
		fg_color = self.theme_entries['text_color_prelight']
		label_markup = '<span foreground="' + fg_color + '">' + self.key + '</span>'
		self.label.set_label(label_markup)
		self.show_all()
		return

	def focus_out(self, widget, event):
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_normal']))
		fg_color= self.theme_entries['text_color_normal']
		label_markup = '<span foreground="' + fg_color + '">' + self.key + '</span>'
		self.label.set_label(label_markup)
		self.show_all()

	def mouse_in(self, widget, event):
		self.grab_focus()
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_prelight']))
		fg_color = self.theme_entries['text_color_prelight']
		label_markup = '<span foreground="' + fg_color + '">' + self.key + '</span>'
		self.label.set_label(label_markup)
		return

	def mouse_out(self, widget, event):
		self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_normal']))
		fg_color= self.theme_entries['text_color_normal']
		label_markup = '<span foreground="' + fg_color + '">' + self.key + '</span>'
		self.label.set_label(label_markup)
		self.show_all()

	def destroy(self, widget=None, event=None, data=None):
		gtk.main_quit()

	def image_label_box(self, button_image, key, label):
		# Pack the image and the label into a box
		box = gtk.VBox()
		image = gtk.Image()
		try:
			image.set_from_file(button_image)
		except IOError:
			exit_log.warn("Unable to set button image.")
		box.pack_start(image, False, False, 0)
		box.pack_start(label, False, False, 0)
		return box

	def send_to_dbus(self, dbus_msg):
		exit_log.info("Executing action " + dbus_msg)
		if dbus_msg == 'Logout':
			self.exit_bus.logout()
		else:
			self.exit_bus.send_dbus(dbus_msg)
		return
