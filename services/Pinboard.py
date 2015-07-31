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

from services.AbstractService import AbstractService
import datetime
import requests
import json

class Pinboard(AbstractService):
    """All of your bookmarks"""

    url = 'https://api.pinboard.in/v1/'

    def __init__(self, config):
        if 'url' in config:
            self.url   = config['url']
        self.token = config['token']

    def do_backup(self):
        filename = 'Pinboard-{}.json'.format(datetime.date.today())
        pinboard = self.connect()
        self.write(filename, json.dumps(pinboard.json()))

    def connect(self):
        auth_token = self.token
        path       = 'posts/all'
        params     = {'format': 'json', 'auth_token': auth_token}

        response = requests.get(self.url + path, params = params, stream=True, verify=True)

        #Throw error if response is not 200
        response.raise_for_status()

        return response
