import os
import logging
import ConfigParser
from xdg import BaseDirectory
import collections
import default_theme
exit_log = logging.getLogger('Bunsen-Exit-Log')


class Config(object):

	def __init__(self):
		self.default_theme = default_theme.Default_Theme()
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

	def get_theme_path(self, theme):
		if not theme['name'] == "default":
			fname = ""
			theme_dir = BaseDirectory.save_config_path('bunsen-exit')
			try:
				fname = theme[ 'rcfile' ]
			except KeyError:
				exit_log.warn("Theme not found. Running with defaults.")
			theme_path = theme_dir + '/themes/' + fname
			msg = 'Theme path is set to ' + theme_path
			exit_log.info(msg)
			return theme_path

	def read_config(self, config_path):
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
			for item in button_visibility:
				for x in range(0, len(item)):
					key = item[ 0 ]
					val = item[ 1 ]
					button_values[ key ] = val
			specified_theme = config_file.items('theme')
			for item in specified_theme:
				for x in range(0, len(item)):
					key = item[ 0 ]
					val = item[ 1 ]
					theme[ key ] = val
		else:
			exit_log.warn("No config file found. Using defaults.")
			button_values = {'Cancel':'show', 'Logout':'show', 'Suspend':'show',
									'Hibernate':'hide', 'Hybridsleep':'hide',
									'Reboot':'show', 'Poweroff':'show'}
			theme['name'] = "default"
		sorted_buttons = collections.OrderedDict(sorted(button_values.items()))
		return sorted_buttons, theme

	def read_theme(self, theme_path):
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

	def validate_theme_entries(self, theme, theme_entries):
		for key, value in self.default_theme__members__.items():
			for theme_entry, theme_value in theme_entries:
				if not key in theme_entries:
					exit_log.warn("<key error>: key " + key "does not exist in config file.")
					exit_log.warn("setting key " + key + "to default value " + value + ".")
					theme_entries[key] = value
				elif theme_entries[key] == "" or theme_entries[key] == None:
						# Value does not exist so plug in a default
						exit_log.warn("Value does not exist for key " + key + ".")
						exit_log.warn("Setting value to " + value + ".")
						theme_entries[key] = value
				# Test for special conditions
				elif theme_entry == "window_width_adjustment":
					result = testDouble(theme_value)
					if not result:
						exit_log.warn("Could not parse " + theme_entry + ". Expected a double.")
						exit_log.warn("Setting value to " + value + ".")
						theme_entries[theme_entry] = value
				elif theme_entry == "dialog_height" \
					or theme_entry == "button_height" \
					or theme_entry == "inner_border" \
					or theme_entry == "overall_opacity" \
					or theme_entry == "button_spacing":
						result = testInt(theme_value)
						if not result:
							exit_log.warn("Could not parse " + theme_entry + ". Expected an int.")
							exit_log.warn("Setting value to " + value + ".")
							
		return
