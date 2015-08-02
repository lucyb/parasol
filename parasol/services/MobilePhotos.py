#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2015 Lucy B, Jonathan Stott
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

from parasol.services.AbstractService import AbstractService
import os.path as ops
import os
import stat
import paramiko
import click


class MobilePhotos(AbstractService):
    """All the photos from your mobile phone"""

    def __init__(self, backup_location, host, remote_path, username=None, port=22, password=None):
        self.backup_location = ops.expandvars(ops.expanduser(backup_location))
        self.host            = host
        self.remote_path     = remote_path
        self.port            = port
        self.username        = username
        self.password        = password

    def do_backup(self):
        # connect with the client
        self.client = self.connect()

        # open up sftp
        self.sftp   = self.client.open_sftp()

        # change to the mobile location
        self.sftp.chdir(self.remote_path)

        # recurse from there, looking for photos
        for filename in self.find_all('.'):

            # figure out where the file would be, if we already had it
            local = ops.abspath(ops.join(self.backup_location, filename))

            # use lexists to account for git-annex and files possibly living in a remote location.
            if ops.lexists(local):
                click.echo("{} ... OK!".format(local)) # yay, report and move on
            else: # get it!
                click.echo("{} ... fetching...".format(local))
                directory = ops.dirname(local)

                if not ops.isdir(directory):
                    # make directories if we need to
                    os.mkdir(directory)

                # fetch it!
                self.sftp.get(filename, local)


    def connect(self):
        # make a client
        client = paramiko.SSHClient()

        # load up user's host keys
        client.load_system_host_keys()

        # try and connect
        client.connect(self.host, self.port, username = self.username, password = self.password)

        return client

    # recurse while yielding results
    # modified from https://stackoverflow.com/questions/13205875/add-an-item-into-a-list-recursively
    def find_all(self, directory):
        # loop over the directory, getting the atributes
        for item in self.sftp.listdir_attr(directory):
            # use join on the string, not os.path join to avoid possible cross-platform issues
            # though this assumes the server is running linux.
            path = '/'.join([directory, item.filename])

            # if we're a file, yield it
            if not stat.S_ISDIR(item.st_mode):
                yield path
            else: # path is a dir
                try: # so we recurse!
                    for found_path in self.find_all(path):
                        yield found_path
                except EnvironmentError:
                    pass # ignore errors

