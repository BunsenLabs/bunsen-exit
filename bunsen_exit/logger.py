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
import logging
import logging.handlers
import os
import sys
import traceback


def setup_logging(fname, loglevel):
    """
    Set up logging to the specified filename
    Args:
        fname: the filename to log too. This file will appear under home. For instance,
        when testing, I typically log to ~/bl_exit.log. However, we would typically want to
        log to ~/.xsession-errors

    Returns:

    """
    try:
        if loglevel is "None":
            # If loglevel is None then dump logs to /dev/null.
            # This way they will still print to console.
            path = "/dev/null"
        else:
            # If the filename entered on the command line is None or does not exist,
            # then log to ~/.xsession-errors.
            # I chose to allow logging to other file because ~/.xsession-errors can get quite spammy
            # and it might be important to have clear logs while designing.
            if fname == "None":
                path = os.path.expanduser('~')
                path = path + "/.xsession-errors"
            else:
                if fname.startswith("~"):
                    path = os.path.expanduser('~')
                    fname = fname.replace("~", "")
                    path = path + fname
                else:
                    path = fname
        sys.path.append(path)
        # create a file handler
        file_handler = logging.FileHandler(path)
        # Create a console handler
        console_handler = logging.StreamHandler()
        log = logging.getLogger('Bunsen-Exit-Log')
        loglevel = loglevel.lower()
        if loglevel == "debug":
            log.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)
        elif loglevel == "warn":
            log.setLevel(logging.WARN)
            file_handler.setLevel(logging.WARN)
            console_handler.setLevel(logging.WARN)
        elif loglevel == "info":
            log.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            console_handler.setLevel(logging.INFO)
        elif loglevel == "none":
            log.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            console_handler.setLevel(logging.INFO)
        else:
            print("--------------------------------------")
            print("Unknown option for loglevel " + loglevel)
            print("Expected one of, Debug, Warn, or Info.")
            print("Setting default to Warn.")
            print("--------------------------------------")
            log.setLevel(logging.WARN)
            file_handler.setLevel(logging.WARN)
            console_handler.setLevel(logging.WARN)

        # create a logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        # add the handlers to the logger
        log.addHandler(file_handler)
        log.addHandler(console_handler)
        msg = "Logging successfully started. \nLogging to " + path
        log.info(msg)
    except Exception as err:
        print (str(err))
        ex_type, ex, tb = sys.exc_info()
        traceback.print_tb(tb)
    return log
