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

import configparser
import logging
import sys
import os.path

class BackupServices(object):

    service_registry = ServiceRegistry(AbstractService)

    config_defaults = {
            'backup_location': os.path.join('~', 'Documents', 'backups')
            }

    def __init__(self, services, config_file, logging_level):
        #Get config options
        self.config_settings  = BackupServices.read_config(config_file, defaults = self.config_defaults)
        #Configure logging
        self.logger = BackupServices.setup_logging(logging_level)
        #Run the backups
        self.run_backups()

    def run_backups(self):
        """Run the backup for each service specified in the config files provided"""

        for section_name, service_name in self.services_to_run():
            try:
                service_config = self.config_settings[section_name]
                service_class  = self.service_registry[service_name]

                self.run_backup(section_name, service_class, service_config)
            except ServiceNotFoundException:
                self.logger.warning('Found config section for {section_name} {[service_name]} but no matching service. Skipping'.format(section_name=section_name, service_name=service_name))
                pass
            except:
                self.logger.exception("Problem backing up %s", service_name)
                #Continue so that the next backup can be run
                #A problem with one service should not stop us from backing up the rest!
                pass

    def run_backup(self, service_name, service_class, service_config):
        """Run the backup for the service provided by service_class and with the configuration settings in service_config"""
        self.logger.info('Backing up {}'.format(service_name))
        service = service_class(service_config)
        service.do_backup()

    def services_to_run(self):
        """Return the name and config details for each service to run"""
        for section in self.config_settings.sections():
            service_name = self.get_service_name(section)

            #Return details for each service that we care about 
            if service_name in self.service_registry.keys:
                yield section_name, service_name

    def get_service_name(self, section):
        """Return the name of the service in this section of the config"""
        if 'service' in self.config_settings[section]:
            return self.config_settings[section]['service']
        return section

    @classmethod
    def setup_logging(cls, logging_level):
        """Setup logger"""
        logger = logging.getLogger()
        #Log to console
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        #Create formatter, using fixed width fields
        formatter = logging.Formatter("%(name)s: %(levelname)s %(message)s")
        handler.setFormatter(formatter)
        #Set the verbosity, as specified via command line arg
        logger.setLevel(logging_level)

        return logger

    @staticmethod
    def read_config(config_file, defaults):
        """Use ConfigParser to read in the configuration file from the path specified by config_file"""
        config = configparser.ConfigParser(default_section='Backup', defaults = defaults)
        config.read(config_file)
        return config
