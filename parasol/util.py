
import os.path
import logging
from functools import wraps
import requests
import sys

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

def custom_http_error(func):
    """A decorator to return custom HTTPErrors.

       Returns a HTTPAuthoristionError for 401 responses.
       Returns original HTTPError otherwise.
    """
    @wraps(func)
    def wrapped(*args, **kwds):
        try:
            return func(*args, **kwds)
        except requests.HTTPError as e:
            if 401 == e.response.status_code:
                raise HTTPAuthorisationError(e)
            raise e
    return wrapped

def trap_errors(exception, msg=""):
    """A decorator to trap and log exceptions.
       Usage:
       @trap_errors(exception_class, msg="error description to add to log")
    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwds):
            try:
                return func(*args, **kwds)
            except exception:
                logger = logging.getLogger(args[0].__class__.__name__)
                logger.error(msg)
                if logger.isEnabledFor(logging.DEBUG):
                    #Display traceback ony if debugging is enabled
                    logger.exception("[{}]".format(func.__name__))
        return wrapped
    return decorator

class HTTPAuthorisationError(requests.HTTPError): pass
