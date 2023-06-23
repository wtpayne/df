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

import fl.net.discord.bot
import fl.util
import fl.util.edict


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    state = fl.util.Bureau()
    _reinit_state(state, cfg)

    signal = None
    fl.util.edict.init(outputs)
    while True:
        inputs = yield (outputs, signal)
        fl.util.edict.reset(outputs)

        # Load state. (should only happen at startup).
        #
        if inputs['state']['ena']:
            state = inputs['state']['list'][0]
            _reinit_state(state, cfg)
        state.has_changed = False

        # Handle periodic summaries and reminders.
        #
        timestamp = None
        if inputs['ctrl']['ena']:
            timestamp = inputs['ctrl']['ts']
            state.list_message_queue.extend(_messages_due_to_be_sent(
                                                        state     = state,
                                                        timestamp = timestamp))

        # Handle messages received from discord.
        #
        if inputs['msg']['ena']:
            for map_msg in inputs['msg']['list']:
                state.list_message_queue.extend(_process_incoming_message(
                                                            state = state,
                                                            ts    = timestamp,
                                                            **map_msg))

        # Handle command invocations recieved from discord.
        #
        if inputs['cmd']['ena']:
            for map_cmd in inputs['cmd']['list']:
<<<<<<< HEAD

                if map_cmd['name_command'] == 'shock':

                    print('SHOCK')

                # if map_cmd['name_command'] == 'diary':

                #     print('')
                #     print('')
                #     print(' +------------+')
                #     print(' | SHOW DIARY |')
                #     print(' +------------+')
                #     print('')
                #     print('')

                #     msg = 'Diary:\n\n'
                #     for (secs_epoch, str_event) in state.list_event_received:
                #         zone_utc    = datetime.timezone.utc
                #         utc_event   = datetime.datetime.fromtimestamp(secs_epoch, zone_utc)
                #         local_event = utc_event.astimezone(zoneinfo.ZoneInfo('Europe/London'))
                #         str_time    = local_event.strftime('%d %B - %H:%M')  # Customize the format as per your requirements

                #         msg += '\n  {time}: {evt}'.format(time = str_time,
                #                                           evt  = str_event)

                #     msg += '\n\n\u200B'

                #     id_channel  = state.cfg.channel['ctrl']
                #     state.list_message_queue.append(dict(type       = 'msg',
                #                                          id_channel = id_channel,
                #                                          msg        = msg))

                # if map_cmd['name_command'] == 'report':

                #     print('')
                #     print('')
                #     print(' +-----------------+')
                #     print(' | GENERATE REPORT |')
                #     print(' +-----------------+')
                #     print('')
                #     print('')

                #     map_message = _daily_summary(state, 'Europe/London')
                #     map_message['type']       = 'msg'
                #     map_message['id_channel'] = int(state.cfg.channel['control'])
                #     state.list_message_queue.append(map_message)
=======
                if map_cmd['name_command'] == 'diary':

                    print('')
                    print('')
                    print(' +------------+')
                    print(' | SHOW DIARY |')
                    print(' +------------+')
                    print('')
                    print('')

                    msg = 'Diary:\n\n'
                    for (secs_epoch, str_event) in state.list_event_received:
                        zone_utc    = datetime.timezone.utc
                        utc_event   = datetime.datetime.fromtimestamp(secs_epoch, zone_utc)
                        local_event = utc_event.astimezone(zoneinfo.ZoneInfo('Europe/London'))
                        str_time    = local_event.strftime('%d %B - %H:%M')  # Customize the format as per your requirements

                        msg += '\n  {time}: {evt}'.format(time = str_time,
                                                          evt  = str_event)

                    msg += '\n\n\u200B'

                    id_channel  = state.cfg.channel['ctrl']
                    state.list_message_queue.append((id_channel, msg))

                if map_cmd['name_command'] == 'report':

                    print('')
                    print('')
                    print(' +-----------------+')
                    print(' | GENERATE REPORT |')
                    print(' +-----------------+')
                    print('')
                    print('')

                    id_channel  = state.cfg.channel['ctrl']
                    map_message = _daily_summary(state, 'Europe/London')
                    state.list_message_queue.append((id_channel, map_message))
>>>>>>> f667730 (Add routine app)

        # Output messages to discord.
        #
        if (timestamp is not None):
            _update_output(state, timestamp, outputs)


