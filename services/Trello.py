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
import click
import json

class Trello(AbstractService):
    """All your organisation with everyone"""

    default_url = 'https://api.trello.com/'

    def __init__(self, config):
        self.url   = config.get('url', self.default_url)
        self.key   = config.get('key')
        self.token = config.get('token')

    def do_backup(self):
        #For each board, fetch all data and write the json to a file
        for board_id, board_name in self.boards_to_backup().items():
            self.write_board_data(board_id, board_name)

    def connect(self, url_path):
        params   = {'format': 'json', 'key' : self.key, 'token': self.token}

        response = requests.get(self.url + url_path, params = params, verify=True)

        response.raise_for_status()     #Throw error if response is not 200

        return response


    def boards_to_backup(self):
        boards = self.connect('1/members/me/boards')
        board_dict = {}
        for boardJson in boards.json():
            board_dict[boardJson['id']] = boardJson['name']

        return board_dict

    def write_board_data(self, board_id, board_name):
        filename = 'Trello-{0}-{1}.json'.format(board_name, str(datetime.date.today()));

        board_url = '1/boards/' + board_id

        board_info = {}

        board = self.connect(board_url)
        board_info['board'] = board

        lists = self.connect(board_url + '/lists')
        board_info['lists'] = lists

        cards = self.connect(board_url + '/cards')
        board_info['cards'] = cards

        checklists = self.connect(board_url + '/checklists')
        board_info['checklists'] = checklists

        self.write(filename, json.dumps(board_info))
