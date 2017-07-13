#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.BackupServices import BackupServices

import click
import inspect
import os.path

logging_levels = [
        'CRITICAL',
        'ERROR',
        'WARNING',
        'INFO',
        'DEBUG'
    ]

def calc_logging_level(verbose, quiet):
    """Returns the appropriate logging level for the application. Defaulting to ERROR if nothing is specified"""
    if quiet and verbose == 0:
        #Show critical errors only
        return logging_levels[0]

    if verbose > 3:
        #Can't go higher than debug
        verbose = 3
    return logging_levels[verbose + 1]

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
    for name, service in BackupServices.service_registry.items():
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
# TODO:  Replace exists=True with custom error handling which points user to example config
# FIXME: resolve_path=True does not expand environmental variables or ~
@click.option('--config',
                        help='Specify location of the config file',
                        default=os.path.join(click.get_app_dir('parasol'), 'config.ini'),
                        show_default=True,
                        type=click.Path(exists=True, dir_okay=False, resolve_path=True))
@click.option('-v', '--verbose',
                        help='Verbose logging. Can be specified multiple times to increase verbosity',
                        count=True)
@click.option('-q', '--quiet',
                        help='Quiet logging. Reduce logging output to critical errors only. Will be ignored if -v is specified',
                        is_flag=True)
def run(services, config, verbose, quiet):
    logging_level = calc_logging_level(verbose, quiet)
    backupStuff   = BackupServices(services, config, logging_level)
