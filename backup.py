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
import sys
import inspect

class BackupServices(object):
				
	def __init__(self, services):
		#if services is empty, then fetch all classes in the services 
		#module that are a subclass of AbstractService
		all_services = self.list_services()
		for name, service in all_services:
			click.echo(name)
			service('')
			
			
	def list_services(self):
		for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass):
			if (issubclass(obj, AbstractService) and name is not 'AbstractService'):
				yield name, obj
				
@click.command()
@click.argument('services', nargs=-1)
def run(services):
	backupStuff = BackupServices(services)
	
if __name__ == '__main__':
	run()
