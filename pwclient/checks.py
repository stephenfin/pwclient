# Copyright (C) 2017 Stephen Finucane <stephen@that.guru>
#
# This file is part of pwclient.
#
# pwclient is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pwclient is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pwclient; if not, see <http://www.gnu.org/licenses/>.

import sys

from pwclient.compat import xmlrpclib


def action_list(rpc):
    checks = rpc.check_list()
    print("%-5s %-16s %-8s %s" % ("ID", "Context", "State", "Patch"))
    print("%-5s %-16s %-8s %s" % ("--", "-------", "-----", "-----"))
    for check in checks:
        print("%-5s %-16s %-8s %s" % (check['id'],
                                      check['context'],
                                      check['state'],
                                      check['patch']))


def action_info(rpc, check_id):
    check = rpc.check_get(check_id)
    s = "Information for check id %d" % (check_id)
    print(s)
    print('-' * len(s))
    for key, value in sorted(check.items()):
        print("- %- 14s: %s" % (key, value))


def action_create(rpc, patch_id, context, state, url, description):
    try:
        rpc.check_create(patch_id, context, state, url, description)
    except xmlrpclib.Fault as f:
        sys.stderr.write("Error creating check: %s\n" % f.faultString)
