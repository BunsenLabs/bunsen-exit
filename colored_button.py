import gtk
import dbus_interface
import logging

exit_log = logging.getLogger('Bunsen-Exit-Log')

class ColoredButton(gtk.EventBox):
	'''
	This class implements a ColoredButton. The objective here is to
	implement a button class that will image a button (if availale)
	or create a label on one, then 
	'''

	def __init__(self, key, button_image):
		'''
		widget must be a gtk.Label
		this is not checked in this simple version
		'''
		
		self.key = key
		self.button_image = button_image
		self.label = gtk.Label(key)
		#initialize superclass EventBox
		super(ColoredButton, self).__init__()

		#get a DBusInterface instance, so we can send message out.
		self.exit_bus = dbus_interface.DbusInterface()

		#define which events should be reacted to, those constants can be found in pygtk docs
		self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
		self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
		self.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
		self.add_events(gtk.gdk.LEAVE_NOTIFY_MASK)
		#self.add_events(gtk.gdk.FOCUS_CHANGE_MASK)

		#activate focus
		self.set_can_focus(True)

		#align the "button" text in the middle of the box
		self.label.set_alignment(xalign=0.5, yalign=0.5)
		
		#colorize the button upon init
		self.changeColor(gtk.gdk.color_parse("black"))
		self.changeTextColor(gtk.gdk.color_parse("white"))

		# Add the image_label box
		box = self.image_label_box(self.button_image, self.key)
		self.add(box)
		# set events
		self.connect("button-release-event",self.clicked)
		self.connect("enter-notify-event", self.mouse_in)
		self.connect("leave-notify-event", self.mouse_out)
		self.connect("focus-in-event", self.focus_in)
		self.connect("focus-out-event", self.focus_out)
		self.show()
	def set_label(self, label):
		self.set_text(label)

	def set_text(self, text):
		self.label.set_text(text)

	def changeColor(self, color, state = gtk.STATE_NORMAL):
		self.modify_bg(state, color)
		return

	def changeTextColor(self, color, state = gtk.STATE_NORMAL):   
		self.modify_fg(gtk.STATE_NORMAL, color)
		return

	def clicked(self, widget, data=None):
		print ("Custom button data is " + widget.name)
		if widget.name == 'Cancel':
			self.destroy()
		else:
			self.send_to_dbus(widget.name)
		return

	def changeColor(self, color, state = gtk.STATE_NORMAL):
		self.modify_bg(state, color)
		return

	def changeTextColor(self, color, state = gtk.STATE_NORMAL):   
		self.modify_fg(gtk.STATE_NORMAL, color)
		return

	def focus_in(self, widget, event):
		exit_log.debug("Focus in. Highlighting button")
		widget.changeColor(gtk.gdk.color_parse("white"))
		widget.changeTextColor(gtk.gdk.color_parse("black"))
		return

	def focus_out(self, widget, event):
		exit_log.debug("Focus out. Removing button highlight")
		widget.changeColor(gtk.gdk.color_parse("black"))
		widget.changeTextColor(gtk.gdk.color_parse("white"))

	def mouse_in(self, widget, event):
		self.grab_focus()
		exit_log.debug("Focus in. Highlighting button")
		widget.changeColor(gtk.gdk.color_parse("white"))
		widget.changeTextColor(gtk.gdk.color_parse("black"))
		return

	def mouse_out(self, widget, event):
		exit_log.debug("Focus out. Removing button highlight")
		widget.changeColor(gtk.gdk.color_parse("black"))
		widget.changeTextColor(gtk.gdk.color_parse("white"))

	def destroy(self, widget=None, event=None, data=None):
		gtk.main_quit()

	def image_label_box(self, button_image, key):
		# Pack the image and the label into a box
		box = gtk.VBox()
		image = gtk.Image()
		try:
			image.set_from_file(button_image)
		except IOError:
			exit_log.warn("Unable to set button image.")
		label = gtk.Label(key)
		box.pack_start(image, False, False, 5)
		box.pack_start(label, False, False, 5)
		box.show()
		image.show()
		label.show()
		return box

	def send_to_dbus(self, dbus_msg):
		exit_log.info("Executing action " + dbus_msg)
		if dbus_msg == 'Logout':
			self.exit_bus.logout()
		else:
			self.exit_bus.send_dbus(dbus_msg)
		return
