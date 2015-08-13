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
from parasol.services import *
from parasol.ServiceRegistry import ServiceRegistry, ServiceNotFoundException

import click
import configparser
import sys
import os.path

class BackupServices(object):

    __service_registry__ = None

    config_defaults = {
            'backup_location': os.path.join('~', 'Documents', 'backups'),
            'verbose': False
            }

    def __init__(self, services, config_file):
        #Get config options
        self.config_settings  = BackupServices.read_config(config_file, defaults = self.config_defaults)
        #Populate the list of services, if required
        self.services = self.populate_services(services)
        #Run the backups
        self.run_backups()

    def run_backups(self):
        """Run the backup for each service specified in the config files provided"""

        for section_name, service_config in self.services_to_run():
            try:
                service_name  = self.get_service_name(section_name)
                service_class = self.service_registry().get(service_name)
                BackupServices.run_backup(section_name, service_class, service_config)
                self.run_backup(section_name, service_class, service_config)
            except ServiceNotFoundException:
                click.echo('Found config section for {} but no matching service. Skipping'.format(service_name))
                pass
            except:
                click.echo(sys.exc_info())
                #Continue so that the next backup can be run
                #A problem with one service should not stop us from backing up the rest!
                pass

    def populate_services(self, services):
        """Return the list of services"""
        if not services:
            services = self.config_settings.sections()
        return services

    def services_to_run(self):
        """Return the name and config details for each service to run"""
        for section in self.config_settings.sections():
            service_name = self.get_service_name(section)

            #Return config details for each service that we care about 
            if service_name in self.services:
                service_config = self.config_settings[section]
                yield section, service_config

    def get_service_name(self, section):
        """Return the name of the service in this section of the config"""
        if 'service' in self.config_settings[section]:
            return self.config_settings[section]['service']
        return section

    @classmethod
    def service_registry(cls):
        """Return a service registry to use"""
        if cls.__service_registry__ is None:
            cls.__service_registry__ = ServiceRegistry(AbstractService)
        return cls.__service_registry__

    @staticmethod
    def read_config(config_file, defaults):
        """Use ConfigParser to read in the configuration file from the path specified by config_file"""
        config = configparser.ConfigParser(default_section='Backup', defaults = defaults)
        config.read(config_file)
        return config

    @staticmethod
    def run_backup(service_name, service_class, service_config):
        """Run the backup for the service provided by service_class and with the configuration settings in service_config"""
        click.echo('Backing up ' + service_name)
        service = service_class(service_config)
        service.do_backup()
