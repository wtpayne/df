# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI agent stableflow-edict component."

description:
    "This component enables communication with
    the OpenAI web API."

id:
    "8d2b1939-cea9-4af0-9528-7cc5e44d0a5c"

type:
    dt004_python_stableflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2023 William Payne"

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


import os

import dotenv

import fl.net.openai.client


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    OpenAI agent coroutine.

    """

    # Initialize the OpenAI client coroutine
    # using an API key loaded from a .env
    # file in configured location.
    #
    dotenv.load_dotenv(dotenv_path = cfg['filepath_env'],
                       verbose     = True,
                       override    = False)

    cfg_client                   = dict()
    cfg_client['api_key']        = os.environ[cfg['envvar_key']]
    cfg_client['secs_interval']  = cfg.get('secs_interval', 5)
    cfg_client['default']        = cfg['default']
    client = fl.net.openai.client.coro(cfg = cfg_client)

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Update map_map_template with new
        # and updated templates. Any old
        # templates with the same id_prompt
        # get overwritten.
        #
        map_ts = dict()
        if inputs['template']['ena']:
            map_ts = inputs['template']['ts']
            # for map_map_tmpl_in in inputs['template']['list']:
            #     for (id_prompt, map_tmpl) in map_map_tmpl_in.items():
            #         map_map_template[id_prompt] = map_tmpl



        # Send the request to the OpenAI API.
        #
        (list_result, list_error) = client.send(list_request)

        # Update the spend record.
        #
        for result in list_result:
            try:
                id_prompt   = result['request']['_id_prompt']
                tokens_used = result['response']['usage']['total_tokens']
                map_spend[id_prompt] += tokens_used
            except (KeyError, TypeError):
                pass

        # Update outputs.
        #
        if ('result' in outputs) and list_result:
            outputs['result']['ena'] = True
            outputs['result']['ts'].update(map_ts)
            outputs['result']['list'][:] = list_result
        if ('error' in outputs) and list_error:
            outputs['error']['ena'] = True
            outputs['error']['ts'].update(map_ts)
            outputs['error']['list'][:] = list_error


