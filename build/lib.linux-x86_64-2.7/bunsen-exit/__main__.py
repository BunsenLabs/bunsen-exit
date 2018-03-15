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
import sys
import logger
import logging
import argparse
import dbus_interface
import config
import gui
import default_theme
import collections
import validator

DISPLAY = os.environ.get('DISPLAY') is not None

exit_log = logging.getLogger('Bunsen-Exit-Log')


def get_options():
    """
    The command line interface's argument parser.
    :return: The arguments from the command line.
    """
    parser = argparse.ArgumentParser(description="Bunsenlabs Exit")
    parser.add_argument("-l", "--logout", help="Log out",
                        action="store_true")
    parser.add_argument("-s", "--suspend", help="Suspend",
                        action="store_true")
    parser.add_argument("-i", "--hibernate", help="Hibernate",
                        action="store_true")
    parser.add_argument("-y", "--hybridsleep", help="Hybrid sleep",
                        action="store_true")
    parser.add_argument("-b", "--reboot", help="Reboot",
                        action="store_true")
    parser.add_argument("-p", "--poweroff", help="Power off",
                        action="store_true")
    parser.add_argument("-f", "--logfile", help="The file to log too",
                        action="store", dest="logfile", default="None")
    parser.add_argument("-z", "--loglevel", help="Verbosity of the logging, Info, Warn, or Debug",
                        action="store", dest="loglevel", default="None")
    print (parser.parse_args())
    args = parser.parse_args()
    return args


def log_config(button_values, theme, theme_entries):
    """
    This function logs the contents of the config file as debug values.
    These logs should serve to show all inputs from both the initial config
    file and the theme_entries from the theme file. This may prove of use in
    diagnosing problems.
    :param button_values: The dictionary of button values. Keys for button
    values are also the button names and will be formatted into proper dbus
    messages later when a button is clicked.
    :param theme: the specified theme from ~/.config/bunsen-exit/bl-exitrc.
    :param theme_entries: the dictionary of theme_entries.
    :return:
    """
    theme_entries = collections.OrderedDict(sorted(theme_entries.items()))
    exit_log.debug('--------------------------------------')
    exit_log.debug('Button Values')
    exit_log.debug('--------------------------------------')
    for key in button_values:
        exit_log.debug(key + '\t' + button_values[key])
    exit_log.debug('\n')
    exit_log.debug('--------------------------------------')
    exit_log.debug('Theme')
    exit_log.debug('--------------------------------------')
    for key in theme:
        exit_log.debug(key + ' = ' + theme[key])
    exit_log.debug('\n')
    exit_log.debug('--------------------------------------')
    exit_log.debug('Theme Entries')
    exit_log.debug('--------------------------------------')
    for key in theme_entries:
        exit_log.debug(key + '\t' + str(theme_entries[key]))
    exit_log.debug("\n")
    return


def main():
    """
    The script works both in a graphical and a non-graphical environment.

    In a graphical environment, the Window is only shown when
    the script is launched without arguments.

    When  the script is launched in a non-graphical environment the requested
    action should be one of the accepted arguments and the action is executed
    without asking for confirmation - as if the script was launched from the
    command line.

    In a non-graphical environment, one of the accepted actions must be
    specified as an argument.
    USAGE:
        -l	--logout		Logs the user out.
        -s	--suspend		Suspend the system.
        -i	--hibernate		Hibernate the system.
        -y	--hybridsleep	Hybrid sleep the system.
        -b	--reboot		Reboot the system.
        -p	--poweroff		Power off the system.

        -f	--logfile		Which file to log too, e.g. ~/gl-exit.log or ~/.xsession-errors
        -z  --loglevel      The default logging level can be one of:
                            None - Logging turned off or sent to /dev/null
                            Info - only log [INFO] messages.
                            Warn - log [WARN] and [INFO] messages.
                            Debug - log all messages.
    """
    args = get_options()
    loglevel = args.loglevel
    # Start the logger
    fname = args.logfile
    exit_log = logger.setup_logging(fname, loglevel)

    # Start the dbus interface
    exit_bus = dbus_interface.DbusInterface()

    if args.logout:
        exit_bus.logout()
    elif args.suspend:
        action = "Suspend"
        exit_bus.send_dbus(action)
    elif args.hibernate:
        action = "Hibernate"
        exit_bus.send_dbus(action)
    elif args.hybridsleep:
        action = "HybridSleep"
        exit_bus.send_dbus(action)
    elif args.reboot:
        action = "Reboot"
        exit_bus.send_dbus(action)
    elif args.poweroff:
        action = "PowerOff"
        exit_bus.send_dbus(action)
    else:
        if not DISPLAY:
            exit_log.debug('No valid xserver found. Please use a command line option')
            sys.exit(1)

        bl_exit_config = config.Config()
        config_path = bl_exit_config.get_config_path()
        if config_path:
            msg = 'Configuration file found at ' + config_path
            exit_log.info(msg)
        else:
            msg = "No configuration file found. Using default gtk theme."
        button_values, theme = bl_exit_config.read_config(config_path)
        if theme['name'] == "default":
            theme_entries = None
        elif theme['name'] == "classic":
            theme_entries = default_theme.DefaultTheme()
        else:
            theme_path = bl_exit_config.get_theme_path(theme)
            theme_entries = bl_exit_config.read_theme(theme_path)
            entry_validator = validator.Validator()
            # Check for missing keys or empty values
            theme_entries = entry_validator.validate_keys(theme_entries)
            log_config(button_values, theme, theme_entries)
        # Start to create the gtk interface
        bl_exit_gtk = gui.Gui(button_values, exit_bus, theme, theme_entries)
        # Pass control over to exit_gtk.
        bl_exit_gtk.main()
        return


if __name__ == "__main__":
    sys.exit(main())
