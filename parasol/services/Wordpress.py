#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService

class Wordpress(AbstractService):
    """All your blogs"""

    url = ""

    def __init__(self, config):
        raise NotImplementedError

    def do_backup(self):
        raise NotImplementedError

