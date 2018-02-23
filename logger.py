import logging
import logging.handlers
import os
import sys
import traceback


def setup_logging(fname):
    """
    Set up logging to the specified filename
    Args:
        fname: the filename to log too. This file will appear under home. For instance,
        when testing, I typically log to ~/bl_exit.log. However, we would typically want to
        log to ~/.xsession-errors

    Returns:

    """
    try:
        path = os.path.expanduser('~')
        path = path + fname
        sys.path.append(path)
        log = logging.getLogger('Bunsen-Exit-Log')
        log.setLevel(logging.DEBUG)
        # create a file handler
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(logging.DEBUG)
        # Create a console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
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