# -----------------------------------------------------------------------------
def _reinit_state(state, cfg):
    """
    Reset application state at startup or reinitialization.

    """

    # Re-load configuration.
    #
    state.cfg.from_dict(cfg)

    # Rebuild data structures to use when
    # detecting and interpreting keyphrases,
    # and also when producing color coded
    # charts.
    #
    state.list_keyphrase = list()  # Used to build set of keyphrases.
    state.map_keyphrase  = dict()  # keyphrase --> id_event
    state.list_id_event  = list()  # id_event sort order
    state.map_color      = dict()  # id_event --> color lookup
    for cfg_event in state.cfg.event.values():

        id_event       = cfg_event.id_event
        iter_keyphrase = cfg_event.keyphrase
        color          = cfg_event.color

        state.list_id_event.append(id_event)
        state.map_color[id_event] = color

        for keyphrase in iter_keyphrase:
            state.map_keyphrase[keyphrase] = id_event
            state.list_keyphrase.append(keyphrase)

    # Keep a record of the events that we have
    # recieved from the user. If it already
    # exists, keep it as-is.
    #
    if 'list_event_received' not in state:
        state.list_event_received = list()

    # Keep a list of scheduled messages that
    # have been sent so we can make sure that
    # we don't send duplicate messages. If the
    # schedule changes at all, then clear it
    # and repopulate (as we only use indices to
    # identify scheduled events at the moment).
    #
    if 'list_schedule_sent' not in state:
        state.list_schedule_sent  = list()

    count_schedule_items = len(state.cfg.schedule)
    if len(state.list_schedule_sent) != count_schedule_items:
        state.list_schedule_sent = list()
        for idx in range(count_schedule_items):
            state.list_schedule_sent.append(list())

    # Queue for outbound messages and a
    # timestamp to allow us to rate
    # limit ourselves.
    #
    state.list_message_queue = list()
    state.time_last_message  = 0.0

    # Queue for outbound command configuration.
    #
    state.list_command_config_queue = list()
    state.list_command_config_queue.extend([
<<<<<<< HEAD
        dict(name        = 'shock',
             description = 'Shock command.')])
        # dict(name        = 'report',
        #      description = 'Generate a report.'),
        # dict(name        = 'diary',
        #      description = 'List recorded events.')])
=======
        dict(name        = 'report',
             description = 'Generate a report.'),
        dict(name        = 'diary',
             description = 'List recorded events.')])
>>>>>>> f667730 (Add routine app)

    # Boolean flag to control saving.
    #
    state.has_changed = False

<<<<<<< HEAD
    # print('')
    # print('#' * 80)
    # print('#' * 80)
    # print('')
    # import pprint
    # pprint.pprint(state.to_dict())
    # print('')
    # print('#' * 80)
    # print('#' * 80)
    # print('')
=======
    print('')
    print('#' * 80)
    print('#' * 80)
    print('')
    import pprint
    pprint.pprint(state.to_dict())
    print('')
    print('#' * 80)
    print('#' * 80)
    print('')


# -----------------------------------------------------------------------------
def _init_output(outputs, tup_id_out):
    """
    """
    for id_out in tup_id_out:
        if id_out in outputs:
            outputs[id_out]['ena']  = False
            outputs[id_out]['ts']   = dict()
            outputs[id_out]['list'] = list()


# -----------------------------------------------------------------------------
def _reset_output(outputs, tup_id_out):
    """
    """
    for id_out in ('msg', 'cmd', 'state'):
        if id_out in outputs:
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()
>>>>>>> f667730 (Add routine app)


# -----------------------------------------------------------------------------
def _update_output(state, timestamp, outputs):
    """
    Update outputs data structure with information from state.

    """

    if state.list_message_queue:
        secs_since_last = timestamp['unix_time'] - state.time_last_message
        is_rate_limited = secs_since_last < state.cfg.rate_limit_secs
        if not is_rate_limited:
            outputs['msg']['ena']     = True
            outputs['msg']['ts']      = timestamp
            outputs['msg']['list'][:] = [state.list_message_queue.pop(0)]
            state.has_changed         = True
            state.time_last_message   = timestamp['unix_time']

    if state.list_command_config_queue:
