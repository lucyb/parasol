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

import datetime
import requests
import json

class TtRss(AbstractService):
    """All of your RSS feeds, as an OPML file"""

    default_url = 'https://tt-rss.org/api'

    def __init__(self, config):
        super().__init__(config)

        self.url      = config.get('url', self.default_url)
        self.username = config['username']
        self.password = config['password']

    def do_backup(self):
        filename = 'ttrss-{}.json'.format(datetime.date.today())
        filepath = self.backup_path(filename)

        session_id = self.log_in()

        #TODO handle error gracefully and log out anyway
        opml = self.download_opml(session_id)
        self.logger.info('Backing up to {}'.format(filename))
        util.write(filepath, json.dumps(opml.json()))

        self.log_out(session_id)

    def log_in(self):
        params = {'format': 'json', 'user': self.username, 'password': self.password}
        path   = '/login'

        response = self.connect(path, params)
        #TODO parse json response and extract session id (sid)
        return session_id

    def download_opml(self, session_id):
        params = {'format': 'json', 'sid': session_id}
        path   = '/getFeeds'
        #TODO this might be /getFeedTree
        opml = self.connect(path, params)

        return opml

    def log_out(self, session_id):
        params = {'format': 'json', 'sid': session_id}
        path   = '/logout'

        self.connect(path, params)

    def connect(self, path, params):
        response = requests.get(self.url + path, params = params, verify=True)

        #Throw error if response is not 200
        response.raise_for_status()

        #TODO check json response for error

        return response
