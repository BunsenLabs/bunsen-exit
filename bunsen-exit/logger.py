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
