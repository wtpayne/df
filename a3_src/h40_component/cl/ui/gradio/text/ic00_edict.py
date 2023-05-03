# -*- coding: utf-8 -*-
"""
---

title:
    "Gradio text input stableflow-edict component."

description:
    "Placeholder no-op component. Does nothing"

id:
    "c917c7be-064d-43b0-adfd-2a057834d51e"

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


import fl.ui.gradio.text


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    OpenAI agent coroutine.

    """

    ui = fl.ui.gradio.text.coro_ui(cfg)

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

        # Grab any new result inputs.
        #
        map_ts      = dict()
        list_result = list()
        if inputs['result']['ena']:
            map_ts      = inputs['result']['ts']
            list_result = inputs['result']['list']

        # Grab any new error inputs.
        #
        map_ts     = dict()
        list_error = list()
        if inputs['error']['ena']:
            map_ts     = inputs['error']['ts']
            list_error = inputs['error']['list']

        # Communicate with the UI.
        #
        (list_workflow,
         list_param) = ui.send((list_result,
                                list_error))

        # Update workflow outputs.
        #
        if ('workflow' in outputs) and list_workflow:
            outputs['workflow']['ena'] = True
            outputs['workflow']['ts'].update(map_ts)
            outputs['workflow']['list'][:] = list_workflow

        # Update param outputs.
        #
        if ('param' in outputs) and list_param:
            outputs['param']['ena'] = True
            outputs['param']['ts'].update(map_ts)
            outputs['param']['list'][:] = list_param
