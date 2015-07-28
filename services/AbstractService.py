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

class AbstractService(object):
	
	def do_backup(self):
		raise NotImplementedError()
		
	def write(self, filename, response, append=False):
		mode = 'wb'
		if append:
			mode = 'ab'
			
		chunk_size = 10
		with open(filename, mode) as fd:
			for chunk in response.iter_content(chunk_size):
				fd.write(chunk)

