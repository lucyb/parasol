#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import inspect

#Used to add to the whitelist below
from parasol.services import *
from parasol.ServiceRegistry import *
from parasol.util import *

class LoggingSetup(object):

    @staticmethod
    def setup(level):
        """Setup logger"""
        logger = logging.getLogger()
        #Log to console
        handler = logging.StreamHandler()
        #Filter out messages from third party libraries
        if not level == 'DEBUG':
            handler.addFilter(LoggerWhitelist())
        logger.addHandler(handler)
        #Create formatter, using fixed width fields
        formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        #Set the verbosity, as specified via command line arg
        logger.setLevel(level)

        return logger

class LoggerWhitelist(logging.Filter):
    """Whitelist for logging messages"""
    #Whitelist class from https://stackoverflow.com/a/17276457
    def __init__(self):
        #Fetch all parasol classes (from https://stackoverflow.com/a/8093671)
        #This will include all classes imported into the namespace and the class that creates the logger
        self.whitelist = [logging.Filter(clsmember[0]) for clsmember in inspect.getmembers(sys.modules[__name__], inspect.isclass)]
        self.whitelist.append(logging.Filter("root"))

    def filter(self, record):
        return any(f.filter(record) for f in self.whitelist)
