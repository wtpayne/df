# -*- coding: utf-8 -*-
"""
---

title:
    "Accprd app engine component."

description:
    "Placeholder no-op component. Does nothing"

id:
    "23d9e2e5-303c-41ea-8815-40a9690d86b3"

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

    outputs['msg']['ena']  = False
    outputs['msg']['ts']   = dict()
    outputs['msg']['list'] = list()

    list_to_app = list()

    state = fl.util.Bureau()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        outputs['msg']['ena'] = False
        outputs['msg']['ts'].clear()
        outputs['msg']['list'].clear()

        list_to_app.clear()

        # Handle periodic reminders.
        #
        if inputs['control']['ena']:
            list_reminder = _get_announcements(state = state,
                                               ts    = inputs['control']['ts'])
            if list_reminder:
                list_to_app.extend(list_reminder)

        # Handle messages received from discord.
        #
        if inputs['msg']['ena']:
            for map_msg in inputs['msg']['list']:
                list_response = _process_message(state = state,
                                                 **map_msg)
                if list_response:
                    list_to_app.extend(list_response)

        if list_to_app:
            outputs['msg']['ena'] = True
            outputs['msg']['ts'].clear()
            outputs['msg']['list'][:] = list_to_app


# -----------------------------------------------------------------------------
def _get_announcements(state, ts):
    """
    """
    pass

# -----------------------------------------------------------------------------
def _process_message(state,
                     msg_type,
                     id_author,
                     id_channel,
                     id_msg,
                     id_prev,
                     content):
    """
    """
    print('ACCORD CONTENT: ' + content)