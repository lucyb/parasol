#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

    def items(self):
        return self.services.items()

    def keys(self):
        return self.services.keys()

    def get(self, service_name):
        """Return the concrete service having the name specified in service_name"""
        if service_name in self.services:
            return self.services[service_name]
        raise ServiceNotFoundException('Service class for {} not found'.format(service_name))

    def __getitem__(self, service_name):
        """Return the concrete service having the name specified in service_name"""
        return self.get(service_name)

class ServiceNotFoundException(Exception): pass
