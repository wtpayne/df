# -*- coding: utf-8 -*-
"""
---

title:
    "Placeholder no-op steadyflow-edict component."

description:
    "Placeholder no-op component. Does nothing"

id:
    "8747de1c-76ac-4f63-a88d-f67a60515571"

type:
    dt004_python_steadyflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2022 William Payne"

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
import multiprocessing
import os
import queue

import dotenv


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Discord client component coroutine.

    """

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Load secrets from a .env
    # file and load configuration.
    #
    dotenv.load_dotenv(dotenv_path = cfg['filepath_env'],
                       verbose     = True,
                       override    = False)
    cfg_client                  = dict()
    cfg_client['str_token']     = os.environ[cfg['envvar_token']]
    cfg_client['secs_interval'] = cfg.get('secs_interval', 5)

    # Start the client in a separate process.
    #
    str_name_process  = 'discord-bot'
    fcn_client        = _discord_client
    queue_to_client   = multiprocessing.Queue()  # steadyflow --> client
    queue_from_client = multiprocessing.Queue()  # client     --> steadyflow
    tup_args          = (cfg_client, queue_to_client, queue_from_client)
    proc_client       = multiprocessing.Process(target = fcn_client,
                                                args   = tup_args,
                                                name   = str_name_process,
                                                daemon = True)  # So we get terminated
    proc_client.start()

    # Loop forever, sending messages
    # to and from the discord client
    # via the two message queues.
    #
    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Take any messages that
        # we recieve from the rest
        # of the steadyflow system
        # and forward them on to
        # the discord client so that
        # they can be printed in
        # the specified channel.
        #
        map_ts = dict()
        for (id_in, pkt_in) in inputs.items():
            if pkt_in['ena']:
                map_ts = pkt_in['ts']
                for tup_msg in pkt_in['list']:
                    try:
                        queue_to_client.put(tup_msg, block = False)
                    except queue.Full:
                        pass  # TODO: LOG SOME SORT OF ERROR?

        # Retrieve any messages that
        # a user has input into the
        # discord client and forward
        # them to the rest of the
        # steadyflow system for
        # further processing.
        #
        list_msg = list()
        while True:
            try:
                list_msg.append(queue_from_client.get(block = False))
            except queue.Empty:
                break

        # If any messages have been
        # received from the discord
        # client, then place them
        # in the component output.
        #
        if list_msg:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_msg


# -----------------------------------------------------------------------------
def _discord_client(cfg_client, queue_to_client, queue_from_client):
    """
    Run the discord client.

    """

    import io
    import logging

    import discord
    import discord.ext

    intents                 = discord.Intents.default()
    intents.message_content = True
    intents.messages        = True
    discord_client          = discord.Client(intents = intents)

    buffer_log = io.StringIO()
    loghandler = logging.StreamHandler(buffer_log)

    # -------------------------------------------------------------------------
    async def _service_msg_queue(cfg_client, queue_to_client):
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
            # TODO: - SEND ON A DIFFERENT QUEUE
            # if str_log:
            #     msg = dict(type = 'log',
            #                msg  = str_log)
            #     try:
            #         queue_from_client.put(msg, block = False)
            #     except queue.Full:
            #         pass  # TODO: LOG SOME SORT OF ERROR?


            # Try to pull the next message
            # from the queue. If none are
            # available, then sleep for a
            # little while then try again.
            #
            try:
                tup_msg = queue_to_client.get(block = False)
            except queue.Empty:
                await asyncio.sleep(secs_interval)
                continue

            # If we have a new message to
            # handle, then simply send it
            # to the specified channel.
            #
            (id_chan, msg) = tup_msg
            if id_chan not in map_chan.keys():
                map_chan[id_chan] = discord_client.get_channel(id_chan)
            await map_chan[id_chan].send(msg)

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
                                                cfg_client, queue_to_client))

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
        system via the queue_from_client
        queue.

        """
        if not message.author.bot:
            msg = dict(type       = 'message',
                       id_prev    = None,
                       id_msg     = message.id,
                       id_author  = message.author.id,
                       id_channel = message.channel.id,
                       content    = message.content)
            try:
                queue_from_client.put(msg, block = False)
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
        system via the queue_from_client
        queue.

        """
        if not msg_after.author.bot:
            try:
                msg = dict(type       = 'message',
                           id_prev    = msg_before.id,
                           id_msg     = msg_after.id,
                           id_author  = msg_after.author.id,
                           id_channel = msg_after.channel.id,
                           content    = msg_after.content)
                queue_from_client.put(msg, block = False)
            except queue.Full:
                pass  # TODO: LOG SOME SORT OF ERROR?

    discord_client.run(cfg_client['str_token'], log_handler = loghandler)
