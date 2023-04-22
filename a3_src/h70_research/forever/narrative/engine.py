# -*- coding: utf-8 -*-
"""
---

title:
    "Narrative engine stableflow-edict component."

description:
    "The narrative engine"

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


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Narrative engine coroutine

    """
    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()


    id_prompt = 'test_prompt'

    list_template = list()
    list_param = list()

    def _add_param(id_prompt, **kwargs):
        list_param.append({id_prompt: kwargs})


    def _add_template(id_prompt, str_template):
        list_template.append({id_prompt: {'guid':      'test_guid_string',
                                          'version':   'test_version_string',
                                          'template':  str_template}})


    _add_template(id_prompt    = id_prompt,
                  str_template = 'Please tell me some facts about {topic}.')

    _add_param(id_prompt = id_prompt,
               topic     = 'Cars',
               _options  = { 'engine': 'text-curie-001' })
    _add_param(id_prompt = id_prompt, topic = 'Lorries')


    # Loop forever
    #
    while True:

        inputs = yield (outputs, signal)

        if inputs['result']['ena']:
            print('#' * 80)
            import pprint
            pprint.pprint(inputs['result'])
            print('#' * 80)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Output stuff.
        #
        if list_template:
            outputs['template']['ena']     = True
            outputs['template']['list'][:] = [list_template.pop()]

        if list_param:
            outputs['param']['ena']     = True
            outputs['param']['list'][:] = [list_param.pop()]



