# -*- coding: utf-8 -*-
"""
---

title:
    "Application logic stableflow-edict component."

description:
    "TBD"

id:
    "b547ad43-aefe-4a76-9de7-14974e3329c6"

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


import textwrap

import fl.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    OpenAI agent coroutine.

    """

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    map_ts        = dict()
    list_user     = list()  # UI --> applogic
    list_workflow = list()  # applogic --> LLM (sometimes)
    list_param    = list()  # applogic --> LLM (often)
    list_result   = list()  # LLM --> applogic
    list_error    = list()  # LLM --> applogic
    list_auto     = list()  # applogic --> UI

    applogic = _applogic(cfg)

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # GRAB INPUTS
        # ===========

        if inputs['user']['ena']:
            map_ts       = inputs['user']['ts']
            list_user[:] = inputs['user']['list']
        else:
            list_user.clear()

        if inputs['result']['ena']:
            list_result[:] = inputs['result']['list']
        else:
            list_result.clear()

        if inputs['error']['ena']:
            list_error[:] = inputs['error']['list']
        else:
            list_error.clear()

        # RUN APPLICATION LOGIC
        # =====================

        (list_workflow,
         list_param,
         list_auto) = applogic.send((list_user,
                                     list_result,
                                     list_error))

        # SEND OUTPUTS
        # ============

        if list_workflow:
            outputs['workflow']['ena'] = True
            outputs['workflow']['ts'].update(map_ts)
            outputs['workflow']['list'][:] = list_workflow
            list_workflow.clear()

        if list_param:
            outputs['param']['ena'] = True
            outputs['param']['ts'].update(map_ts)
            outputs['param']['list'][:] = list_param
            list_param.clear()

        if list_auto:
            outputs['auto']['ena'] = True
            outputs['auto']['ts'].update(map_ts)
            outputs['auto']['list'][:] = list_auto
            list_auto.clear()


# -----------------------------------------------------------------------------
@fl.util.coroutine
def _applogic(cfg):
    """
    """

    list_user     = list()  # UI --> applogic
    list_workflow = list()  # applogic --> LLM (sometimes)
    list_param    = list()  # applogic --> LLM (often)
    list_result   = list()  # LLM --> applogic
    list_error    = list()  # LLM --> applogic
    list_auto     = list()  # applogic --> UI

    uid_workflow = 'e6150ce3-8ebc-4553-9a9a-b1ebdc038f7e'
    coro         = _coro_workflow()
    coro.send(None)
    list_workflow.append({
        'uid_workflow':     uid_workflow,
        'type':             {'id': 'prompt_workflow', 'ver': '1.0'},
        'coroutine':        coro,
        'spec':             None
    })

    while True:

        (list_user,
         list_result,
         list_error) = yield (list_workflow,
                              list_param,
                              list_auto)

        if list_result:
            response         = list_result[0]['response']
            response_content = response['choices'][0]['message']['content']
            list_auto.append(response_content)

            print('<' * 80)
            import pprint
            pprint.pprint(list_result)
            print('>' * 80)


        if list_user:

            uid_params        = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
            uid_template      = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'

            list_param.append({
                'type':             {'id': 'prompt_params', 'ver': '1.0'},
                'uid_params':       uid_params,
                'uid_template':     uid_template,
                'uid_workflow':     uid_workflow,
                'kwargs_tmpl':      dict(), # <-- Args for template
                'kwargs_req':       dict(), # <-- Args for OpenAI request
                'state':            dict()}) # <-- Process state




# -----------------------------------------------------------------------------
def _coro_workflow():
    """
    """
    list_param_in     = list()
    list_result_in    = list()
    list_error_in     = list()
    list_template_out = list()
    list_param_out    = list()
    list_error_out    = list()

    id_endpoint       = 'chat_completions'
    uid_workflow      = 'e6150ce3-8ebc-4553-9a9a-b1ebdc038f7e'
    uid_template      = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant       = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params        = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model          = 'gpt-3.5-turbo-0301'
    messages_test     = [{'role':    'user',
                          'content': 'Please say hello to {name}'}]

    template = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_variant':      uid_variant,  # Improvement.
        'uid_template':     uid_template, # Process step.
        'uid_workflow':     uid_workflow, # Process id.
        'kwargs_req':       {'model': id_model},
        'messages':         messages_test }

    list_template_out.append(template)

    while True:

        list_param_in.clear()
        list_result_in.clear()
        list_error_in.clear()

        (list_param_in,
         list_result_in,
         list_error_in) = yield (list_template_out,
                                 list_param_out,
                                 list_error_out)

        list_template_out.clear()
        list_param_out.clear()
        list_error_out.clear()

        list_param_out[:] = list_param_in

