# -*- coding: utf-8 -*-
"""
---

title:
    "Placeholder no-op stableflow-edict component."

description:
    "Placeholder no-op component. Does nothing"

id:
    "bde45b4b-ed77-44ab-88d5-64ad2624dc69"

type:
    dt004_python_stableflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2022 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""


import asyncio
import copy
import hashlib
import json
import multiprocessing
import os
import queue
import textwrap

import discord
import discord.ext
import dotenv


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    signal = None

    # Load secrets from a .env file
    #
    filepath_self = os.path.realpath(__file__)
    dirpath_self  = os.path.dirname(filepath_self)
    filepath_env  = os.path.join(dirpath_self, '.env')
    dotenv.load_dotenv(dotenv_path = filepath_env,
                       verbose     = True,
                       override    = False)

    outputs['to_discord']['ena']  = False
    outputs['to_discord']['ts']   = dict()
    outputs['to_discord']['list'] = list()

    # State
    #
    map_ts_latest  = dict()
    map_cache      = dict()
    md5_prev       = None
    pending_report = None

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        outputs['to_discord']['ena'] = False
        outputs['to_discord']['ts'].clear()
        outputs['to_discord']['list'].clear()

        # Update the pending report if any new
        # information has been recieved.
        #
        if inputs['fileinfo']['ena']:

            map_ts_latest = inputs['fileinfo']['ts']
            map_cache     = _update_cache(map_cache    = map_cache,
                                          pkt_fileinfo = inputs['fileinfo'])
            map_summary   = _map_summary(map_cache = map_cache)
            md5_new       = _md5_hex_digest(map_data = map_summary)
            is_changed    = md5_new != md5_prev

            if is_changed:
                md5_prev       = md5_new
                pending_report = _str_report(map_summary)

        # Handle messages received from discord.
        #
        if inputs['from_discord']['ena']:
            for msg in inputs['from_discord']['list']:
                _handle_message_from_discord(msg)

        # Wait until a gap in the
        # stream of fileinfo updates
        # before publishing to the
        # client.
        #
        if pending_report and not inputs['fileinfo']['ena']:
            list_msg = [(cfg['id_chan_gen'], pending_report)]
            outputs['to_discord']['ena'] = True
            outputs['to_discord']['ts'].update(map_ts_latest)
            outputs['to_discord']['list'][:] = list_msg
            pending_report = None


# -----------------------------------------------------------------------------
def _update_cache(map_cache, pkt_fileinfo):
    """
    Update the map_cache data structure.

    This data structure contains the most
    up-to-date noncconformity information
    recieved.

    """
    map_ts = copy.deepcopy(pkt_fileinfo['ts'])

    for fileinfo in pkt_fileinfo['list']:

        filepath               = fileinfo['filepath']
        list_nonconformity     = fileinfo['list_nonconformity']
        id_fileinfo            = filepath
        count_nonconformity    = len(list_nonconformity)
        is_conforming          = count_nonconformity > 0
        map_cache[id_fileinfo] = dict(filepath            = filepath,
                                      ts_last_update      = map_ts,
                                      count_nonconformity = count_nonconformity,
                                      is_conforming       = is_conforming)

    return map_cache


# -----------------------------------------------------------------------------
def _map_summary(map_cache):
    """
    Build summary statistics of nonconformity information in the cache.

    TODO: MOST RECENT NONCONFORMITY

    """
    count_file_conforming    = 0
    count_file_nonconforming = 0
    count_nonconformity      = 0
    for item in map_cache.values():
        if item['is_conforming']:
            count_file_conforming += 1
        else:
            count_file_nonconforming += 1
        count_nonconformity += item['count_nonconformity']
    is_conforming = count_nonconformity == 0
    map_summary = dict(is_conforming            = is_conforming,
                       count_file_conforming    = count_file_conforming,
                       count_file_nonconforming = count_file_nonconforming,
                       count_nonconformity      = count_nonconformity)
    return map_summary


# -----------------------------------------------------------------------------
def _md5_hex_digest(map_data):
    """
    Return a non-cryptographic hex digest for the specified data structure.

    """
    hash_md5 = hashlib.md5()
    hash_md5.update(json.dumps(map_data, sort_keys = True).encode('utf-8'))
    return hash_md5.hexdigest()


# -----------------------------------------------------------------------------
def _str_report(map_summary):
    """
    Return a string with the formatted map_summary information.

    Format all of the messages
    that are to be passed on
    to the discord client.

    """
    if map_summary['is_conforming']:
        str_status = '**Conforming**'
        str_detail = '{num} files conform to the design rules.'.format(
                            num = map_summary['count_file_conforming'])
    else:
        str_status = '**Nonconforming**'
        str_detail = '{num} nonconformities in {file} files.'.format(
                            num  = map_summary['count_nonconformity'],
                            file = map_summary['count_file_nonconforming'])



    str_report = '>\n{status}\n{detail}'.format(status = str_status,
                                                detail = str_detail)

    return str_report


# -----------------------------------------------------------------------------
def _handle_message_from_discord(msg):
    """
    Handle messages received from discord.

    content':       'FOO',
    'id_author':    563330464220446726,
    'id_channel':   1050172081259692085,
    'id_msg':       1052532966796042270,
    'id_prev':      None}],
    """
    print(msg['content'])
