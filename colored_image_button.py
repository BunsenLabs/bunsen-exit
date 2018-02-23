import gtk
import pango
import dbus_interface
import logging

exit_log = logging.getLogger('Bunsen-Exit-Log')


class ColoredImageButton(gtk.EventBox):
    """
    This class implements a ColoredImageButton. A ColoredImgeButton in this case
    is an image and a label packed into a Vbox. This box is then packed into
    an event box so that keyboard events can also be mapped.
    """
    def __init__(self, key, button_image, theme_entries, num_buttons, dialog_width, show_labels, button_height):
        """
        Creates the ColoredImageButton
        :param key: - the key in this case is the button label.
        :param button_image: the specified image for the button. If button image
        cannot be found, a gtk.STOCK_ERROR_DIALOG image will be placed instead.
        :param theme_entries: the dictionary of theme_entries.
        :param num_buttons: the number of buttons. Used to calculate button widths.
        :param dialog_width: the width of the dialog. Button width is basically
        (dialog_width / num_buttons) - button_spacing.
        :param show_labels: whether to show/hide the labels.
        :param button_height: the height of the buttons.
        """
        self.key = key
        self.button_image = button_image
        self.theme_entries = theme_entries
        self.attr = pango.AttrList()
        self.show_labels = show_labels
        self.button_height = button_height
        self.button_spacing = int(self.theme_entries['button_spacing'])
        # Maps button keys to accelerators.
        if self.key == "Cancel":
            self.accel = "Cancel"
        elif self.key == "Logout":
            self.accel = "_Logout"
        elif self.key == "PowerOff":
            self.accel = "_Poweroff"
        elif self.key == "Suspend":
            self.accel = "_Suspend"
        elif self.key == "Hibernate":
            self.accel = "H_ibernate"
        elif self.key == "HybridSleep":
            self.accel = "_HybridSleep"
        elif self.key == "Reboot":
            self.accel = "Re_boot"
        self.button_width = (dialog_width / num_buttons) - self.button_spacing
        exit_log.debug("Setting button width to " + str(self.button_width))
        # initialize superclass EventBox
        super(ColoredImageButton, self).__init__()

        # get a DBusInterface instance, so we can send message out.
        self.exit_bus = dbus_interface.DbusInterface()

        # define which events should be reacted to, those constants can be found in pygtk docs
        self.add_events(gtk.gdk.BUTTON_RELEASE_MASK)
        self.add_events(gtk.gdk.BUTTON_PRESS_MASK)
        self.add_events(gtk.gdk.ENTER_NOTIFY_MASK)
        self.add_events(gtk.gdk.LEAVE_NOTIFY_MASK)
        self.add_events(gtk.gdk.KEY_PRESS)
        # activate focus
        self.set_can_focus(True)
        if self.show_labels:
            # create the label
            self.label = gtk.Label()
            self.label.modify_font(pango.FontDescription("Sans 12"))
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['text_color_normal']))
            self.label.set_use_underline(True)
            self.label.set_text_with_mnemonic(self.accel)
        else:
            self.label = None
        # colorize the button upon init
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_normal']))
        # Add the image_label box
        box = self.image_label_box(self.button_image, self.label)

        # We have to add a little to height to account for the height of the labels.
        box.set_size_request(self.button_width, self.button_height)
        self.add(box)
        # set events
        self.connect("button-release-event", self.clicked)
        self.connect("enter-notify-event", self.mouse_in)
        self.connect("leave-notify-event", self.mouse_out)
        self.connect("focus-in-event", self.focus_in)
        self.connect("focus-out-event", self.focus_out)
        self.connect("key-press-event", self.key_pressed)

    def key_pressed(self, widget, event, data=None):
        """
        Capture a keypress event and handle it.
        Args:
        widget: the widget that fired the event
        event: the event
        data: optional data

        Returns:
    """
        keyval = event.keyval
        keyval_name = gtk.gdk.keyval_name(keyval)
        if keyval_name == "Return":
            if widget.name == 'Cancel':
                self.destroy()
            else:
                self.send_to_dbus(widget.name)
        return

    def clicked(self, widget, data=None):
        """
        Captures a button press event
        Args:
        widget: the widget the fire the event
        data: Optional data

        Returns:

        """
        if widget.name == 'Cancel':
            self.destroy()
        else:
            self.send_to_dbus(widget.name)
        return

    def focus_in(self, widget, event):
        """
        The widget has received keyboard focus
        Args:
        widget: the widget
        event: the event
        Returns:

        """
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_prelight']))
        if self.show_labels:
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['text_color_prelight']))
            self.label.set_text_with_mnemonic(self.accel)
        self.show_all()
        return

    def focus_out(self, widget, event):
        """
        The widget has lost keyboard focus
        Args:
        widget: the widget that received the event
        event: the event
        """
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_normal']))
        if self.show_labels:
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['text_color_normal']))
            self.label.set_text_with_mnemonic(self.accel)
        self.show_all()

    def mouse_in(self, widget, event):
        """
        The widget has received mouse focus
        Args:
        widget: the widget that received the event
        event: the event

        Returns:

        """
        self.grab_focus()
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_prelight']))
        if self.show_labels:
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['text_color_prelight']))
            self.label.set_text_with_mnemonic(self.accel)
        self.show_all()
        return

    def mouse_out(self, widget, event):
        """
        The widget has lost mouse focus
        Args:
        widget: the widget that received the event
        event: the event.
        """
        self.modify_bg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['button_background_normal']))
        if self.show_labels:
            self.label.modify_fg(gtk.STATE_NORMAL, gtk.gdk.color_parse(self.theme_entries['text_color_normal']))
            self.label.set_text_with_mnemonic(self.accel)
        self.show_all()

    def destroy(self, widget=None, event=None, data=None):
        """
        Destroys an object
        Args:
        widget: the widget to destroy
        event: the event
        data: optional data
        """
        gtk.main_quit()

    def image_label_box(self, button_image, label):
        """
        Packs the specified image and label into a Vbox and returns it.
        Args:
        button_image: the path to the button's image. If this fails, a
        gtk.STOCK_DIALOG_ERROR image will be placed instead.
        label: the label is actually the button key modified with an accelerator.

        Returns: the box with the image and label packed into it.

        """
        # Pack the image and the label into a box
        box = gtk.VBox()
        image = gtk.Image()
        if button_image == gtk.STOCK_DIALOG_ERROR:
            # Need to set a stock icon for the button image if image cannot be set.
            image.set_from_stock(button_image, gtk.ICON_SIZE_DIALOG)
            exit_log.warn("Unable to set button image. Using stock icon.")
            exit_log.warn("Setting stock icon to " + gtk.STOCK_DIALOG_ERROR)
        else:
            image.set_from_file(button_image)
        box.pack_start(image, False, False, 0)
        if self.label:
            box.pack_start(label, False, False, 0)
        return box

    def send_to_dbus(self, dbus_msg):
        """
        Once a button or shortcut key is pressed, send a properly formatted dbus
        message out.
        Args:
        dbus_msg: The dbus message to send,

        Returns:

        """
        exit_log.info("Executing action " + dbus_msg)
        if dbus_msg == 'Logout':
            self.exit_bus.logout()
        else:
            self.exit_bus.send_dbus(dbus_msg)
        return
