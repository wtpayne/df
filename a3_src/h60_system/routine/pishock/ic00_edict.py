# -*- coding: utf-8 -*-
"""
---

title:
    "Pishock client component."

description:
    "Control a pishock device."

id:
    "95ce5b4b-c747-4504-a765-57cf31475d28"

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


import requests

import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Pishock client component coroutine.

    """

    # TODO: get APIKEY from env file.

    api_cfg = dict(username = 'kt',
                   name     = 'bot_test',
                   code     = '27CCAE8766B',
                   apikey   = 'cb79a7e8-3e22-4479-be8f-e1aa29e381de')

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Handle periodic summaries and reminders.
        #
        timestamp = None
        if not inputs['ctrl']['ena']:
            continue

        if inputs['command']['ena']:
            for map_cmd in inputs['command']['list']:
                _call_api(api_cfg,
                          operation = map_cmd['operation'],
                          duration  = map_cmd['duration'],
                          intensity = map_cmd['intensity'])


# -----------------------------------------------------------------------------
def _call_api(cfg, operation = 'beep', duration = 1, intensity = 0):
    """
    Call the pishock HTTP API.

    """

    if operation not in {'shock', 'vibrate', 'beep'}:
        raise RuntimeError('Bad operation value: {operation}'.format(
                                                        operation = operation))

    if (duration < 1) or (15 < duration):
        raise RuntimeError('Duration out of range: {duration}'.format(
                                                        duration = duration))

    if (intensity < 1) or (100 < intensity):
        raise RuntimeError('Intensity out of range: {intensity}'.format(
                                                        intensity = intensity))

    MAP_OPERATION  = dict(shock   = 0,
                          vibrate = 1,
                          beep    = 2):
    session        = requests.Session()
    session.params = dict(Username  = cfg['username'],
                          Name      = cfg['name'],
                          Code      = cfg['code'],
                          Apikey    = cfg['apikey'],
                          Intensity = intensity,
                          Duration  = duration,
                          Op        = MAP_OPERATION[operation])
    response = session.post(url  = 'https://do.pishock.com/api/apioperate',
                            json = session.params)
    return [response.status_code, response.text]