<<<<<<< HEAD
        outputs['cfg_cmd']['ena']     = True
        outputs['cfg_cmd']['ts']      = timestamp
        outputs['cfg_cmd']['list'][:] = [state.list_command_config_queue.pop(0)]
        state.has_changed             = True
=======
        outputs['cmd']['ena']     = True
        outputs['cmd']['ts']      = timestamp
        outputs['cmd']['list'][:] = [state.list_command_config_queue.pop(0)]
        state.has_changed         = True
>>>>>>> f667730 (Add routine app)

    if state.has_changed:
        outputs['state']['ena']     = True
        outputs['state']['ts']      = timestamp
        outputs['state']['list'][:] = [state]


# -----------------------------------------------------------------------------
def _messages_due_to_be_sent(state, timestamp):
    """
    Return a list of messages which are due to be sent to the app.

    """

    list_message = list()

    for (idx, item) in enumerate(state.cfg.schedule.values()):

        if not _is_message_due(state, timestamp, idx):
            continue

        state.has_changed = True

        if item.type == 'mantra':
            id_channel  = state.cfg.channel[item.channel]
            str_mantra  = state.cfg[item.message]
            str_prefix  = 'Time for you to say your mantra:-'
            str_message = '{prefix}\n\n*"{example}"*\n\n\u200B'.format(
                                                        prefix  = str_prefix,
                                                        example = str_mantra)
            map_message = { 'content': str_message }
            list_message.append((id_channel, map_message))

        if item.type == 'summary':
            id_channel  = state.cfg.channel[item.channel]
            map_message = _daily_summary(state, item.tz_report)
            list_message.append((id_channel, map_message))

    return list_message


# -----------------------------------------------------------------------------
def _is_message_due(state, timestamp, idx):
    """
    Return True if the specified message is due, False otherwise.

    This function checks if it's time to send a
    message based on the hour and timezone
    specified in the configured schedule.\

    If it is time, and if the message has not
    been sent in this hour, the function
    indicates that the message is due by
    returning True.

    It also updates the state to mark that the
    message will be sent. If it's not time, or
    if the message has already been sent, the
    function indicates that the message is not
    due by returning False.

    """
    msg = state.cfg.schedule[idx]
    utc = datetime.datetime.fromtimestamp(timestamp = timestamp['unix_time'],
                                          tz        = datetime.timezone.utc)
    now = utc.astimezone(zoneinfo.ZoneInfo(msg.timezone))

    for msg_hour in sorted(msg.hour):

        if (now.hour != msg_hour):
            continue

        id_hour         = timestamp['id_hour']
        is_already_sent = id_hour in state.list_schedule_sent[idx]
        if is_already_sent:
            continue

        state.list_schedule_sent[idx].append(id_hour)
        return True

    return False


# -----------------------------------------------------------------------------
def _daily_summary(state, timezone):
    """
    Return a daily summary message dict.

    """
    if not state.list_event_received:
        return { 'content': 'No events recorded.' }

    return {
        'content': _compose_daily_summary(state, timezone),
        'file':    fl.net.discord.bot.FileData(
                        filename    = 'daily_summary.png',
                        spoiler     = False,
                        description = 'Daily Summary',
                        buffer      = plot_summary_chart(state, timezone))}


# -----------------------------------------------------------------------------
def _compose_daily_summary(state, timezone):
    """
    Return a string representing the daily summary.

    """

    # Convert timezone to local time.
    #
    list_local = list()
    for (secs_epoch, id_event) in state.list_event_received:
        zone_utc    = datetime.timezone.utc
        utc_event   = datetime.datetime.fromtimestamp(secs_epoch, zone_utc)
        local_event = utc_event.astimezone(zoneinfo.ZoneInfo(timezone))
        list_local.append((local_event, id_event))

    # Convert to dataframe and index by time.
    #
    df_local = pandas.DataFrame(data    = list_local,
                                columns = ['timestamp', 'id_event'])
    df_local.set_index('timestamp', inplace = True)

    str_date  = df_local.index.max().strftime('%B %d')
    str_title = 'Summary for {date}'.format(date = str_date)
    str_count = 'There were {count} events recorded.'.format(
                                        count = len(state.list_event_received))

    str_summary = '{title}\n\n{count}'.format(title = str_title,
                                              count = str_count)

    return str_summary


