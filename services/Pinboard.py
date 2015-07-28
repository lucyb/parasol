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

from services.AbstractService import AbstractService
import datetime
import requests
import json

class Pinboard(AbstractService):

	url = 'https://api.pinboard.in/v1/posts/all'

	def __init__(self, token):
		self.token = token

	def doBackup(self):
		#do stuff
		filename = 'Pinboard-{}.json'.format(datetime.date.today())
		pinboard = self.connect()

		chunk_size = 10
		with open(filename, 'wb') as fd:
			for chunk in pinboard.iter_content(chunk_size):
				fd.write(chunk)

	def connect(self):

		auth_token = self.token
		params     = {'format': 'json', 'auth_token': auth_token}

		response = requests.get(Pinboard.url, params = params, stream=True)

		return response
