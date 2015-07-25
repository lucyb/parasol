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

class Trello(AbstractService):
	
	url	  = 'https://api.trello.com/'
	key   = 'a 32 hexdigit string'
	token = 'a 64 hexdigit string'
	
	def __init__(self):
		#Required?
	
	def doBackup(self):
		#For each board, fetch all data and write the json to a file
		for filename, board_id in boardsToBackup().iteritems():
			getBoardData(filename, board_id)
   
    
	def connect(self, urlPath):
		key_token = key + '&token=' + token

		fullUrl = url + Path
		urllib2.urlopen(fullUrl + '?key=' + key_token)

	def boardsToBackup(self):
		#TODO is there a way of getting all the boards?
		board_dict = {
			'board1': 'a 24 hexdigit string',
			'board2': 'a 24 hexdigit string',
			...,
			'boardn': 'a 24 hexdigit string'
		}
		return board_dict

    def getBoardData(self, filename, boardId):
		print filename
    
		boardUrl = '1/boards/' + board_id
		
		get_url 	= connect(boardUrl)
		board 		= json.loads(get_url.read())
		
		get_url 	= connect(boardUrl + '/lists')
		lists 		= json.loads(get_url.read())
		
		get_url 	= connect(boardUrl + '/cards')
		cards 		= json.loads(get_url.read())
		
		get_url 	= connect(boardUrl + '/checklists')
		checklists 	= json.loads(get_url.read())

		writeData(filename, lists, cards, checklists)

	def writeData(self, boardname, lists, cards, checklists):
		
		filename = 'Trello-'.join(boardname.join(str(datetime.date.today()));
		
		fhtm = open(filename + '.json', 'w')
		print_header(fhtm, board, lists)
		print >> fhtm, '<H1>' + board['name'] + ' (' + str(datetime.date.today())
                 + ')</H1>'
		print_lists(fhtm, lists, cards, checklists)
		print_footer(fhtm)
		fhtm.close()
    
