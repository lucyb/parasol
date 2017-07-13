#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService
import parasol.util as util

import requests
import json

class Pinboard(AbstractService):
    """All of your bookmarks"""

    default_url = 'https://api.pinboard.in/v1/'

    def __init__(self, config):
        super().__init__(config)

        self.url   = config.get('url', self.default_url)
        self.token = config['token']

    @util.trap_error(util.HTTPAuthorisationError,         "Not authorised: token is incorrect.")
    @util.trap_error(util.HTTPInternalServiceError,       "An unexpected error occurred, please try again later.")
    @util.trap_error(requests.exceptions.ConnectionError, "Unable to connect. Please check the URL.")
    def do_backup(self):
        filename = self.filename(ext = 'json')
        filepath = self.backup_path(filename)

        pinboard = self.connect()
        self.logger.info('Backing up to {}'.format(filename))
        util.write(filepath, json.dumps(pinboard.json()))

    def connect(self):
        auth_token = self.token
        path       = 'posts/all'
        params     = {'format': 'json', 'auth_token': auth_token}

        response = requests.get(self.url + path, params = params, verify=True)

        #Throw informative error if response is not 200
        util.raise_for_status(response)

        return response
