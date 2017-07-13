#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService
import parasol.util as util

import requests
import os.path
import json

class Trello(AbstractService):
    """All your organisation with everyone"""

    default_url   = 'https://api.trello.com/1/'
    #Ignore the Welcome Board
    ignore_boards = ['5480d754127a52ce96eb950b']

    def __init__(self, config):
        super().__init__(config)

        self.url   = config.get('url', self.default_url)
        self.key   = config['key']
        self.token = config['token']

    @util.trap_error(util.HTTPAuthorisationError,         "Not authorised: key or token is incorrect.")
    @util.trap_error(util.HTTPInternalServiceError,       "An unexpected error occurred, please try again later.")
    @util.trap_error(requests.exceptions.ConnectionError, "Unable to connect. Please check the URL.")
    def do_backup(self):
        #For each board, fetch all data and write the json to a file
        for board_id, board_name in self.boards_to_backup().items():
            self.write_board_data(board_id, board_name)

    def connect(self, url_path, absolute_path = False, **extra_params):
        params = {'format': 'json', 'key' : self.key, 'token': self.token}
        if extra_params is not None:
            #This will overwrite params if there are matching keys
            params.update(extra_params)

        url = ''
        if not absolute_path:
            url = self.url

        response = requests.get(url + url_path, params = params, verify=True)

        util.raise_for_status(response)     #Throw informative error if response is not 200

        return response

    def boards_to_backup(self):
        boards = self.connect('members/me/boards')
        board_dict = {}
        for board_json in boards.json():
            board_id = board_json['id']
            if board_id not in self.ignore_boards and not board_json['closed']:
                board_dict[board_id] = board_json['name']

        return board_dict

    def write_board_data(self, board_id, board_name):
        self.logger.info("Backing up {}".format(board_name))
        filename = self.filename(ext = 'json', extra = board_name)
        filepath = self.backup_path(filename)

        board_url = 'boards/' + board_id
        #See https://trello.com/docs/api/board/
        params = {'actions': 'all', 'actions_limit': '1000', 'cards': 'all', 
                'lists': 'all', 'list_fields': 'all', 'members': 'all', 
                'checklists': 'all', 'fields': 'all', 'card_attachments': 'true', 
                'card_checklists': 'all', 'labels': 'all', 'organization': 'true'}

        board_info = {}

        board = self.connect(board_url, **params)
        board_info['board'] = board.json()

        for card in board_info['board']['cards']:
            for idx, attachment in enumerate(card['attachments']):
                attachmentpath = self.download_attachment(attachment, board_name)
                card['attachments'][idx]['localurl'] = attachmentpath

        util.write(filepath, json.dumps(board_info))

    def download_attachment(self, attachment, board_name):
        self.logger.info("Downloading attachments for {}".format(board_name))

        filename = attachment['id'] + '-' + attachment['name']
        filepath = self.backup_path(os.path.join(board_name, filename))

        to_download = attachment['url']
        result = self.connect(to_download, absolute_path = True)
        util.write(filepath, result.content, binary = True)
        return filepath
