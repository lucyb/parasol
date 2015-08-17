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
        #Get the section names to run backups for
        section_names = self.get_sections_to_backup(services)
        #Run the backups
        self.run_backups(section_names)

    def get_sections_to_backup(self, sections):
        """Return the list of sections to run backups for. Defaults to all"""
        if not sections:
            sections = self.config_settings.sections()
        return sections

    def run_backups(self, section_names):
        """Run the backup for each service specified in the config files provided"""
        for section_name, service_config in self.services_to_run(section_names):
            try:
                service_name   = service_config.get('service', section_name)

                service_class  = self.service_registry[service_name]

                self.run_backup(section_name, service_class, service_config)
            except ServiceNotFoundException:
                self.logger.warning('Found config section for {section_name} {[service_name]} but no matching service. Skipping'.format(section_name=section_name, service_name=service_name))
                pass
            except:
                self.logger.exception("Problem backing up {section} [{service}]".format(section = section_name, service = service_name))
                #Continue so that the next backup can be run
                #A problem with one service should not stop us from backing up the rest!
                pass

    def run_backup(self, service_name, service_class, service_config):
        """Run the backup for the service provided by service_class and with the configuration settings in service_config"""
        self.logger.info('Backing up {}'.format(service_name))
        service = service_class(service_config)
        service.do_backup()

    def services_to_run(self, section_names):
        """Return the name and config details for each service to run"""
        for section_name in section_names:
            service_config = self.config_settings[section_name]

            # return configurations for each section we asked to run
            yield section_name, service_config

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
