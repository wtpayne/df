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
def coro(cfg_bot):
    """
    Yield results for workflow coroutines sent to the OpenAI web API.

    Start the client in a separate process.

    """

    str_name_process   = 'discord-bot'
    fcn_bot            = _discord_bot
    queue_msg_to_bot   = multiprocessing.Queue()  # msg system  --> discord
    queue_cmd_to_bot   = multiprocessing.Queue()  # cmd system  --> discord
    queue_msg_from_bot = multiprocessing.Queue()  # msg discord --> system
    queue_cmd_from_bot = multiprocessing.Queue()  # cmd discord --> system
    queue_log_from_bot = multiprocessing.Queue()  # log discord --> system
    tup_args           = (cfg_bot,
                          queue_msg_to_bot,
                          queue_cmd_to_bot,
                          queue_msg_from_bot,
                          queue_cmd_from_bot,
                          queue_log_from_bot)
    proc_bot           = multiprocessing.Process(
                                        target = fcn_bot,
                                        args   = tup_args,
                                        name   = str_name_process,
                                        daemon = True)  # So we get terminated
    proc_bot.start()

    list_msg_to_bot   = list()
    list_cmd_to_bot   = list()
    list_msg_from_bot = list()
    list_cmd_from_bot = list()
    list_log_from_bot = list()

    while True:

        list_msg_to_bot.clear()
        list_cmd_to_bot.clear()

        (list_msg_to_bot,
         list_cmd_to_bot) = yield (list_msg_from_bot,
                                   list_cmd_from_bot,
                                   list_log_from_bot)

        list_msg_from_bot.clear()
        list_cmd_from_bot.clear()
        list_log_from_bot.clear()

        # If the rest of the system sends us
        # any system messages or new commands
        # to configure, then forward them
        # on to the discord client process
        # to either be sent to the relevant
        # channel (in the case of messages),
        # or to use to configure new commands
        # (in the case of command configuration).
        #
        for tup_msg in list_msg_to_bot:
            try:
                queue_msg_to_bot.put(tup_msg, block = False)
            except queue.Full as err:
                list_log_from_bot.append(
                        'Message dropped: queue_msg_to_bot is full.')

        for cfg_cmd in list_cmd_to_bot:
            try:
                queue_cmd_to_bot.put(cfg_cmd, block = False)
            except queue.Full as err:
                list_log_from_bot.append(
                        'Command config dropped: queue_cmd_to_bot is full.')

        # Retrieve any user messages, command
        # invocations or log messages from the
        # discord client and forward them to
        # the rest of the system for further
        # processing.
        #
        while True:
            try:
                list_msg_from_bot.append(queue_msg_from_bot.get(block = False))
            except queue.Empty:
                break

        while True:
            try:
                list_cmd_from_bot.append(queue_cmd_from_bot.get(block = False))
            except queue.Empty:
                break

        while True:
            try:
                list_log_from_bot.append(queue_log_from_bot.get(block = False))
            except queue.Empty:
                break


