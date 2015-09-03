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
from parasol.services.AbstractService import AbstractService
import parasol.util as util

import requests

class TinyTinyRss(AbstractService):
    """All of your RSS feeds, as an OPML file"""

    def __init__(self, config):
        super().__init__(config)

        self.url        = config['url']
        self.verify_ssl = config.getboolean('verify_ssl', True)

    @util.trap_error(util.HTTPInternalServiceError,       "An unexpected error occurred, please try again later.")
    @util.trap_error(requests.exceptions.ConnectionError, "Unable to connect. Please check the URL.")
    def do_backup(self):
        filename = self.filename(ext = 'opml')
        filepath = self.backup_path(filename)

        opml_file = self.connect()

        self.logger.info('Backing up to {}'.format(filename))
        util.write(filepath, opml_file.text)

    def connect(self):
        response = requests.get(self.url, verify=self.verify_ssl)

        #Throw informative error if response is not 200
        util.raise_for_status(response)

        return response
