# bunsen-exit

bl-exit:    Logout dialog box with various options.

The script works both in a graphical and a non-graphical environment. In a graphical environment, the window is only shown when the script is launched without arguments. The <Shift> key can be used to show | hide the button labels. The <Shift> key acts as a toggle, so button labels will not be hidden again until the <Shift> key is pressed again.  

When  the script is launched in a non-graphical environment the requested action should be one of the accepted arguments and the action is executed without asking for confirmation.
In a non-graphical environment, one of the accepted actions must be specified as an argument.

**USAGE:**  

	-l	--logout	Logs the user out.
	-s	--suspend	Suspend the system.
	-i	--hibernate	Hibernate the system.
	-y	--hybridsleep	Hybrid sleep the system.
	-b	--reboot	Reboot the system.
	-p	--poweroff	Power off the system.
	-f	--logfile	Which file to log too, e.g. ~/bl-exit.log or ~/.xsession-errors
	-z	--loglevel	The default logging level can be one of:
				* None - Logging turned off or sent to /dev/null
				* Info - only log [INFO] messages.
				* Warn - log [WARN] and [INFO] messages.
				* Debug - log all messages.
When designing themes for the exit dialog, I would recommend that the loglevel be set to at least Warn and send the logs into their own file such as ~/bl-exit.log. The logfile defaults to ~/xsession-errors. With the loglevel set to None, logs will be sent to /dev/null. However, the console handler will still print messages to the console. Note that the Debug option is pretty verbose but does display all the program's inputs and outputs. 
## Configuration:

Bunsen-exit is designed to be themed. Themes are setup in two different files. The first file, in ~/.config/bunsen-exit/bl-exitrc controls which buttons are shown and the theme to use when running bl-exit. If this config file cannot be found, the program will run with the gtk2 theme currently specified in ~/gtkrc-2.0. This is functionally the equivalent of running the "Classic" version from Crunchbang.

**Button Settings**

    [button_values] 
    Cancel = show 
    Logout = show 
    Suspend = show 
    Reboot = show 
    PowerOff = show 
    Hibernate = hide
    HybridSleep = hide

Button labels are derived from these settings, so it is important that the names such as Cancel, Logout, etc remain in the list. These settings toggle whether to show/hide the buttons when building the exit dialog.

**Themes**

Set the directory and file for the theme
If one cannot be found, then the default gtk theme will be used.

    [theme]
    dir = themes
    rcfile = helium.rc
    name = helium
[theme] is required in order to properly parse the rest of the entries under it. dir is the directory under ~/.config/bunsen-exit that holds the specified theme, in this case under ~/.config/bunsen-exit/themes/, while rcfile is the name of the actual file to load, in this case, that file name would be helium.rc

## Theme Entries
I chose to implement the theme entries in an ini style format. I feel like this will be a simpler interface for theme designers to use. Additionally, I had considerable difficulty implementing custom classes in the gtk.RcStyles format. 

*NOTE:* All defaults are taken from the theme bunsen-small from the original bl-exitrc. 
This is the previous set of defaults used in Bunsenlabs Hydrogen. 
*NOTE*: In order to achieve the original Crunchbang look, ensure that you have a gtk theme similar to that of #! set as your default, then remove or rename # the config file, located at: ~/.config/bunsen-exit/bl-exitrc
  
   [theme] is mandatory. Please do not remove it. 
    **Meta Data**
    
     name	The name of the theme. Defaults to Unknown 
     author	The author of the theme. Defaults to Unknown
  
**Dialog**

     window_width adjustment	Percentage of the screen the dialog window should occupy. 
									Must resolve to a float. 
									Defaults to 0.50 
									Scale factor for window_width_adjustment 
									( 0 = default, 800px; 1 = full screen)
     dialog_height			The height of the dialog window. 
									Must be resolve to an int. 
									Defaults to 64.
  **Opacity**
   
     sleep_delay		Delay for the fade in counter. 
							This allows the dialog to fade into view.
							Must resolve to a float. 
							Defaults to 0.001.
	 overall_opacity	Opacity of the dialog from (0 - 100)
						0 is transparent. 100 is opaque. 
						Must resolve to an int. 
						Defaults to 100.
**Buttons**
  

      button_height		The height of the custom buttons.
							Must resolve to an int.
							Defaults to 64.  
NOTE: values of less than 60 tend to create clipping on the labels. Similarly, values larger than the dialog_height will create clipping.

        inner_border	Specifies the size of the horizontal container that the buttons get packed into. 
						Must resolve to an int. 
						Defaults to 0.
Useful to create a thin inner border between the dialog and that container.  Large values may create clipping. 
					        
        button_spacing	The spacing between the buttons. 
						Must resolve to an int. 
						Defaults to 0.
        icon_path		The path to the images you want to map to the buttons. 
   If this path cannot be found, then the dialog will fall back to a default gtk dialog.
   
   Button textures (i.e. the images on them) Map file names to button types similar to below. When button images fail to load, an image from gtk.STOCK_DIALOG_ERROR is loaded instead. 			

	button_image_cancel = cancel-sm.png
	button_image_poweroff = poweroff-sm.png
	button_image_reboot = reboot-sm.png
	button_image_suspend = sleep-sm.png
	button_image_logout = logout-sm.png
	button_image_hybridsleep = hibernate-sm.png
	button_image_hibernate = hibernate-sm.png
  **Labels**
   

	label_height	Additional height to add to the dialog when <Shift> 
					is pressed and button labels are shown. 
					Increase this value for larger fonts or fonts
					with odd ascenders/descenders that end up clipped. 
						Defaults to 20. 
						Must be an int.
**Window Colors**
   

     window_background_normal		The color of the dialog window. 
			    						Must use hexadecimal color format. 
	    								Defaults to #838383.
**Button Colors**
  

      button_background_normal		The normal color of the button. 
									  Must use hexadecimal format. 
								      Defaults to #838383.
      button_background_prelight	the highlighted color of the button. 
								      Must use hexadecimal format. 
								      Defaults to #c1c1c1.
**Text Colors**
   

     text_color_normal		The normal text color for labels. 
			    				Must use hexadecimal format.     																		    												
			    				Defaults to #d9d9d9.
     text_color_prelight	The highlighted text color of labels. 
								Must use hexadecimal format.
								Defaults to #d9d9d9.
**Tooltip Colors**
   

     tooltip_background		The color of tooltip backgrounds.
								Must use hexadecimal format.
								Defaults to #c1c1c1.
     tooltip_foreground		The tooltip text color. 
								Must use hexadecimal format.
								Defaults to #000000.
**Button Label Font**

		font_family		Sets the font family for labels, e.g. sans, serif, monospace. 
		font_style		Sets the font style, e.g. bold, or bold italic.
		font_size		Sets the font size for font_labels.
**Tooltip Font**
   

     tooltip_font_family	Sets the font family for tooltips
								Defaults to Noto Sans
        tooltip_font_style	Sets the font style for tooltips, e.g. bold or regular
								Defaults to regular.
        tooltip_font_size	Sets the font size for tooltips.
								Defaults to 9.
