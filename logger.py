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
            if fname is "None":
                path = os.path.expanduser('~')
                path = path + "/.xsession-errors"
            else:
                path = os.path.expanduser('~')
                path = path + "/" + fname
        sys.path.append(path)
        # create a file handler
        file_handler = logging.FileHandler(path)
        # Create a console handler
        console_handler = logging.StreamHandler()
        log = logging.getLogger('Bunsen-Exit-Log')
        if loglevel == "Debug":
            log.setLevel(logging.DEBUG)
            file_handler.setLevel(logging.DEBUG)
            console_handler.setLevel(logging.DEBUG)
        elif loglevel == "Warn":
            log.setLevel(logging.WARN)
            file_handler.setLevel(logging.WARN)
            console_handler.setLevel(logging.WARN)
        elif loglevel == "Info":
            log.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            console_handler.setLevel(logging.INFO)
        elif loglevel == "None":
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
