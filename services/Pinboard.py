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

import requests
import json

class Pinboard(AbstractService):
	
	def __init__(self):
		#Required?
	
	def doBackup(self):
		#do stuff
		filename = 'Pinboard-%s.json' % (datetime.date.today(), )
		pinboard = connect()
		#destinationFullPath = os.path.join(destinationPath, self.filename)
	
		
		with open(filename, 'w') as f:
			f.write(pinboard)
	
	def connect(self):
		
		auth_token = ''
		url		   = 'https://api.pinboard.in/v1/posts/all'
		params     = {'format': 'json', 'auth_token': auth_token}
		
		response = requests.get(url, params = params)
		
		return response.text
