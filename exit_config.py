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
		# Ensure that all theme_entries conform to some sort of sensible defaults
		# Theme entries will default to the bunsen-small theme with a grey style.
		# In order to emulate legacy versions of this app.

		# Validate name
		try:
			if theme_entries['name'] == "" or theme_entries['name'] == None:
				theme_entries['name'] = "Uknown"
				exit_log.warn("Theme entry for name was empty. Setting to Unknown")
		except:
			exit_log.warn("<key error>: name not found in config file. Setting name to Unknown")
			theme_entries['name'] = "Unknown"

		# Validate author
		try:
			if theme_entries['author'] == "" or ['window_width_adjustment'] == None:
				theme_entries['author'] = "Uknown"
				exit_log.warn("Theme entry for author was empty. Setting to Unknown")
		except:
			exit_log.warn("<key error>: author not found in config file. Setting author to Unknown")
			theme_entries['author'] = "Unknown"

		# Validate window_width_adjustment.
		try:
			if theme_entries['window_width_adjustment'] == "" or ['window_width_adjustment'] == None:
				theme_entries['window_width_adjustment'] = 0.50
				exit_log.warn("Theme entry for window_width_adjustment was empty. Setting to 0.50")
			try:
				temp = double(theme_entries['window_width_adjustment'])
			except:
				exit_log.warn["window_width_adjustment is not a float. Defaulting to 0.50"]
				theme_entries['window_width_adjustment'] = 0.50
		except:
			exit_log.warn("<key error>: window_width_adjustment not found in config file.") 
			exit_log.warn("Setting window_width_adjustment to 0.50.")
			theme_entries['window_width_adjustment'] = 0.50

		# Validate dialog_height. Early versions defaults to 130
		try:
			if theme_entries['dialog_height'] == "" or theme_entries['dialog_height'] == None:
				theme_entries['dialog_height'] = 130
				exit_log.warn("Theme entry for dialog_height was empty. Setting to 130")
			try:
				temp = int(theme_entries['dialog_height'])
			except:
				exit_log.warn("dialog_height is not an int. Defaulting to 130")
				theme_entries['dialog_height'] = 130
		except:
			exit_log.warn("<key error>: dialog_height not found in config file.")
			exit_log.warn("Setting dialog_height to 130.")
			theme_entries['dialog_height'] = 130

		# Validate button_height. For early version of this program,
		# dialog_height was the button_height, so button_height will default to 130
		try:
			if theme_entries['button_height'] == "" or theme_entries['button_height'] == None:
				theme_entries['button_height'] = 130
				exit_log.warn("Theme entry for button_height was empty. Setting to 130")
			try:
				temp = int(theme_entries['button_height')
			except:
				exit_log.warn("button_height is not an int. Defaulting to 130")
				theme_entries['button_height'] = 130
		except:
			exit_log.warn("<key error>: button_height not found in config file.")
			exit_log.warn("Setting button_height to 130.")

		# Validate inner_border. Early versions did not use this setting,
		# so inner_border defaults to 0
		try:
			if theme_entries['inner_border'] == "" or theme_entries['inner_border'] == None:
				theme_entries['inner_border'] = 0
				exit_log.warn("Theme entry for inner_border was empty. Setting to 0.")
			try:
				temp = int(theme_entries['inner_border']
			except:
				exit_log.warn("inner_border is not an int. Defaulting to 0")
				theme_entries['inner_border'] = 0
		except:
			exit_log.warn("<key error>: inner_border not found in config file.")
			exit_log.warn("Setting inner_border to 0")
			theme_entries['inner_border'] = 0

		# Validate sleep_delay. Dafaults to 0.001
		try:
			if theme_entries['sleep_delay'] == "" or theme_entries['sleep_delay'] == None:
				theme_entries['sleep_delay'] = 0.001
				exit_log.warn("Theme entry for sleep_delay was empty. Setting to 0.001")
			try:
				temp = theme_entries['sleep_delay'] = float(theme_entries['sleep_delay']
			except:
				exit_log.warn("sleep_delay is not a float. Defaulting to 0.001")
				theme_entries['sleep_delay'] = 0.001
		except:
			exit_log.warn("<key error>: sleep_delay not found in config file.")
			exit_log.warn("Setting sleep_delay to 0.001")
			theme_entries['sleep_delay'] = 0.001
		
		# Validate overall_opacity
		try:
			if theme_entries['overall_opacity'] == "" or theme_entries['overall_opacity'] = None:
				theme_entries['overall_opacity'] = 80
				exit_log.warn("overall_opacity was empty. Setting to 80")
			try:
				temp = int(theme_entries['overall_opacity'])
			except:
				exit_log.warn("overall opacity is not an int. Defaulting to 80")
				theme_entries['overall_opacity'] = 80
		except:
			exit_log.warn("<key error>: overall_opacity not found in config file.")
			exit_log.warn("Setting overall_opacity to 80")
			theme_entries['overall_opacity'] = 80
		
		# Validate button spacing. Prior versions did not use this.
		# Defaults to 0.
		try:
			if theme_entries['button_spacing'] == "" or theme_entries['button_spacing'] = None:
				theme_entries['button_spacing'] = 80
				exit_log.warn("button_spacing was empty. Setting to 0.")
			try:
				temp = int(theme_entries['button_spacing']
			except:
				exit_log.warn("button_spacing is not an int. Defaulting to 0.")
				theme_entries['button_spacing'] = 0
		except:
			exit_log.warn("<key error>: button_spacing not found in config file.")
			exit_log.warn("Setting button_spacing to 0")
			theme_entries['button_spacing'] = 0
		
		
		return
