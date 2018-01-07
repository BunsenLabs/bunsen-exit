#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
#
#    bl-exit: Bunsenlabs exit dialog, offering various exit options
#     via both GUI and CLI
#    Copyright (C) 2012 Philip Newborough  <corenominal@corenominal.org>
#    Copyright (C) 2016 xaos52  <xaos52@gmail.com>
#    Copyright (C) 2017 damo  <damo@bunsenlabs.org>
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
import exit_config
import exit_gtk

DISPLAY = os.environ.get('DISPLAY') is not None
LOGGING = True

exit_log = logging.getLogger('Bunsen-Exit-Log')


def get_options():
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
	args = parser.parse_args()
	return args


def log_config(button_visibility, style, theme, theme_entries):
	exit_log.debug('--------------------------------------')
	exit_log.debug('Button Values')
	exit_log.debug('--------------------------------------')
	for key in button_visibility:
		exit_log.debug(key + '\t' + button_visibility[ key ])
	exit_log.debug('\n')
	exit_log.debug('--------------------------------------')
	exit_log.debug('Style')
	exit_log.debug('--------------------------------------')
	for key in style:
		exit_log.debug(key + ' = ' + style[ key ])
	exit_log.debug('\n')
	exit_log.debug('Theme is set to ' + theme + '\n')
	exit_log.debug('--------------------------------------')
	exit_log.debug('Theme Entries')
	exit_log.debug('--------------------------------------')
	for key in theme_entries:
		exit_log.debug(key + '\t' + theme_entries[ key ])
	return

def main():
	'''
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

	The following three options determine how to handle errors in the
	program.
		-d	--dialog		Send errors to a gtk dialog. Defaults to False.
		-z	--logfile		Log files to ~/bunsen_exit.log
	'''
	args = get_options()
	if LOGGING:
		# Start the logger
		fname = "/bl_exit.log"
		exit_log = logger.setup_logging(fname)
	# Start the dbus interface
	exit_bus = dbus_interface.DbusInterface()

	action = None
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
		bl_exit_config = exit_config.Config()
		config_path = bl_exit_config.get_config_path()
		if config_path:
			if LOGGING:
				msg = 'Configuration file found at ' + config_path
				exit_log.info(msg)
		else:
			if LOGGING:
				msg = "No configuration file found. Using default gtk theme."
				exit_log.warn(msg)

		button_values, style, theme, theme_entries = bl_exit_config.read_config(config_path)
		if LOGGING:
			try:
				log_config(button_values, style, theme, theme_entries)
			except TypeError:
				exit_log.warn("No config information found to log. Moving on.")
		if not DISPLAY:
			exit_log.debug('No valid xserver found. Please use a command line option')
			sys.exit(1)
		else:
			style_path = bl_exit_config.get_style_path(style)
			style_entries = bl_exit_config.read_style(style_path)
			# Start to create the gtk interface
			bl_exit_gtk = exit_gtk.ExitGtk(button_values, exit_bus, theme, theme_entries, style_entries, style_path)
			bl_exit_gtk.main(button_values, style, theme, theme_entries)
	return


if __name__ == "__main__":
	sys.exit(main())
