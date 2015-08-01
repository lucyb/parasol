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

from services import *

class ServiceRegistry(object):
    """A registry of all known backup services"""

    def __init__(self, service_type):
        """Create a ServiceRegistry instance and load all known subclasses of
           service_type"""
        self.services = {}
        self.load_all(service_type)

    def load_all(self, service_type):
        """Locate all services that implement the class provided by service_type
           and add to the dict of known services.
           Return the dict of services"""
        for concrete_service in service_type.__subclasses__():
            self.load(concrete_service.__name__, concrete_service)
        return self.services

    def load(self, service_name, service_class):
        """Add a service to the dict of known services"""
        self.services[service_name] = service_class

    def get_all(self):
        return self.services

    def get(self, service_name):
        """Return the concrete service having the name specified in service_name"""
        if service_name in self.services:
            return self.services[service_name]
        raise ServiceNotFoundException('Service class for {} not found'.format(service_name))

    def __getitem__(self, service_name):
        """Return the concrete service having the name specified in service_name"""
        return self.get(service_name)

class ServiceNotFoundException(Exception): pass
