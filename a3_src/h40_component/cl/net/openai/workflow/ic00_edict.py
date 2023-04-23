# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI workflow automation stableflow-edict component."

description:
    "This component integrates with the OpenAI
    client to drive predefined workflows and to
    continuously improve them."

id:
    "0e7c1e6d-1368-4142-93eb-caf53dd4f552"

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


import fl.net.openai.workflow


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Narrative engine coroutine

    """

    # Initialize the workflow automation engine.
    #
    # This will generate new prompts
    #
    cfg_engine = dict()
    engine     = fl.net.openai.workflow.coro(cfg = cfg_engine)

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Loop forever
    #
    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Build list of input parameters
        # and feedback results from
        # previous steps.
        #
        has_param_input   = ('param'  in inputs) and inputs['param']['ena']
        list_param_input  = list()
        if has_param_input:
            list_param_input.extend(inputs['param']['list'])

        has_result_input  = ('result' in inputs) and inputs['result']['ena']
        list_result_input = list()
        if has_result_input:
            list_result_input.extend(inputs['result']['list'])

        # Step the workflow engine for each
        # input received.
        #
        list_templ_output    = list()
        list_param_output    = list()
        list_resource_output = list()
        for map_result in list_result_input:
            (list_template, list_param, list_resource) = engine.send((map_result, None))
            list_templ_output.extend(list_template)
            list_param_output.extend(list_param)
            list_resource_output.extend(list_resource)
        for map_param in list_param_input:
            (list_template, list_param, list_resource) = engine.send((None, map_param))
            list_templ_output.extend(list_template)
            list_param_output.extend(list_param)
            list_resource_output.extend(list_resource)

        # Output any new templates which have
        # been generated.
        #
        if list_templ_output:
            outputs['template']['ena']     = True
            outputs['template']['list'][:] = list_templ_output
        if list_param_output:
            outputs['param']['ena']        = True
            outputs['param']['list'][:]    = list_param_output
        if list_resource_output:
            outputs['resource']['ena']     = True
            outputs['resource']['list'][:] = list_resource_output
