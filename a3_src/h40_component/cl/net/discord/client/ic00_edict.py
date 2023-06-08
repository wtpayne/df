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

    discord = init_discord_client(cfg)

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
        map_ts      = dict()
        list_to_app = list()
        for (id_in, pkt_in) in inputs.items():
            if pkt_in['ena']:
                map_ts = pkt_in['ts']
                list_to_app.extend(pkt_in['list'])

        list_from_app = discord.send(list_to_app)

        # If any messages have been
        # received from the discord
        # client, then place them
        # in the component output.
        #
        if list_from_app:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_from_app


# -----------------------------------------------------------------------------
def init_discord_client(cfg):
    """
    Return the discord client coroutine.

    """

    # Load secrets from a .env
    # file and load configuration.
    #
    dotenv.load_dotenv(dotenv_path = cfg['filepath_dotenv'],
                       verbose     = True,
                       override    = False)
    cfg_client                  = dict()
    cfg_client['str_token']     = os.environ[cfg['envvar_token']]
    cfg_client['secs_interval'] = cfg.get('secs_interval', 5)

    discord = fl.net.discord.client.coro(cfg_client)

    return discord
