# -*- coding: utf-8 -*-
"""
---

title:
    "Discord client stableflow-edict component."

description:
    "This component enables integration with the
    Discord HTTP API."

id:
    "8747de1c-76ac-4f63-a88d-f67a60515571"

type:
    dt004_python_stableflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

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


import dotenv
import os

import fl.net.discord.client
import key


DEFAULT_ENVVAR = 'TOKEN_DISCORD_BOT_DEFAULT'


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    discord = init_discord_client(
                filepath_env  = cfg.get('filepath_env',  None),
                envvar_key    = cfg.get('envvar_key',    DEFAULT_ENVVAR),
                str_token     = cfg.get('str_token',     None),
                secs_interval = cfg.get('secs_interval', 5),
                debug         = cfg.get('debug',         False))

    # Loop forever, sending messages
    # to and from the discord client
    # via the two message queues.
    #
    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Take any messages that
        # we recieve from the rest
        # of the stableflow system
        # and forward them on to
        # the discord client so that
        # they can be printed in
        # the specified channel.
        #
        map_ts          = dict()
        list_msg_to_bot = list()
        list_cmd_to_bot = list()
        for (id_in, pkt_in) in inputs.items():
            if pkt_in['ena']:
                map_ts = pkt_in['ts']
                list_msg_to_bot.extend(pkt_in['list'])

        (list_msg_from_bot,
         list_cmd_from_bot,
         list_log_from_bot) = discord.send((list_msg_to_bot,
                                            list_cmd_to_bot))

        # If any messages have been
        # received from the discord
        # client, then place them
        # in the component output.
        #
        if list_msg_from_bot:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_msg_from_bot

            print('ON MESSAGE!!!!! (C)')

        if list_cmd_from_bot:
            pass

        if list_log_from_bot:
            pass


# -----------------------------------------------------------------------------
def init_discord_client(filepath_env  = None,
                        envvar_key    = DEFAULT_ENVVAR,
                        str_token     = None,
                        secs_interval = 5,
                        debug         = False):
    """
    Return the discord client coroutine.

    """

    if str_token is None:
        str_token = key.load(id_value     = envvar_key,
                             filepath_env = filepath_env)

    cfg_client = { 'secs_interval': secs_interval,
                   'str_token':     str_token,
                   'debug':         debug }

    discord    = fl.net.discord.client.coro(cfg_client)

    return discord
