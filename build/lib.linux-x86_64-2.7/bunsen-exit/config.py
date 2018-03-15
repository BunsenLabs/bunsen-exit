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
import os
import logging
import ConfigParser
from xdg import BaseDirectory
import collections
import default_theme
import re

exit_log = logging.getLogger('Bunsen-Exit-Log')


class Config(object):
    """ This class includes all the methods necessary to read and parse
    the config file ~/.config/bunsen-exit/bl-exitrc and any theme files listed under the
    theme subdirectory.
    """
    
    def get_config_path(self):
        """
        Determine config directory: first try the environment variable
        XDG_CONFIG_HOME according to XDG specification and as a fallback
        use ~/.config/bunsen-exit. Use /etc/bunsen-exit/bl-exitrc as a last
        resort.
        Returns: config_path - the path to bl-exitrc.
        """
        config_dir = BaseDirectory.save_config_path('bunsen-exit')
        fname = '/bl-exitrc'
        config_path = config_dir + fname
        if not os.path.exists(config_path):
            # Config file not present in $HOME so move from
            # /etc/bunsen-exit, if it exists
            src = '/etc/bunsen-exit'
            config_path = src + fname
        return config_path

    def get_theme_path(self, theme):
        """
        Use of this function requires pyxdg.
        Args: theme: the theme named in ~/.config/bunsen-exit/bl-exitrc
        Returns: theme_path - the path to the named theme.

        """
        fname = ""
        theme_dir = BaseDirectory.save_config_path('bunsen-exit')
        if not theme_dir:
            theme_dir = "/etc/bunsen-exit"
        try:
            fname = theme['rcfile']
        except KeyError:
            exit_log.warn("Theme not found. Running with defaults.")
        theme_path = theme_dir + '/themes/' + fname
        msg = 'Theme path is set to ' + theme_path
        exit_log.info(msg)
        return theme_path

    def read_config(self, config_path):
        """
        read the configuration file specified by config_path
        Args:
            config_path: the path to the configuration file, typically
            ~/.config/bunsen-exit/bl-exitrc.
        Returns:
            - a sorted dictionary representing the buttons to create in the dialog.
            - the theme to process.
        """
        specified_theme = {}
        theme = {}
        button_values = {}
        button_visibility = []
        config_file = ConfigParser.RawConfigParser()
        if config_path:
            exit_log.info('Attempting to parse ' + config_path)
            config_file.read(config_path)
            try:
                button_visibility = config_file.items('button_values')
            except ConfigParser.NoSectionError as err:
                exit_log.warn(err)
                button_values = {'Cancel': 'show', 'Logout': 'show', 'Suspend': 'show',
                                 'Hibernate': 'hide', 'Hybridsleep': 'hide',
                                 'Reboot': 'show', 'Poweroff': 'show'}
            if button_visibility:
                for item in button_visibility:
                    for x in range(0, len(item)):
                        key = item[0]
                        val = item[1]
                        button_values[key] = val
            try:
                specified_theme = config_file.items('theme')
            except ConfigParser.NoSectionError as err:
                exit_log.warn(err)
                theme['name'] = "default"
                exit_log.warn("Running with default gtk theme")
            for item in specified_theme:
                for x in range(0, len(item)):
                    key = item[0]
                    val = item[1]
                    theme[key] = val
        else:
            theme['name'] = "default"
            exit_log.warn("No config file found. Using default button_values.")
            button_values = {'Cancel': 'show', 'Logout': 'show', 'Suspend': 'show',
                             'Hibernate': 'hide', 'Hybridsleep': 'hide',
                             'Reboot': 'show', 'Poweroff': 'show'}
        sorted_buttons = collections.OrderedDict(sorted(button_values.items()))
        return sorted_buttons, theme

    def read_theme(self, theme_path):
        """

        Args:
            theme_path: the path to the specified theme

        Returns:
            a sorted dictionary containing all of the theme entries specified
            by the theme file.
        """
        theme_entries = {}
        theme = {}
        theme_file = ConfigParser.RawConfigParser()
        if theme_path:
            exit_log.info("Attempting to parse " + theme_path)
            theme_file.read(theme_path)
            try:
                theme = theme_file.items('theme')
            except ConfigParser.NoSectionError as err:
                exit_log.warn(err)
            for item in theme:
                for x in range(0, len(item)):
                    key = item[0]
                    val = item[1]
                    theme_entries[key] = val
        sorted_themes = collections.OrderedDict(sorted(theme_entries.items()))
        return sorted_themes

    def log_theme_warning(self, key, value, var_type):
        """
        This method logs theme warnings for entries that fail to parse.
        These warning can arise because of key errors, type conversion errors
        or missing or blank theme entries.
        Args:
            key: the dictionary key
            value: the value stored in dictionary[key]
            var_type: the type of variable expected.

        Returns: Nothing.

        """
        exit_log.warn("Could not parse " + key + ". Expected a(n) " + var_type + ".")
        exit_log.warn("Setting value to " + str(value) + ".")
        return

    def test_entry(self, key, value, var_type):
        """
        The method tests theme entries for valid values.
        Args:
            key: the dictionary key
            value: the value to be processed.
            var_type: the type of variable the value must be cast too.

        Returns: True | False for passed | failed tests.

        """
        if var_type == "int":
            try:
                temp = int(value)
                result = True
            except ValueError:
                self.log_theme_warning(key, value, var_type)
                result = False
        elif var_type == "float":
            try:
                temp = float(value)
                result = True
            except ValueError:
                self.log_theme_warning(key, value, var_type)
                result = False
        elif var_type == "dir":
            temp = os.path.isdir(value)
            if temp:
                result = True
            else:
                self.log_theme_warning(key, value, var_type)
                result = False
        elif var_type == "file":
            temp = os.path.exists(key)
            if temp:
                result = True
            else:
                self.log_theme_warning(key, value, var_type)
                result = False
        elif var_type == "color":
            temp = re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', value)
            if temp:
                result = True
            else:
                self.log_theme_warning(key, value, var_type)
                result = False
        return result




