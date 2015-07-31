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
import services
from services.AbstractService import AbstractService
from services.Pinboard import Pinboard
from services.Trello import Trello
import inspect
import configparser

class BackupServices(object):

    def __init__(self, services, config):
        #Fetch available services
        all_services    = {s[0]: s[1] for s in AbstractService.list_services()}
        #Get config options
        config_settings = BackupServices.read_config(config)
        #Run the backups
        self.run_backups(all_services, config_settings)

    def run_backups(self, all_services, config_settings):
        '''Run the backup for each service specified in the config files provided'''
        for section in config_settings.sections():
            service_config = config_settings[section]
            service_name   = BackupServices.get_service_name(config_settings, section)

            try:
                service_class = BackupServices.fetch_service(all_services, service_name)
                BackupServices.run_backup(service_name, service_class, service_config)
            except ServiceNotFoundException:
                click.echo('Found config section for {} but no matching service. Skipping'.format(service_name))
                continue

    @staticmethod
    def run_backup(service_name, service_class, service_config):
        '''Run the backup for the service provided by service_class and with the configuration settings in service_config'''
        click.echo('Backing up ' + service_name)
        service = service_class(service_config)
        service.do_backup()

    @staticmethod
    def get_service_name(config_settings, section):
        if 'service' in config_settings[section]:
            return config_settings[section]['service']
        return section

    @staticmethod
    def fetch_service(all_services, service_name):
        if service_name in all_services:
            return all_services[service_name]

        raise ServiceNotFoundException('Service class for {} not found'.format(service_name))

    @staticmethod
    def read_config(config_file):
        '''Use ConfigParser to read in the configuration file from the path specified by config_file'''
        config = configparser.ConfigParser()
        config.read(config_file)
        return config

class ServiceNotFoundException(Exception): pass

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
    for name, service in AbstractService.list_services():
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
