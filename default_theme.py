# Enumeration of all the possible theme_entries keys and default values.


class DefaultTheme:
    """
    This class provides a default theme that the program can fall back on
    when improper entries are found in the specified theme file. This makes
    the program robust but can lead to unexpected appearances when theme entries
    in the specified theme are invalid. Check log [WARN] messages for invalid
    entries.
    """

    default_theme = {}

    def __init__(self):
        """
        Creates a new default theme. Other themes that fail to implement
        items properly will fall back to these specified defaults.
        Returns:

        """
        self.default_theme['name'] = "Classic"
        self.default_theme['author'] = "Unknown"
        self.default_theme['window_width_adjustment'] = 0.50
        self.default_theme['dialog_height'] = 64
        self.default_theme['button_height'] = 64
        self.default_theme['inner_border'] = 0
        self.default_theme['sleep_delay'] = 0.001
        self.default_theme['overall_opacity'] = 95
        self.default_theme['button_spacing'] = 0
        self.default_theme['icon_path'] = "/usr/share/images/bunsen/exit/dark"
        self.default_theme['button_image_cancel'] = "cancel-sm.png"
        self.default_theme['button_image_poweroff'] = "poweroff-sm.png"
        self.default_theme['button_image_reboot'] = "reboot-sm.png"
        self.default_theme['button_image_suspend'] = "sleep-sm.png"
        self.default_theme['button_image_logout'] = "logout-sm.png"
        self.default_theme['button_image_hybridsleep'] = "hibernate-sm.png"
        self.default_theme['button_image_hibernate'] = "hibernate-sm.png"
        self.default_theme['label_height'] = 20
        self.default_theme['window_background_normal'] = '#696969'
        self.default_theme['button_background_normal'] = '#696969'
        self.default_theme['button_background_prelight'] = '#838383'
        self.default_theme['text_color_normal'] = '#000000'
        self.default_theme['text_color_prelight'] = '#ffffff'
        self.default_theme['tooltip_background'] = '#696969'
        self.default_theme['tooltip_foreground'] = '#000000'
        self.default_theme['border_color'] = '#000040'
        self.default_theme['font_family'] = "monospace"
        self.default_theme['font_style'] = "bold"
        self.default_theme['font_size'] = "8"

        return

    def get_default_theme(self):
        """
        Returns the default theme dictionary
        Returns: default theme - a dictionary representing the default theme.

        """
        return self.default_theme

    def __getitem__(self, key):
        """
        This method is required. Extracts one element from the default_theme
        dictionary.
        Args:
            key: the key of the item to retrieve.

        Returns: default_theme[key] - the entry specified by key.

        """
        return self.default_theme[key]

