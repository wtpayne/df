# -*- coding: utf-8 -*-
"""
---

title:
    "Routine app state store."

description:
    "Placeholder no-op component. Does nothing"

id:
    "15cf8553-fd47-42c7-beef-27ed1fa6d8e5"

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


import fl.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    signal = None

    outputs['state']['ena']  = False
    outputs['state']['ts']   = dict()
    outputs['state']['list'] = list()

    list_to_app = list()

    state = fl.util.Bureau()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        outputs['state']['ena'] = False
        outputs['state']['ts'].clear()
        outputs['state']['list'].clear()



