import os
import logging
import ConfigParser
from xdg import BaseDirectory
import collections
import default_theme
import re
exit_log = logging.getLogger('Bunsen-Exit-Log')


class Config(object):

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
			src = '/etc/bunsen-exit'
			config_path = src + fname
			if not os.path.exists(config_path):
				src = '/usr/share/bunsen/skel/.config/bunsen-exit'
				config_path = src + fname
				if not os.path.exists(config_path):
					config_path = None
		return config_path

	def get_theme_path(self, theme):
		fname = ""
		theme_dir = BaseDirectory.save_config_path('bunsen-exit')
		if not theme_dir:
			theme_dir = "/etc/bunsen-exit"
			if not theme_dir:
				theme_dir = "/usr/share/bunsen/skel/.config/bunsen-exit"
				if not theme_dir:
					theme_dir = None
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
				button_values = {'Cancel':'show', 'Logout':'show', 'Suspend':'show',
									'Hibernate':'hide', 'Hybridsleep':'hide',
									'Reboot':'show', 'Poweroff':'show'}
			if button_visibility:
				for item in button_visibility:
					for x in range(0, len(item)):
						key = item[ 0 ]
						val = item[ 1 ]
						button_values[ key ] = val
			try:
				specified_theme = config_file.items('theme')
			except ConfigParser.NoSectionError as err:
				exit_log.warn(err)
				theme['name'] = "default"
			for item in specified_theme:
				for x in range(0, len(item)):
					key = item[ 0 ]
					val = item[ 1 ]
					theme[ key ] = val
		else:
			theme['name'] = "default"
			exit_log.warn("No config file found. Using default button_values.")
			button_values = {'Cancel':'show', 'Logout':'show', 'Suspend':'show',
									'Hibernate':'hide', 'Hybridsleep':'hide',
									'Reboot':'show', 'Poweroff':'show'}
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

	def log_theme_warning(self, key, value, var_type):
		exit_log.warn("Could not parse " + key + ". Expected a(n) " + var_type + ".")
		exit_log.warn("Setting value to " + str(value) + ".")
		return

	def test_entry(self, key, value, var_type):
		if var_type == "int":
			try:
				temp = int(value)
				result = True
			except:
				self.log_theme_warning(key, value, var_type)
				result = False
		elif  var_type == "float":
			try:
				temp = float(value)
				result = True
			except:
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
			temp = os.path.exists
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

	def validate_theme_entries(self, theme, theme_entries):
		theme_defaults = default_theme.Default_Theme()
		default_dict = theme_defaults.get_default_theme()
		for key, value in default_dict.iteritems():
			if not key in theme_entries:
				exit_log.warn("<key error>: " + key + " does not exist in config file.")
				exit_log.warn("setting key " + key + " to default value " + str(value) + ".")
				theme_entries[key] = value
			if theme_entries[key] == "" or theme_entries[key] == None:
				# Value does not exist so plug in a default
				exit_log.warn("Value does not exist for key " + key + ".")
				exit_log.warn("Setting default to " + str(value) + ".")
				theme_entries[key] = str(value)
			# Test for ints
			if key == "dialog_height" \
				or key == "button_height" \
				or key == "inner_border" \
				or key == "overall_opacity" \
				or key == "button_spacing":
				var_type = "int"
				result = self.test_entry(key, value, var_type)
				if not result:
					theme_entries[key] = str(value)
			# Test for floats
			if key == "sleep_delay" \
				or key == "window_width_adjustment":
				var_type = "float"
				result = self.test_entry(key, value, var_type)
				if not result:
					theme_entries[key] = str(value)
			# Test directory entry
			if key == "icon_path":
				exit_log.debug("icon_path set to " + theme_entries[key] + ".")
				var_type = "dir"
				result = self.test_entry(key, value, var_type)
				if not result:
					theme_entries[key] = str(value)
			# Test for files
			if key == "button_image_cancel" \
				or key == "button_image_poweroff" \
				or key == "button_image_reboot" \
				or key == "button_image_suspend" \
				or key == "button_image_logout" \
				or key == "button_image_hybridsleep" \
				or key == "button_image_hibernate":
				file_path = key + "/" + value
				var_type = "file"
				result = self.test_entry(file_path, value, var_type)
				if not result:
					theme_entries[key] = str(value)
			# test for colors
			if key == "window_background_normal" \
				or key == "button_background_normal" \
				or key == "button_background_prelight" \
				or key == "text_color_normal" \
				or key == "text_color_prelight" \
				or key == "tooltip_background" \
				or key == "tooltip_foreground":
				var_type = "color"
				result = self.test_entry(key, value, var_type)
				if not result:
					theme_entries[key] = str(value)
		return theme_entries
