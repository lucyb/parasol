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
import datetime
import requests

class Evernote(AbstractService):
    '''All of your notes'''

    default_url = 'https://api.evernote.com/'

    def __init__(self, config):
        self.url   = config.get('url', self.default_url)
        self.token = config['token']

    def do_backup(self):
        raise NotImplementedError()

    def connect(self):
        auth_token = self.token
        path       = ''
        params     = {'format': 'json', 'auth_token': auth_token}

        response = requests.get(self.url + path, params = params, stream=True, verify=True)

        #Throw error if response is not 200
        response.raise_for_status()

        return response
