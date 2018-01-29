import os
import logging
import ConfigParser
from xdg import BaseDirectory
import collections
exit_log = logging.getLogger('Bunsen-Exit-Log')


class Config(object):

	def __init__(self):
		return

	def error_message(self, config_dir, src):
		msg += "\n" + config_dir + " does not exist.\n"
		exit_log.warn(msg)
		return

	def get_config_path(self):
		"""Determine config directory: first try the environment variable
		XDG_CONFIG_HOME according to XDG specification and as a fallback
		use ~/.config/bunsen-exit. Use /etc/bunsen-exit/bl-exitrc as a last
		resort."""
		config_dir = BaseDirectory.save_config_path('bunsen-exit')
		fname = '/bl-exitrc'
		config_path = config_dir + fname
		if not os.path.exists(config_path):
			# Config file not present in $HOME so move from
			# /etc/bunsen-exit, if it exists
			src = '/etc/bunsen-exit/'
			config_path = src + fname
			self.error_message(config_dir, src)
			if not os.path.exists(config_path):
				src = '/usr/share/bunsen/skel/.config/bl-exit/'
				if not os.path.exists(config_path):
					config_path = None
					self.error_message(config_dir, src)
		return config_path

	def error_message(self, config_dir, src):
		msg = "\n" + config_dir + " does not exist.\n"
		exit_log.warn(msg)
		return

	def get_style_path(self, style):
		fname = ""
		style_dir = BaseDirectory.save_config_path('bunsen-exit')
		try:
			fname = style[ 'rcfile' ]
		except KeyError:
				exit_log.warn("Style not found. Running with defaults.")
		style_path = style_dir + '/styles/' + fname
		msg = 'Style path is set to ' + style_path
		exit_log.info(msg)
		return style_path

	def read_config(self, config_path):
		theme = {}
		theme_entries = {}
		button_values = {}
		button_visibility = []
		style = {}
		config_file = ConfigParser.RawConfigParser()
		if config_path:
			exit_log.info('Attempting to parse ' + config_path)
			config_file.read(config_path)
			try:
				button_visibility = config_file.items('button_values')
			except ConfigParser.NoSectionError as err:
				exit_log.warn(err)
			for item in button_visibility:
				for x in range(0, len(item)):
					key = item[ 0 ]
					val = item[ 1 ]
					button_values[ key ] = val
			style_entries = config_file.items('style')
			for item in style_entries:
				for x in range(0, len(item)):
					key = item[ 0 ]
					val = item[ 1 ]
					style[ key ] = val
			theme = config_file.get('theme', 'theme')
			theme_list = config_file.items(theme)
			for item in theme_list:
				for x in range(0, len(item)):
					key = item[ 0 ]
					val = item[ 1 ]
					theme_entries[ key ] = val
		else:
			exit_log.warn("No config file found. Using defaults.")
			button_values = {'Cancel':'show', 'Logout':'show', 'Suspend':'show',
									'Hibernate':'hide', 'Hybridsleep':'hide',
									'Reboot':'show', 'Poweroff':'show'}
			theme = "default"
		sorted_buttons = collections.OrderedDict(sorted(button_values.items()))
		return sorted_buttons, style, theme, theme_entries

