#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService

class Mobile(AbstractService):
    """Application and settings data from your mobile phone"""

    def __init__(self, config):
        raise NotImplementedError

    def do_backup(self):
        raise NotImplementedError
		#backup clue data
		#backup weight data
		#backup notes
		#backup settings?
