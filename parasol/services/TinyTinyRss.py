#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
