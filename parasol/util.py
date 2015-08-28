
import os.path
import logging
from functools import wraps

def expandpath(path):
    """Expand out a path with both ~ and ENV variables"""
    return os.path.expandvars(os.path.expanduser(path))

def write(filename, data, append=False, binary = False):
    """Write a backup file, making directories necessary to do so"""

    mode = 'w'
    if append:
        mode = 'a'

    if binary is True:
        mode = mode + 'b'

    directory = os.path.dirname(filename)
    if not os.path.isdir(directory):
        os.makedirs(directory, mode = 0o700)

    with open(filename, mode) as fd:
        fd.write(data)

def trap_errors(func=None, msg=None):
    """A decorator to trap and log exceptions.
       Usage:
       @trap_errors
       @trap_errors(msg="error description to add to log")
    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwds):
            try:
                return func(*args, **kwds)
            except Exception:
                logger = logging.getLogger(args[0].__class__.__name__)
                logger.exception("[{}] {}".format(func.__name__, msg))
        return wrapped
    #Allow decorator to be called as a function or not
    if func:
        return decorator(func)
    return decorator
