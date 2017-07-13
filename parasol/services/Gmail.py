#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService

class Gmail(AbstractService):
    """All of your email"""

    url = ""

    def __init__(self, config):
        raise NotImplementedError

    def do_backup(self):
        raise NotImplementedError
