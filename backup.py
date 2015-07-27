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
from datetime import datetime
from services import Pinboard

class BackupServices(object):
				
	def __init__(self, services):
		for service in services:
			Pinboard('')

@click.command()
@click.argument('services', nargs=-1)
def run(services):
	backupStuff = BackupServices(services)
	
if __name__ == '__main__':
	run()
