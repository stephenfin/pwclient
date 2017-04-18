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


def project_id_by_name(rpc, linkname):
    """Given a project short name, look up the Project ID."""
    if len(linkname) == 0:
        return 0
    projects = rpc.project_list(linkname, 0)
    for project in projects:
        if project['linkname'] == linkname:
            return project['id']
    return 0


def action_list(rpc):
    projects = rpc.project_list("", 0)
    print("%-5s %-24s %s" % ("ID", "Name", "Description"))
    print("%-5s %-24s %s" % ("--", "----", "-----------"))
    for project in projects:
        print("%-5d %-24s %s" % (project['id'],
                                 project['linkname'],
                                 project['name']))
