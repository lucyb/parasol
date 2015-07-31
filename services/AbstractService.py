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

import abc

class AbstractService(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def do_backup(self):
        """Run the backup for the service"""

    def write(self, filename, data, append=False):
        mode = 'w'
        if append:
            mode = 'a'

        with open(filename, mode) as fd:
            fd.write(data)
