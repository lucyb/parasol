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

class Trello(AbstractService):

        url   = 'https://api.trello.com/'
        key   = 'a 32 hexdigit string'
        token = 'a 64 hexdigit string'

        def __init__(self, key, token):
            self.key   = key
            self.token = token

        def do_backup(self):
            #For each board, fetch all data and write the json to a file
            for board_name, board_id in self.boards_to_backup().items():
                self.write_board_data(board_name, board_id)

        def connect(self, url_path):
            params   = {'format': 'json', 'token': self.token, 'key' : self.key}

            response = requests.get(Trello.url.join(url_path), params = params, stream=True)

            if response.status_code != requests.codes.ok:
                raise Exception(response.raise_for_status())

            return response


        def boards_to_backup(self):
            #TODO is there a way of getting all the boards?
            board_dict = {
                'board1': 'a 24 hexdigit string',
                'board2': 'a 24 hexdigit string',
                'boardn': 'a 24 hexdigit string'
            }
            return board_dict

        def write_board_data(self, board_name, board_id):
                filename = 'Trello-{}-{}.json'.format(board_name, str(datetime.date.today()));

                board_url = '1/boards/' + board_id

                board = self.connect(board_url)
                self.write(filename, board, True)

                lists = self.connect(board_url.join('/lists'))
                self.write(filename, lists, True)

                cards = self.connect(board_url.join('/cards'))
                self.write(filename, cards, True)

                checklists = self.connect(board_url.join('/checklists'))
                self.write(filename, checklists, True)

