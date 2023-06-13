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
import io
import zoneinfo

import discord
import matplotlib.pyplot
import numpy
import pandas
import thefuzz.process

import fl.util
import fl.net.discord.client



# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    signal = None

    outputs['msg']['ena']  = False
    outputs['msg']['ts']   = dict()
    outputs['msg']['list'] = list()

    outputs['state']['ena']  = False
    outputs['state']['ts']   = dict()
    outputs['state']['list'] = list()

    state = fl.util.Bureau()
    state.cfg.from_dict(cfg)

    state.set_keyphrase = set()
    state.map_keyphrase = dict()
    for (id_event, iter_keyphrase) in state.cfg.events.items():
        state.set_keyphrase.update(iter_keyphrase)
        for keyphrase in iter_keyphrase:
            state.map_keyphrase[keyphrase] = id_event

    state.set_daily_summary = set()

    list_to_app = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        outputs['msg']['ena'] = False
        outputs['msg']['ts'].clear()
        outputs['msg']['list'].clear()

        outputs['state']['ena']  = False
        outputs['state']['ts'].clear()
        outputs['state']['list'].clear()

        list_to_app.clear()

        # Handle periodic summaries and reminders.
        #
        if inputs['control']['ena']:
            list_to_app.extend(_messages_due_to_be_sent(
                                        state     = state,
                                        timestamp = inputs['control']['ts']))

        # Handle messages received from discord.
        #
        if inputs['msg']['ena']:
            for map_msg in inputs['msg']['list']:
                list_to_app.extend(_process_incoming_message(
                                            state = state,
                                            ts    = inputs['control']['ts'],
                                            **map_msg))

        if list_to_app:
            outputs['msg']['ena'] = True
            outputs['msg']['ts'].clear()
            outputs['msg']['list'][:] = list_to_app


# -----------------------------------------------------------------------------
def _messages_due_to_be_sent(state, timestamp):
    """
    Return a list of messages which are due to be sent to the app.

    """

    list_message = list()
    id_day       = _id_day(timestamp)

    if id_day not in state.set_daily_summary:
        if _is_time_for_daily_summary(state, timestamp):
            tup_summary = _daily_summary(state)
            state.set_daily_summary.add(id_day)
            list_message.append(tup_summary)

    return list_message

# -----------------------------------------------------------------------------
def _daily_summary(state):
    """
    Return a daily summary message tuple.

    """

    file_data = fl.net.discord.client.FileData(
                            filename    = 'daily_summary.png',
                            spoiler     = False,
                            description = 'Daily Summary',
                            buffer      = _plot_daily_summary_as_png(state))

    payload = {
        'content': 'Test daily summary 8.',
        'file':    file_data
    }

    name_channel = state.cfg.daily_summary.channel
    id_channel   = state.cfg.channel[name_channel]
    tup_msg      = (id_channel, payload)
    return tup_msg


# -----------------------------------------------------------------------------
def _plot_daily_summary_as_png(state):
    """
    Return bytes representing the daily summary image

    """
    events = [
        (1623484800, 'event1'),  # '2023-06-12 08:00:00' UTC
        (1623486600, 'event2'),  # '2023-06-12 08:30:00' UTC
        (1623488400, 'event2'),  # '2023-06-12 09:00:00' UTC
        (1623490200, 'event3'),  # '2023-06-12 09:30:00' UTC
    ]

    tz_utc     = datetime.timezone.utc

    events = [(datetime.datetime.fromtimestamp(ts, tz_utc), event) for ts, event in events]

    EVENT_COLORS = {
        'event1': 'red',
        'event2': 'orange',
        'event3': 'black',
        'event4': 'yellow',
    }

    # Convert list of events to dataframe
    frame = pandas.DataFrame(events, columns = ['timestamp', 'event'])
    frame.set_index('timestamp', inplace = True)

    # Resample the data to 30 minute intervals and get the most frequent event
    resampled = frame.resample('30T').apply(lambda x: x.value_counts().idxmax() if len(x.value_counts())>0 else numpy.nan)

    # Create a color mapping for the resampled data
    color_mapping = resampled['event'].map(EVENT_COLORS)

    # Create a new figure
    matplotlib.pyplot.figure(figsize=(5, 10))

    # Iterate over each half hour and plot a colored bar
    for i, (time, color) in enumerate(color_mapping.items()):
        matplotlib.pyplot.barh(i, 1, color=color)

    matplotlib.pyplot.yticks(numpy.arange(0, 48, 2), [f'{h}:00' for h in range(24)])  # set y-axis labels
    matplotlib.pyplot.gca().invert_yaxis()  # invert y-axis

    # Save the plot as a PNG byte array
    buffer = io.BytesIO()
    matplotlib.pyplot.savefig(buffer, format='png')
    buffer.seek(0)
    bytes_fig = buffer.read()

    # Close the figure
    matplotlib.pyplot.close()


    # print(resampled)

    # filepath_fig = '/home/wtp/Pictures/Logos/Infinity.png'
    # with open(filepath_fig, 'rb') as file_fig:
    #     bytes_fig = file_fig.read()
    return bytes_fig


# -----------------------------------------------------------------------------
def _id_day(timestamp):
    """
    Return an id for a daily report.

    """
    return str(timestamp['id_day'])


# -----------------------------------------------------------------------------
def _is_time_for_daily_summary(state, timestamp):
    """
    Return True if it is time to deliver a daily summary.

    """

    tz_utc     = datetime.timezone.utc
    tz_cfg     = state.cfg.daily_summary.timezone
    secs_epoch = timestamp['unix_time']
    dt_utc     = datetime.datetime.fromtimestamp(secs_epoch, tz = tz_utc)
    dt_local   = dt_utc.astimezone(zoneinfo.ZoneInfo(tz_cfg))

    if dt_local.hour >= state.cfg.daily_summary.hour:
        return True
    else:
        return False


# -----------------------------------------------------------------------------
def _process_incoming_message(state,
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

    id_channel = 1115742503044386816
    return [(id_channel, response)]