# -----------------------------------------------------------------------------
def plot_summary_chart(state, timezone):
    """
    Return bytes representing the daily summary image

    """

    # Convert timezone to local time.
    #
    list_local = list()
    for (secs_epoch, id_event) in state.list_event_received:
        zone_utc    = datetime.timezone.utc
        utc_event   = datetime.datetime.fromtimestamp(secs_epoch, zone_utc)
        local_event = utc_event.astimezone(zoneinfo.ZoneInfo(timezone))
        list_local.append((local_event, id_event))

    # Convert to dataframe and index by time.
    #
    df_local = pandas.DataFrame(data    = list_local,
                                columns = ['timestamp', 'id_event'])
    df_local.set_index('timestamp', inplace = True)

    # Get the date. We will use this as the figure title.
    #
    str_date = df_local.index.max().strftime('%B %d')

    # Group events into one-hour bins.
    #
    one_hour       = '1H'
    events_by_hour = df_local['id_event'].resample(one_hour).apply(list)
    count_hour     = len(events_by_hour)
    max_per_hour   = max([len(list_event) for list_event in events_by_hour])

    # Lookup table for colours.
    #
    list_id_event = list(item.id_event for item in state.cfg.event.values())

    # Create a figure and axis and plot patches.
    #
    figure = matplotlib.pyplot.figure(figsize = (10, 10))
    axis   = figure.gca()

    # Create patches.
    #
    for (idx_hour, list_event) in enumerate(events_by_hour):

        # Define a sort order for events.
        #
        list_event.sort(key = list_id_event.index)

        for (idx_event, id_event) in enumerate(list_event):

            x_min = idx_event
            y_min = idx_hour
            x_mid = x_min + 0.5
            y_mid = y_min + 0.5

            axis.add_patch(matplotlib.patches.Rectangle(
                                        xy     = (x_min, y_min),
                                        width  = 1,
                                        height = 1,
                                        color  = state.map_color[id_event]))
            axis.text(x = x_mid,
                      y = y_mid,
                      s = id_event,
                      horizontalalignment = 'center',
                      verticalalignment   = 'center')

    axis.set_title('Summary for {date}.'.format(date = str_date))

    axis.set_xlim(0, max_per_hour)
    axis.set_ylim(0, 24)

    x_labels = ['{idx}'.format(idx = idx) for idx in range(max_per_hour)]
    axis.set_xticks(numpy.arange(0, max_per_hour, 1))
    axis.set_xticklabels(x_labels)

    y_labels = ['{hour}:00'.format(hour = hour) for hour in range(24)]
    axis.set_yticks(numpy.arange(0, 24, 1))
    axis.set_yticklabels(y_labels)
    axis.invert_yaxis()

    # DEBUG
    # matplotlib.pyplot.show()
    # DEBUG

    bytes_buffer = _save_figure_to_bytes(figure = figure, format = 'png')

    return bytes_buffer


# -----------------------------------------------------------------------------
def _save_figure_to_bytes(figure, format = 'png'):
    """
    Return the matplotlib figure as a saved image in a bytes string.

    Args:

        fig (matplotlib.figure.Figure):     Matplotlib figure handle

        format (str, optional):             Desired output format. Defaults
                                            to 'png'.

    Returns:

        bytes:  Byte representation of the figure.

    """

    io_buffer = io.BytesIO()
    figure.savefig(io_buffer, format = 'png', dpi = 60)
    io_buffer.seek(0)
    bytes_buffer = io_buffer.read()
    matplotlib.pyplot.close(figure)
    return bytes_buffer


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
    print('ON MESSAGE!!!!! (D)')

    dt_utc             = datetime.datetime.fromtimestamp(ts['unix_time'])
    str_time           = dt_utc.strftime('%H:%M')
    set_keyphrase      = {item for item in state.list_keyphrase}
    (keyphrase, score) = thefuzz.process.extractOne(content, set_keyphrase)

    if keyphrase not in set_keyphrase:
        print('KEYPHRASE NOT FOUND!')
        return []

    id_event = state.map_keyphrase[keyphrase]

    if not isinstance(state.list_event_received, list):
        state.list_event_received = [item for item in state.list_event.values()]

    state.list_event_received.append((ts['unix_time'], id_event))
    state.has_changed = True

    response = 'event: {id} registered at {ts}. (total = {count})'.format(
                                        id    = id_event,
                                        ts    = str_time,
                                        count = len(state.list_event_received))

    return [(state.cfg.channel.report, response)]
