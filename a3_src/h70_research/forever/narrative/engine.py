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


import cl.web.util


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

    map_res = cl.web.util.ResMap()

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

        map_res.json(
            story = '{"story": "Once upon a time, A narrative engine said Hello World"}')

        for id_out in outputs.keys():
            outputs[id_out]['ena']     = True
            outputs[id_out]['list'][:] = [dict(map_res)]

