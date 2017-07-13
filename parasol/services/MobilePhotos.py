#!/usr/bin/env python
# -*- coding: utf-8 -*-

from parasol.services.AbstractService import AbstractService
import parasol.util as util

import paramiko

import os.path as ops
import os
import stat
from contextlib import contextmanager

class MobilePhotos(AbstractService):
    """All the photos from your mobile phone"""

    def __init__(self, config):
        super().__init__(config)

        self.host            = config['host']
        self.remote_path     = config['remote_path']
        self.port            = int(config.get('port', 22))
        self.username        = config.get('username')
        self.password        = config.get('password')

    def do_backup(self):
        """Backup all photos on the remote path"""
        with self.connect() as sftp:
            sftp.chdir(self.remote_path)

            for filename in MobilePhotos.find_all(sftp, '.'):
                self.backup_file(sftp, filename)

    def backup_file(self, sftp, filename):
        """Backup one file via sftp"""
        # figure out where the file would be, if we already had it
        local = self.backup_path(filename)

        # use lexists to account for git-annex and files possibly living in a remote location.
        if ops.lexists(local):
            self.logger.debug("{} ... OK!".format(local))
        else:
            self.logger.debug("{} ... fetching...".format(local))

            with sftp.open(filename, "r") as f:
                util.write(local, f.read(), binary = True)

    # The contextmanager turns a method which yields into something which can
    # be used with a with block.  And error in the block gets re-raised at the
    # yield statement so the finally block can fire, closing the connection
    # down.
    @contextmanager
    def connect(self):
        """Connect to the backup host and yield an sftp client, cleaning up after"""
        # make a client
        client = paramiko.SSHClient()

        try:
            # load up user's host keys
            client.load_system_host_keys()

            # Try and connect, using the supplied password or SSH agent
            client.connect(self.host, self.port, username = self.username, password = self.password)

            sftp = client.open_sftp()

            yield sftp
        finally:
            client.close()

    # recurse while yielding results
    # modified from https://stackoverflow.com/questions/13205875/add-an-item-into-a-list-recursively
    @staticmethod
    def find_all(sftp, directory):
        # loop over the directory, getting the atributes
        for item in sftp.listdir_attr(directory):
            # use join on the string, not os.path join to avoid possible cross-platform issues
            # though this assumes the server is running linux.
            path = '/'.join([directory, item.filename])

            # if we're a file, yield it
            if not stat.S_ISDIR(item.st_mode):
                yield path
            else: # path is a dir
                try: # so we recurse!
                    for found_path in MobilePhotos.find_all(sftp, path):
                        yield found_path
                except EnvironmentError:
                    pass # ignore errors

