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
from parasol.BackupServices import BackupServices

import click
import inspect

def logging_levels():
    return {
        1: 'CRITICAL',
        2: 'ERROR',
        3: 'WARNING',
        4: 'INFO',
        5: 'DEBUG'
    }

def calc_logging_level(verbose):
    if verbose >= 5:
        #Can't go higher than debug
        return logging_levels()[5]
    if verbose == 0:
        #Critical errors only if nothing is specified
        return logging_levels()[1]
    return logging_levels()[verbose]

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
    for name, service in BackupServices.service_registry().items():
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
@click.option('-v', '--verbose', count=True)
def run(services, config, verbose):
    logging_level = calc_logging_level(verbose)
    backupStuff = BackupServices(services, config, logging_level)

if __name__ == '__main__':
    run()
