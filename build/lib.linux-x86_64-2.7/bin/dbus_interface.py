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
import subprocess
import dbus
import logging

exit_log = logging.getLogger('Exit-Log')


class DbusInterface(object):
    """
    This class is responsible for dbus actions. It can setup a dbus connection
    and send a properly formatted dbus message out to dbus.
    Usage: Setup a dbus connection before attempting to send a dbus message.
    """

    def __init__(self):
        """
        Create a new empty dbus interface.
        """
        self.dbus_iface = None

    def setup_dbus_connection(self):
        """
        Setup the dbus connection.
        """
        try:
            bus = dbus.SystemBus()
            dbus_object = bus.get_object('org.freedesktop.login1',
                                         '/org/freedesktop/login1')
            self.dbus_iface = dbus.Interface(dbus_object,
                                             'org.freedesktop.login1.Manager')
        except bus.DBusException as err:
            exit_log.info(err)

    def send_dbus(self, action):
        """
        Sends a properly formatted dbus message out to dbus.
        Args:
            action: the action to perform.

        Returns:

        """
        print("do_action: {}".format(action))
        try:
            if self.dbus_iface is None:
                self.setup_dbus_connection()
            if action[ :3 ] == "Can":
                command = "self.dbus_iface.{}()".format(action)
            else:
                command = "self.dbus_iface.{}(['True'])".format(action)
            response = eval(command)
            return str(response)
        except dbus.DBusException as err:
            exit_log.info(err)

    def logout(self):
        """
        Dbus does not handle logout commands, so those need to be handled separately here.
        """
        try:
            subprocess.check_output(["openbox", "--exit"])
        except subprocess.CalledProcessError as err:
            pass
        try:
            subprocess.check_output(["bspc", "quit"])
        except subprocess.CalledProcessError as err:
            pass
        exit_log.debug("Could not log out of Openbox or bspwm.")
        exit_log.debug("Trying to kill the Window Manager in a more generic way")
        try:
            subprocess.check_output(["killall `wmctrl -m | awk '/Name/ {print tolower($2)}'`"])
        except subprocess.CalledProcessError  as err:
            exit_log.debug("Cannot log out of window manager.")
            exit_log.debug("Please raise an issue on git or on the Bunsenlabs forums with the")
            exit_log.debug("Window manager you are using, so we can add its logout command to this script.")
        return
