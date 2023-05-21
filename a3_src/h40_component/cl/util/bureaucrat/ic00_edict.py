# -*- coding: utf-8 -*-
"""
---

title:
    "Bureaucrat stableflow-edict component."

description:
    "Configurable node for filtering, routing
    and synchronizing hierarchical data."

id:
    "abe9ba5c-2d14-4405-aa22-69213fc6afa7"

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


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Bureaucrat coroutine.

    """

    # We distinguish between 'administrative'
    # inputs and 'operational' inputs.
    #
    # Operational inputs are assumed to
    # hold batches of Bureau data structure
    # updates, whereas administrative inputs
    # either hold control signals or rules.
    #
    set_input_all            = set(inputs.keys())
    set_input_administrative = {'control',}
    for key in set_input_all:
        if key.endswith('rule'):
            set_input_administrative.add(key)

    set_input_operational = set_input_all - set_input_administrative
    tup_input_operational = tuple(sorted(set_input_operational))

    # Data.
    #
    data = fl.util.Bureau()

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

        map_ts = dict()
        if inputs['control']['ena']:
            map_ts = inputs['control']['ts']

        # Configure rules
        #
        if inputs['rule']['ena']:
            for rule in inputs['rule']['list']:
                data.rule(rule)

        # Update data from operational inputs.
        #
        with data.batch_context() as batch:
            for key in tup_input_operational:
                data.from_batch(inputs[key]['list'])

        # Update outputs with outgoing user provided data.
        #
        if batch:
            for key in outputs.keys():
                outputs[key]['ena'] = True
                outputs[key]['ts'].update(map_ts)
                outputs[key]['list'][:] = batch
