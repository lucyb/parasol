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
        #if services is empty, then fetch all classes in the services
        #module that are a subclass of AbstractService
        all_services = AbstractService.list_services()
        for name, service in all_services:
            click.echo('Backing up ' + name)
            service_config = self.read_config('config.ini', name)
            s = service(service_config)
            s.do_backup()

    def read_config(self, config_file, service_name):
        config = configparser.ConfigParser()
        config.read(config_file)
        return config[service_name]

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
