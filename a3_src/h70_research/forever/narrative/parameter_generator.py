# -*- coding: utf-8 -*-
"""
---

title:
    "Narrative engine parameter generator."

description:
    "Parameter generator."

id:
    ""

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

list_param_preset = [
    dict(theme       = "Join Lily and her friends on a journey through time and space as they discover how our universe came to be.",
         style       = "Science-fiction adventure",
         inspiration = "The Magic School Bus by Joanna Cole and Bruce Degen",
         teaching    = "Lily and her friends learn about the big bang theory and the origins of the universe, emphasizing the importance of scientific curiosity and critical thinking.",
         age         = 9)]

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Parameter generator coroutine

    """

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

        # Output any new parameters which have
        # been generated.
        #
        if list_param_preset:
            outputs['param']['ena']     = True
            outputs['param']['list'][:] = [list_param_preset.pop()]
