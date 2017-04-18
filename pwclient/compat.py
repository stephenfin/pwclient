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

try:
    import xmlrpclib  # noqa
except ImportError:
    # Python 3 has merged/renamed things.
    import xmlrpc.client as xmlrpclib  # noqa

try:
    import ConfigParser  # noqa
except ImportError:
    # Python 3 has renamed things.
    import configparser as ConfigParser  # noqa

import sys
if sys.version_info[0] < 3:
    # the python 2.7 reference implementation tries to re-encode to
    # ascii bytes here but leaves unicode if it fails. Do not try to
    # re-encode to ascii byte string to have a more predictive behavior.
    xmlrpclib._stringify = lambda s: s
