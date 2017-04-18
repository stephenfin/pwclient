# Copyright (C) 2008 Nate Case <ncase@xes-inc.com>
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


def state_id_by_name(rpc, name):
    """Given a partial state name, look up the state ID."""
    if len(name) == 0:
        return 0
    states = rpc.state_list(name, 0)
    for state in states:
        if state['name'].lower().startswith(name.lower()):
            return state['id']
    return 0


def action_list(rpc):
    states = rpc.state_list("", 0)
    print("%-5s %s" % ("ID", "Name"))
    print("%-5s %s" % ("--", "----"))
    for state in states:
        print("%-5d %s" % (state['id'], state['name']))