# -----------------------------------------------------------------------------
def _discord_bot(cfg_bot,
                 queue_msg_to_bot,
                 queue_cmd_to_bot,
                 queue_msg_from_bot,
                 queue_cmd_from_bot,
                 queue_log_from_bot):
    """
    Run the discord client.

    This function is expected to be run in a separate daemon process.

    """

    import functools
    import io
    import logging
    import os

    import discord
    import discord.ext
    import discord.ext.commands

    intents                 = discord.Intents.default()
    intents.guilds          = True
    intents.dm_messages     = True
    intents.dm_reactions    = True
    intents.message_content = True
    intents.messages        = True
    intents.reactions       = True
    bot                     = discord.ext.commands.Bot(
                                                    command_prefix = '$',
                                                    intents        = intents)

    buffer_log = io.StringIO()
    loghandler = logging.StreamHandler(buffer_log)

    # -------------------------------------------------------------------------
    @bot.event
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

        task_msg = bot.loop.create_task(coro = _service_all_queues(
                                                        cfg_bot,
                                                        queue_msg_to_bot,
                                                        queue_cmd_to_bot,
                                                        queue_log_from_bot))


    # -------------------------------------------------------------------------
    async def _service_all_queues(cfg_bot,
                                  queue_msg_to_bot,
                                  queue_cmd_to_bot,
                                  queue_log_from_bot):
        """
        Message queue servicing coroutine.

        This coroutine is intended to
        run continuously, servicing
        the multiprocessing.queue
        instance that feeds messages
        from the rest of the system to
        the discord bot.

        This coroutine is started from
        the on_ready callback - i.e as
        soon as the discord bot is
        ready.

        """

        # This is a redundant sanity check, as
        # the service task should be created in
        # the on_ready callback.
        #
        await bot.wait_until_ready()

        map_chan = dict()
        map_cmd  = dict()

        while True:

            # Try to pull the next message
            # from the queue, and if we get
            # one, then process it.
            #
            try:
                tup_msg = queue_msg_to_bot.get(block = False)
            except queue.Empty:
                await asyncio.sleep(cfg_bot['secs_interval'])

            else:

                # If we have a new message to
                # handle, then simply send it
                # to the specified channel.
                #
                (id_chan, msg) = tup_msg
                if id_chan not in map_chan.keys() or map_chan[id_chan] is None:
                    map_chan[id_chan] = bot.get_channel(id_chan)

                if map_chan[id_chan] is None:
                    print('Failed to access channel: ' + str(id_chan))
                    continue

                # Allow clients to send messages in
                # simplified form - just as a string.
                #
                if isinstance(msg, str):
                    await map_chan[id_chan].send(msg)
                    continue

                # When we are being given a mapping
                # type for a message, we need to
                # add special handling for FileData
                # named tuples. This is so that
                # we can send files without needing
                # access ot the local filesystem.
                # (The FileData encodes the file
                # in an in-memory buffer).
                #
                if 'file' in msg and isinstance(msg['file'], FileData):

                    file_data   = msg['file']
                    msg['file'] = discord.File(
                                    fp          = io.BytesIO(file_data.buffer),
                                    filename    = file_data.filename,
                                    spoiler     = file_data.spoiler,
                                    description = file_data.description)

                # Finally we can post the specified
                # message to the specified channel.
                #
                await map_chan[id_chan].send(**msg)

            # Try to pull the next command
            # from the queue, and if we get
            # one, then process it.
            #
            try:
                cfg_cmd = queue_cmd_to_bot.get(block = False)
            except queue.Empty:
                await asyncio.sleep(cfg_bot['secs_interval'])

            else:

                # -------------------------------------------------------------
                async def on_command_generic(name_cmd, ctx, *args):
                    """
                    Generic command callback.

                    """

                    print('ON COMMAND')

                    try:
                        queue_cmd_from_bot.put(dict(name = name_cmd,
                                                    ctx  = ctx,
                                                    args = args),
                                               block = False)
                    except queue.Full:
                        print('Cmd cfg dropped: queue_cmd_from_bot is full.')

                name_cmd = cfg_cmd['name']
                on_command = functools.partial(on_command_generic, name_cmd)
                on_command.__name__     = on_command_generic.__name__
                on_command.__qualname__ = on_command_generic.__qualname__

                command = discord.ext.commands.Command(
                                                on_command,
                                                name = name_cmd,
                                                help = cfg_cmd['description'])

                map_cmd[cfg_cmd['name']] = command
                bot.add_command(command)

            # If there is any log data in the
            # buffer, then enqueue it to be
            # sent back to the rest of the
            # system.
            #
            loghandler.flush()
            str_log = buffer_log.getvalue()
            if str_log:
                try:
                    queue_log_from_bot.put(str_log, block = False)
                except queue.Full:
                    print('Log msg dropped: queue_log_from_bot is full.')

    # -------------------------------------------------------------------------
    @bot.event
    async def on_command_error(ctx, error):
        """
        Handle errors in commands.

        """

        # TODO: Add error to log.
        raise error

    # -------------------------------------------------------------------------
    @bot.event
    async def on_message(message):
        """
        Handle messages that are sent to the client.

        This coroutine is invoked
        whenever a message is created
        and sent.

        This coroutine is intended to
        simply forward the content of
        the message to the rest of the
        system via the queue_msg_from_bot
        queue.

        """

        await bot.process_commands(message)

        if not message.author.bot:

            msg = dict(msg_type   = 'message',
                       id_prev    = None,
                       id_msg     = message.id,
                       id_author  = message.author.id,
                       id_channel = message.channel.id,
                       content    = message.content)
            try:
                queue_msg_from_bot.put(msg, block = False)
            except queue.Full:
                pass  # TODO: LOG SOME SORT OF ERROR?

    # -------------------------------------------------------------------------
    @bot.event
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
        system via the queue_msg_from_bot
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
                queue_msg_from_bot.put(msg, block = False)
            except queue.Full:
                pass  # TODO: LOG SOME SORT OF ERROR?

    # Run the client.
    #
    if cfg_bot['debug']:

        bot.run(token     = cfg_bot['str_token'],
                reconnect = False,
                log_level = logging.INFO)

    else:

        bot.run(token       = cfg_bot['str_token'],
                reconnect   = True,
                log_level   = logging.INFO,
                log_handler = loghandler)
