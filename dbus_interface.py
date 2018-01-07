import subprocess
import dbus
import logging

exit_log = logging.getLogger('Exit-Log')


class DbusInterface(object):

    def __init__(self):
        self.dbus_iface = None

    def setup_dbus_connection(self):
        try:
            bus = dbus.SystemBus()
            dbus_object = bus.get_object('org.freedesktop.login1',
                                         '/org/freedesktop/login1')
            self.dbus_iface = dbus.Interface(dbus_object,
                                             'org.freedesktop.login1.Manager')
        except bus.DBusException as err:
            exit_log.info(err)

    def send_dbus(self, action):
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
        try:
            subprocess.check_output([ "openbox", "--exit" ])
        except subprocess.CalledProcessError as err:
            exit_log.info(err)
