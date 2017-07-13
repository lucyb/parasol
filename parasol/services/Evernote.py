#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
