# -*- coding: utf-8 -*-
"""
---

title:
    "Discord HTTP API integration support module."

description:
    "This Python module is designed to interact
    with the Discord API using a separate process
    for handling requests and responses."

id:
    "08a41d6d-9b21-4248-b87a-9f4c7a003648"

type:
    dt003_python_module

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


import asyncio
import collections
import multiprocessing
import os
import queue

import fl.util


# -----------------------------------------------------------------------------
FileData = collections.namedtuple(
                'FileData', ['filename', 'spoiler', 'description', 'buffer'])


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(cfg_client):
    """
    Yield results for workflow coroutines sent to the OpenAI web API.

    Start the client in a separate process.

    """

    str_name_process = 'discord-bot'
    fcn_client       = _discord_client
    queue_to_app     = multiprocessing.Queue()  # stableflow --> client
    queue_from_app   = multiprocessing.Queue()  # client     --> stableflow
    queue_log        = multiprocessing.Queue()  # client     --> stableflow
    tup_args         = (cfg_client, queue_to_app, queue_from_app, queue_log)
    proc_client      = multiprocessing.Process(target = fcn_client,
                                               args   = tup_args,
                                               name   = str_name_process,
                                               daemon = True)  # So we get terminated
    proc_client.start()

    list_to_app   = list()
    list_from_app = list()
    list_log      = list()

    while True:

        (list_to_app) = yield (list_from_app, list_log)

        for tup_msg in list_to_app:
            try:
                queue_to_app.put(tup_msg, block = False)
            except queue.Full:
                pass  # TODO: LOG SOME SORT OF ERROR?

        # Retrieve any messages that
        # a user has input into the
        # discord client and forward
        # them to the rest of the
        # stableflow system for
        # further processing.
        #
        list_from_app.clear()
        while True:
            try:
                list_from_app.append(queue_from_app.get(block = False))
            except queue.Empty:
                break

        list_log.clear()
        while True:
            try:
                list_log.append(queue_log.get(block = False))
            except queue.Empty:
                break



# -----------------------------------------------------------------------------
def _discord_client(cfg_client, queue_to_app, queue_from_app, queue_log):
    """
    Run the discord client.

    """

    import io
    import logging
    import os

    import discord
    import discord.ext

    intents                 = discord.Intents.none()
    intents.guilds          = True
    intents.message_content = True
    intents.messages        = True
    intents.reactions       = True
    discord_client          = discord.Client(intents = intents)

    buffer_log = io.StringIO()
    loghandler = logging.StreamHandler(buffer_log)

    # -------------------------------------------------------------------------
    async def _service_msg_queue(cfg_client, queue_to_app, queue_log):
        """
        Message queue servicing coroutine.

        This coroutine is intended to
        run continuously, servicing
        the multiprocessing.queue
        instance that feeds messages
        from the rest of the system to
        the discord client.

        This coroutine is started from
        the on_ready callback - i.e as
        soon as the discord client is
        ready.

        """
        map_chan      = dict()
        secs_interval = cfg_client['secs_interval']

        while True:

            loghandler.flush()
            str_log = buffer_log.getvalue()
            if str_log:
                msg = dict(type = 'log',
                           msg  = str_log)
                try:
                    queue_log.put(msg, block = False)
                except queue.Full:
                    pass  # TODO: LOG SOME SORT OF ERROR?

            # Try to pull the next message
            # from the queue. If none are
            # available, then sleep for a
            # little while then try again.
            #
            try:
                tup_msg = queue_to_app.get(block = False)
            except queue.Empty:
                await asyncio.sleep(secs_interval)
                continue

            # If we have a new message to
            # handle, then simply send it
            # to the specified channel.
            #
            (id_chan, msg) = tup_msg
            if id_chan not in map_chan.keys() or map_chan[id_chan] is None:
                map_chan[id_chan] = discord_client.get_channel(id_chan)

            if map_chan[id_chan] is None:
                continue

            if isinstance(msg, str):
                await map_chan[id_chan].send(msg)
                continue

            if 'file' in msg and isinstance(msg['file'], FileData):

                file_data   = msg['file']
                msg['file'] = discord.File(
                                fp          = io.BytesIO(file_data.buffer),
                                filename    = file_data.filename,
                                spoiler     = file_data.spoiler,
                                description = file_data.description)

            await map_chan[id_chan].send(**msg)

    # -------------------------------------------------------------------------
    @discord_client.event
    async def on_ready():
        """
        Create worker tasks once the client is ready.

        This callback is invoked once the
        client is done preparing the data
        that has been received from Discord.
        This usually happens after login
        is successful and the Client.guilds
        and similar data structures are
        filled up.

        """

        task_msg = discord_client.loop.create_task(
                            coro = _service_msg_queue(
                                        cfg_client, queue_to_app, queue_log))

    # -------------------------------------------------------------------------
    @discord_client.event
    async def on_message(message):
        """
        Handle messages that are sent to the client.

        This coroutine is invoked
        whenever a message is created
        and sent.

        This coroutine is intended to
        simply forward the content of
        the message to the rest of the
        system via the queue_from_app
        queue.

        """

        if not message.author.bot:
            msg = dict(msg_type   = 'message',
                       id_prev    = None,
                       id_msg     = message.id,
                       id_author  = message.author.id,
                       id_channel = message.channel.id,
                       content    = message.content)
            try:
                queue_from_app.put(msg, block = False)
            except queue.Full:
                pass  # TODO: LOG SOME SORT OF ERROR?

    # -------------------------------------------------------------------------
    @discord_client.event
    async def on_message_edit(msg_before, msg_after):
        """
        Handle message-edits that are sent to the client.

        This coroutine is invoked
        whenever a message receives
        an update event. If the
        message is not found in the
        internal message cache, then
        these events will not be
        called.

        Messages might not be in
        cache if the message is
        too old or the client is
        participating in high
        traffic guilds.

        This coroutine is intended to
        simply forward the content of
        the message to the rest of the
        system via the queue_from_app
        queue.

        """

        if not msg_after.author.bot:
            try:
                msg = dict(msg_type   = 'message',
                           id_prev    = msg_before.id,
                           id_msg     = msg_after.id,
                           id_author  = msg_after.author.id,
                           id_channel = msg_after.channel.id,
                           content    = msg_after.content)
                queue_from_app.put(msg, block = False)
            except queue.Full:
                pass  # TODO: LOG SOME SORT OF ERROR?

    if cfg_client['debug']:
        discord_client.run(cfg_client['str_token'])
    else:
        discord_client.run(cfg_client['str_token'], log_handler = loghandler)
