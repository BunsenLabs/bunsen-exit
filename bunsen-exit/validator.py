import logging
import default_theme
import gtk
import os

exit_log = logging.getLogger('Bunsen-Exit-Log')


class Validator:
    """
    The Validator Class validates theme_entries from the specified theme file.
    It can check for ints, floats, valid colors, if files or directories are present, and
    can also check for missing keys or empty configuration entries.
    """
    def __init__(self):
        self.default = default_theme.DefaultTheme()

    def parse_int(self, key, config_value):
        try:
            config_value = int(config_value)
        except ValueError:
            exit_log.warn("The value for " + key + " is not an int.")
            exit_log.warn("Setting value to a default of " + str(self.default[key]))
            config_value = int(self.default[key])
        return config_value

    def parse_float(self, key, config_value):
        try:
            config_value = float(config_value)
        except ValueError:
            exit_log.warn("The value for " + key + " is not a float.")
            exit_log.warn("Setting value to a default of " + str(self.default[key]))
            config_value = float(self.default[key])
        return config_value

    def parse_color(self, key, config_value):
        try:
            config_value = gtk.gdk.color_parse(config_value)
        except ValueError:
            exit_log.warn("The value for " + key + " is not a valid color.")
            exit_log.warn("Please use six digit hex colors, e.g. #000000.")
            exit_log.warn("Setting value to a default of " + str(self.default[key]))
            config_value = gtk.gdk.color_parse(self.default[key])
        return config_value

    def is_dir(self, key, config_value):
        try:
            os.path.isdir(config_value)
        except IOError:
            exit_log.warn("The entry " + config_value + " is not a valid directory")
            exit_log.warn("Setting value to a default of " + str(self.default[key]))
            config_value = self.default[key]
        return config_value

    def validate_keys(self, theme_entries):
        """
        This method tests each entry in the dictionary theme_entries, which is
        created when reading in a theme. It tests for valid keys and empty entries
        This allows for testing if proper keys and values are present in the config file.
        This method does not check for proper type casting.
        Args:
            theme_entries: the dictionary to validate.

        Returns: theme_entries as a clean dictionary.

        """
        theme_defaults = default_theme.DefaultTheme()
        default_dict = theme_defaults.get_default_theme()
        for key, value in default_dict.iteritems():
            if key not in theme_entries:
                exit_log.warn("<KEY ERROR>: " + key + " does not exist in config file.")
                exit_log.warn("Setting key[" + key + "] to default value " + str(value) + ".")
                theme_entries[key] = value
            if theme_entries[key] == "" or theme_entries[key] is None:
                # Value does not exist so plug in a default
                exit_log.warn("Value does not exist for key " + key + ".")
                exit_log.warn("Setting default to " + str(value) + ".")
                theme_entries[key] = str(value)
        return theme_entries
