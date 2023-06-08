# -*- coding: utf-8 -*-
"""
---

title:
    "Routine app engine component."

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


import datetime
import zoneinfo

import thefuzz.process

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
    state.cfg.from_dict(cfg)

    state.set_keyphrase = set()
    state.map_keyphrase = dict()
    for (id_event, iter_keyphrase) in state.cfg.events.items():
        state.set_keyphrase.update(iter_keyphrase)
        for keyphrase in iter_keyphrase:
            state.map_keyphrase[keyphrase] = id_event

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
            list_to_app.extend(_get_daily_summary(
                                            state = state,
                                            ts    = inputs['control']['ts']))

        # Handle messages received from discord.
        #
        if inputs['msg']['ena']:
            for map_msg in inputs['msg']['list']:
                list_to_app.extend(_process_message(
                                            state = state,
                                            ts    = inputs['control']['ts'],
                                            **map_msg))

        if list_to_app:
            outputs['msg']['ena'] = True
            outputs['msg']['ts'].clear()
            outputs['msg']['list'][:] = list_to_app


# -----------------------------------------------------------------------------
def _get_daily_summary(state, ts):
    """
    """

    tz_utc = datetime.timezone.utc
    tz_cfg = state.cfg.daily_summary.timezone
    NOOP   = []

    id_summary = str(ts['id_day'])
    if id_summary in state.summary:
        return NOOP

    dt_utc   = datetime.datetime.fromtimestamp(ts['unix_time'], tz = tz_utc)
    dt_local = dt_utc.astimezone(zoneinfo.ZoneInfo(tz_cfg))

    if dt_local.hour < state.cfg.daily_summary.hour:
        return NOOP

    state.summary[id_summary] = _prepare_daily_summary(state, ts)

    id_channel = 1115742663002554503

    return [(id_channel,state.summary[id_summary])]


# -----------------------------------------------------------------------------
def _prepare_daily_summary(state, ts):
    """
    """

    return "Summary"


# -----------------------------------------------------------------------------
def _process_message(state,
                     ts,
                     msg_type,
                     id_author,
                     id_channel,
                     id_msg,
                     id_prev,
                     content):
    """
    """

    dt_utc   = datetime.datetime.fromtimestamp(ts['unix_time'])
    str_time = dt_utc.strftime('%H:%M')

    (keyphrase, score) = thefuzz.process.extractOne(
                                                content, state.set_keyphrase)

    id_event = state.map_keyphrase[keyphrase]
    response = 'event: {id} registered at {ts}'.format(id = id_event,
                                                       ts = str_time)

    print(response)

    id_channel = 1115742503044386816
    return [(id_channel, response)]


