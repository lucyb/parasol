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

class AbstractService(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.backup_location = util.expandpath(config['backup_location'])
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def do_backup(self):
        """Run the backup for the service"""

    def backup_path(self, filename):
        return os.path.abspath(os.path.join(self.backup_location, filename))

    def echo(self, message):
        self.logger.debug("[{service}] {message}".format(service = self.__class__.__name__, message = message))
