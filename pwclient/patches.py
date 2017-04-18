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

import io
import os
import re
import string
import subprocess
import sys

from pwclient.compat import xmlrpclib
from pwclient.people import person_ids_by_name
from pwclient.states import state_id_by_name


def patch_id_from_hash(rpc, project, hash):
    try:
        patch = rpc.patch_get_by_project_hash(project, hash)
    except xmlrpclib.Fault:
        # the server may not have the newer patch_get_by_project_hash function,
        # so fall back to hash-only.
        patch = rpc.patch_get_by_hash(hash)

    if patch == {}:
        sys.stderr.write("No patch has the hash provided\n")
        sys.exit(1)

    patch_id = patch['id']
    # be super paranoid
    try:
        patch_id = int(patch_id)
    except:
        sys.stderr.write("Invalid patch ID obtained from server\n")
        sys.exit(1)
    return patch_id


def _list_patches(patches, format_str=None):
    """Dump a list of patches to stdout."""
    if format_str:
        format_field_re = re.compile("%{([a-z0-9_]+)}")

        def patch_field(matchobj):
            fieldname = matchobj.group(1)

            if fieldname == "_msgid_":
                # naive way to strip < and > from message-id
                val = string.strip(str(patch["msgid"]), "<>")
            else:
                val = str(patch[fieldname])

            return val

        for patch in patches:
            print(format_field_re.sub(patch_field, format_str))
    else:
        print("%-7s %-12s %s" % ("ID", "State", "Name"))
        print("%-7s %-12s %s" % ("--", "-----", "----"))
        for patch in patches:
            print("%-7d %-12s %s" %
                  (patch['id'], patch['state'], patch['name']))


def action_list(rpc, filter, submitter_str, delegate_str, format_str=None):
    filter.resolve_ids(rpc)

    if submitter_str is not None:
        ids = person_ids_by_name(rpc, submitter_str)
        if len(ids) == 0:
            sys.stderr.write("Note: Nobody found matching *%s*\n" %
                             submitter_str)
        else:
            for id in ids:
                person = rpc.person_get(id)
                print('Patches submitted by %s <%s>:' %
                      (person['name'], person['email']))
                f = filter
                f.add("submitter_id", id)
                patches = rpc.patch_list(f.d)
                _list_patches(patches, format_str)
        return

    if delegate_str is not None:
        ids = person_ids_by_name(rpc, delegate_str)
        if len(ids) == 0:
            sys.stderr.write("Note: Nobody found matching *%s*\n" %
                             delegate_str)
        else:
            for id in ids:
                person = rpc.person_get(id)
                print('Patches delegated to %s <%s>:' %
                      (person['name'], person['email']))
                f = filter
                f.add("delegate_id", id)
                patches = rpc.patch_list(f.d)
                _list_patches(patches, format_str)
        return

    patches = rpc.patch_list(filter.d)
    _list_patches(patches, format_str)


def action_info(rpc, patch_id):
    patch = rpc.patch_get(patch_id)
    s = "Information for patch id %d" % (patch_id)
    print(s)
    print('-' * len(s))
    for key, value in sorted(patch.items()):
        print("- %- 14s: %s" % (key, value))


def action_get(rpc, patch_id):
    patch = rpc.patch_get(patch_id)
    s = rpc.patch_get_mbox(patch_id)

    if patch == {} or len(s) == 0:
        sys.stderr.write("Unable to get patch %d\n" % patch_id)
        sys.exit(1)

    base_fname = fname = os.path.basename(patch['filename'])
    i = 0
    while os.path.exists(fname):
        fname = "%s.%d" % (base_fname, i)
        i += 1

    with io.open(fname, 'w', encoding='utf-8') as f:
        f.write(s)
        print('Saved patch to %s' % fname)


def action_apply(rpc, patch_id, apply_cmd=None):
    patch = rpc.patch_get(patch_id)
    if patch == {}:
        sys.stderr.write("Error getting information on patch ID %d\n" %
                         patch_id)
        sys.exit(1)

    if apply_cmd is None:
        print('Applying patch #%d to current directory' % patch_id)
        apply_cmd = ['patch', '-p1']
    else:
        print('Applying patch #%d using %s' %
              (patch_id, repr(' '.join(apply_cmd))))

    print('Description: %s' % patch['name'])
    s = rpc.patch_get_mbox(patch_id)
    if len(s) > 0:
        proc = subprocess.Popen(apply_cmd, stdin=subprocess.PIPE)
        proc.communicate(s.encode('utf-8'))
        return proc.returncode
    else:
        sys.stderr.write("Error: No patch content found\n")
        sys.exit(1)


def action_update(rpc, patch_id, state=None, archived=None, commit=None):
    patch = rpc.patch_get(patch_id)
    if patch == {}:
        sys.stderr.write("Error getting information on patch ID %d\n" %
                         patch_id)
        sys.exit(1)

    params = {}

    if state:
        state_id = state_id_by_name(rpc, state)
        if state_id == 0:
            sys.stderr.write("Error: No State found matching %s*\n" % state)
            sys.exit(1)
        params['state'] = state_id

    if commit:
        params['commit_ref'] = commit

    if archived:
        params['archived'] = archived == 'yes'

    success = False
    try:
        success = rpc.patch_set(patch_id, params)
    except xmlrpclib.Fault as f:
        sys.stderr.write("Error updating patch: %s\n" % f.faultString)

    if not success:
        sys.stderr.write("Patch not updated\n")
