#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Lucy B
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>.
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

    def filename(self, extra = None):
        """Provides a filename suitable for use in backing up files"""
        safe_name  = slugify.slugify(self.name)
        components = filter(None, [safe_name, extra, self.timestamp()])
        return '-'.join(components)
