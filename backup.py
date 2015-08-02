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

import click
from services import *
from ServiceRegistry import ServiceRegistry, ServiceNotFoundException
import inspect
import configparser
import sys

class BackupServices(object):

    def __init__(self, services, config):
        #Find available services
        self.service_registry = ServiceRegistry(AbstractService)
        #Get config options
        self.config_settings  = BackupServices.read_config(config)
        #Populate the list of services, if required
        self.services = self.populate_services(services)
        #Run the backups
        self.run_backups()

    def run_backups(self):
        """Run the backup for each service specified in the config files provided"""

        for service_name, service_config in self.services_to_run():
            try:
                service_class = self.service_registry.get(service_name)
                BackupServices.run_backup(service_name, service_class, service_config)
            except ServiceNotFoundException:
                click.echo('Found config section for {} but no matching service. Skipping'.format(service_name))
                pass
            except:
                click.echo(sys.exc_info())
                #Continue so that the next backup can be run
                #A problem with one service should not stop us from backing up the rest!
                pass

    @staticmethod
    def run_backup(service_name, service_class, service_config):
        """Run the backup for the service provided by service_class and with the configuration settings in service_config"""
        click.echo('Backing up ' + service_name)
        service = service_class(service_config)
        service.do_backup()

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
                yield service_name, service_config

    def get_service_name(self, section):
        """Return the name of the service in this section of the config"""
        if 'service' in self.config_settings[section]:
            return self.config_settings[section]['service']
        return section

    @staticmethod
    def read_config(config_file):
        """Use ConfigParser to read in the configuration file from the path specified by config_file"""
        config = configparser.ConfigParser(default_section='Backup')
        config.read(config_file)
        return config

# List services callback
#
# This uses a callback to interupt the usual argument handling
# http://click.pocoo.org/4/options/#callbacks-and-eager-options
#
# ctx is the script execution context, which in this case we use to exit the
# program (And also check for resiliant parsing, in which case we shouldn't
# exit.
def list_services(ctx, param, value):
    """Callback used for the --list commandline flag, which returns a list of the services the program can potentially back up"""
    # If we weren't called with a value (not sure how this can happen) or we're in the resiliant parsing / no errors mode give up now.
    if not value or ctx.resilient_parsing:
        return

    # iterate over the services list, printing names and the docstrings
    service_registry = ServiceRegistry(AbstractService)
    for name, service in service_registry.items():
        click.echo("{} - {}".format(name, inspect.getdoc(service)))

    # exit with status 0
    ctx.exit(0)

@click.command()
@click.argument('services', nargs=-1)
@click.option('--list', help         = 'List services we know how to back up',
                        is_flag      = True,
                        callback     = list_services,
                        expose_value = False,
                        is_eager     = True)
@click.option('--config', help='Specify location of the config file',
                         default='config.ini')
def run(services, config):
	backupStuff = BackupServices(services, config)

if __name__ == '__main__':
    run()
