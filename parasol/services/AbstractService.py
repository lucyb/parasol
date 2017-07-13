#!/usr/bin/env python
# -*- coding: utf-8 -*-

import parasol.util as util

import click

import abc
import os.path
import logging
import time
import slugify

class AbstractService(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.name              = config.name
        self.backup_location   = util.expandpath(config['backup_location'])
        self.timestamp_format  = config['timestamp']
        #Create a child logger for each service based on the logger configured in BackupServices.py
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def do_backup(self):
        """Run the backup for the service"""

    def backup_path(self, filename):
        """Return the full filepath"""
        return os.path.abspath(os.path.join(self.backup_location, filename))

    def timestamp(self):
        """Return the timestamp, or nothing if the timestamp looks falsy"""
        if not self.timestamp_format.lower() in ('none', 'false', '0'):
            return time.strftime(self.timestamp_format)
        else:
            return None

    def filename(self, ext, extra = None):
        """Provides a filename suitable for use in backing up files"""
        safe_name  = slugify.slugify(self.name)
        if extra:
            extra  = slugify.slugify(extra)

        components = filter(None, [safe_name, extra, self.timestamp()])
        slugified  = '-'.join(components)
        return '.'.join([slugified, ext])
