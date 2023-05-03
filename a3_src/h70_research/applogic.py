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

    while True:

        list_auto = ['TEST STRING']

        (list_user,
         list_result,
         list_error) = yield (list_workflow,
                              list_param,
                              list_auto)



