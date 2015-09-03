
import os.path
import logging
from functools import wraps
import requests
import sys

def expandpath(path):
    """Expand out a path with both ~ and ENV variables"""
    return os.path.expandvars(os.path.expanduser(path))

def write(filename, data, append=False, binary=False):
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

def raise_for_status(response):
    """Return custom HTTPErrors based on response HTTP status code.

       Returns a HTTPAuthoristionError for 401 responses.
       Returns a HTTPInteralServiceError for 500 responses.
       Returns original HTTPError otherwise.
    """
    try:
        #requests will throw an error if response does not have a HTTP 200 status code
        response.raise_for_status()
    except requests.HTTPError as e:
        if 401 == e.response.status_code:
            raise HTTPAuthorisationError(e)
        if 500 == e.response.status_code:
            raise HTTPInternalServiceError(e)
        raise e

def trap_error(exception, msg=""):
    """A decorator to trap and log exceptions.
       Usage:
       @trap_error(exception_class, msg="error description to add to log")
    """
    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwds):
            try:
                return func(*args, **kwds)
            except exception:
                logger = logging.getLogger(args[0].__class__.__name__)
                if logger.isEnabledFor(logging.DEBUG):
                    #Display traceback ony if debugging is enabled
                    logger.exception(msg)
                else:
                    logger.error(msg)
        return wrapped
    return decorator

class HTTPAuthorisationError(requests.HTTPError): pass
class HTTPInternalServiceError(requests.HTTPError): pass
