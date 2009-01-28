# Copyright (C) 2008, 2009 Red Hat, Inc.  All rights reserved.
#
# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program; if
# not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth
# Floor, Boston, MA 02110-1301, USA.  Any Red Hat trademarks that are
# incorporated in the source code or documentation are not subject to the GNU
# General Public License and may only be used or replicated with the express
# permission of Red Hat, Inc.
#
# Red Hat Author: Miloslav Trmac <mitr@redhat.com>

import getpass
import logging
import readline # for raw_input
import sys

import server_common
import utils

def main():
    options = utils.get_daemon_options('Add an administrator to the signing '
                                       'server', '~/.sigul/server.conf',
                                       daemonize=False)
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=utils.logging_level_from_options(options))
    try:
        config = server_common.ServerBaseConfiguration(options.config_file)
    except utils.ConfigurationError, e:
        sys.exit(str(e))
    try:
        utils.set_regid(config)
        utils.set_reuid(config)
        utils.update_HOME_for_uid(config)
    except:
        # The failing function has already logged the exception
        sys.exit(1)

    try:
        utils.nss_init(config)
    except utils.NSSInitError, e:
        sys.exit(str(e))
    name = raw_input('Administrator user name: ')
    password1 = getpass.getpass('Administrator password: ')
    password2 = getpass.getpass('Administrator password (again): ')
    if password1 != password2:
        sys.exit('Passwords don\'t match.')
    db = server_common.db_open(config)
    user = server_common.User(name, clear_password=password1, admin=True)
    db.save(user)
    db.commit()

if __name__ == '__main__':
    main()