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

import urllib2
import json

class Pinboard(AbstractService):
	
	def __init__(self):
		#Required?
	
	def doBackup(self):
		#do stuff
		filename = 'Pinboard-'.join(str(datetime.date.today()).join('.json');
		pinboard = connect()
		#destinationFullPath = os.path.join(destinationPath, self.filename)
	
		f = None
		try:
		    f = open (filename, 'w')
			f.write(pinboard)
		finally:
			if f is not None:
				f.close()
	
	def connect(self):
		
		auth_token = ''
		url		   = 'https://api.pinboard.in/v1/posts/all'
		query_string= '?format=json&auth_token'.join(auth_token)
		
		full_url = url.join(query_string)
		response = urllib2.urlopen(full_url)
		return json.load(response)
