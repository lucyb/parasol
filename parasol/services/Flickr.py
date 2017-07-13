#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService

class Flickr(AbstractService):
    """All of your photos"""

    url = 'https://'

    def __init__(self, config):
        if 'url' in config:
            self.url   = config['url']
        self.token = config['token']

    def do_backup(self):
        filename = 'Flickr-{}.json'.format(datetime.date.today())
        flickr = self.connect()
        self.write(filename, json.dumps(flickr.json()))

    def connect(self):
        auth_token = self.token
        path       = ''
        params     = {'format': 'json', 'auth_token': auth_token}

        response = requests.get(self.url + path, params = params, stream=True, verify=True)

        #Throw error if response is not 200
        response.raise_for_status()

        return response

