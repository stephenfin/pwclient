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

import os
import sys

from pwclient.compat import xmlrpclib


class Transport(xmlrpclib.SafeTransport):

    def __init__(self, url):
        xmlrpclib.SafeTransport.__init__(self)
        self.credentials = None
        self.host = None
        self.proxy = None
        self.scheme = url.split('://', 1)[0]
        self.https = url.startswith('https')
        if self.https:
            self.proxy = os.environ.get('https_proxy')
        else:
            self.proxy = os.environ.get('http_proxy')
        if self.proxy:
            self.https = self.proxy.startswith('https')

    def set_credentials(self, username=None, password=None):
        self.credentials = '%s:%s' % (username, password)

    def make_connection(self, host):
        self.host = host
        if self.proxy:
            host = self.proxy.split('://', 1)[-1].rstrip('/')
        if self.credentials:
            host = '@'.join([self.credentials, host])
        if self.https:
            return xmlrpclib.SafeTransport.make_connection(self, host)
        else:
            return xmlrpclib.Transport.make_connection(self, host)

    if sys.version_info[0] == 2:
        def send_request(self, connection, handler, request_body):
            handler = '%s://%s%s' % (self.scheme, self.host, handler)
            xmlrpclib.Transport.send_request(self, connection, handler,
                                             request_body)
    else:  # Python 3
        def send_request(self, host, handler, request_body, debug):
            handler = '%s://%s%s' % (self.scheme, host, handler)
            return xmlrpclib.Transport.send_request(self, host, handler,
                                                    request_body, debug)
