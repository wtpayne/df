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

    # Initialize 'database' of prompt templates.
    #
    # Prompt templates are persisted
    # in memory so they don't need to
    # be provided anew at each time step.
    #
    # It is envisaged that the templates
    # will be updated from time to time
    # as part of a continuous improvement
    # process.
    #
    # We also keep a per-template token
    # budget, and a per-template record
    # of how many tokens have been spent
    # on that template as well.
    #
    map_map_template = dict()  # id_prompt -> dict with template & metadata.
    map_budget       = dict()  # id_prompt -> spend
    map_spend        = dict()  # id_prompt -> budget

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
            for map_map_tmpl_in in inputs['template']['list']:
                for (id_prompt, map_tmpl) in map_map_tmpl_in.items():
                    map_map_template[id_prompt] = map_tmpl

        # Add a spend record if none exists.
        #
        # TODO: Think about breaking down spend
        #       by template version, so we can
        #       track efficiency as templates
        #       change.
        #
        for id_prompt in map_map_template.keys():
            if id_prompt not in map_spend:
                map_spend[id_prompt] = 0

        # Apply parameters to prompt templates
        # to get prompts. Prompts are packaged
        # up alongside metadata in a 'request'
        # structure.
        #
        list_request = list()
        if inputs['param']['ena']:
            map_ts = inputs['param']['ts']
            for map_map_param in inputs['param']['list']:

                for id_prompt in map_map_param.keys():
                    if id_prompt not in map_map_template:
                        continue

                    # TODO: Check budget against spend and
                    #       discard the request if we've gone
                    #       over budget either for the template
                    #       or overall.
                    #
                    #       We also need a way of setting
                    #       and renewing the budget.
                    #
                    list_request.append(
                        _build_map_request(
                                    id_prompt    = id_prompt,
                                    map_template = map_map_template[id_prompt],
                                    map_param    = map_map_param[id_prompt]))

        # Send the request to the OpenAI API.
        #
        (list_result, list_error) = client.send(list_request)

        # Update the spend record.
        #
        # for result in list_result:
        #     id_prompt   = result['request']['_id_prompt']
        #     tokens_used = result['response']['usage']['total_tokens']
        #     map_spend[id_prompt] += tokens_used

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


# -----------------------------------------------------------------------------
def _build_map_request(id_prompt, map_template, map_param):
    """
    Return a map_request dict.

    """
    map_request = {
        '_id_prompt':  id_prompt,
        '_template':   map_template,
        '_param':      map_param,
        'messages':    [{
                'role':     'system',
                'content':  map_template['template'].format(**map_param)}]}

    if '_options' in map_param:
        map_request.update(**map_param['_options'])

    return map_request
