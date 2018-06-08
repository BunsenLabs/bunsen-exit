#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#    bl-exit: Bunsenlabs exit dialog, offering various exit options
#     via both GUI and CLI
#    Copyright (C) 2012 Philip Newborough  <corenominal@corenominal.org>
#    Copyright (C) 2016 xaos52  <xaos52@gmail.com>
#    Copyright (C) 2017 damo  <damo@bunsenlabs.org>
#    Copyright (C) 2018 tknomanzr <webradley9929@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
                msg = "<KEY ERROR>: " + key + " does not exist in config file."
                exit_log.warn(msg)
                msg = "Setting key [" + key + "] to default value " + str(value) + "."
                exit_log.warn(msg)
                theme_entries[key] = value
            if theme_entries[key] == "" or theme_entries[key] is None:
                # Value does not exist so plug in a default
                msg = "Value does not exist for key " + key + "."
                exit_log.warn(msg)
                msg = "Setting default to " + str(value) + "."
                exit_log.warn(msg)
                theme_entries[key] = str(value)
        return theme_entries
