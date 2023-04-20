# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI client module."

description:
    "This module contains functionality for
    interacting with the OpenAI web API."

id:
    "555345dc-41c5-4810-a4fc-7ccbcde432af"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2022-2023 William Payne"

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


import multiprocessing
import queue
import time

import openai

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(cfg_client):
    """
    Yield results for requests sent to the OpenAI web API.

    For each list of request items that are
    sent to this coroutine, it will yield a
    tuple containing a list of result items
    followed by a list of errors encountered.

    """

    # Configure queues and start the
    # client in a separate process.
    #
    cfg_client['queue_request'] = multiprocessing.Queue()  # coro   --> daemon
    cfg_client['queue_result']  = multiprocessing.Queue()  # daemon --> coro
    cfg_client['queue_error']   = multiprocessing.Queue()  # daemon --> coro

    daemon = multiprocessing.Process(target = _daemon,
                                     args   = (cfg_client,),
                                     name   = 'openai-client',
                                     daemon = True)
    daemon.start()

    # Loop forever, sending data to
    # and from the openai client via
    # the two multiprocessing queue
    # objects.
    #
    list_item_result = list()
    list_item_error  = list()

    while True:

        # At each step, yield results
        # and errors to the controlling
        # context, and get any new
        # requests to send to the client
        # process.
        #
        list_item_request = yield (list_item_result, list_item_error)
        list_item_result.clear()
        list_item_error.clear()

        # Enqueue any newly submitted
        # requests.
        #
        for item_request in list_item_request:
            try:
                cfg_client['queue_request'].put(item_request, block = False)
            except queue.Full as err:
                list_item_error.append(err)

        # Dequeue any newly returned
        # results and errors.
        #
        while True:
            try:
                list_item_result.append(cfg_client['queue_result'].get(
                                                                block = False))
            except queue.Empty:
                break

        while True:
            try:
                list_item_error.append(cfg_client['queue_error'].get(
                                                                block = False))
            except queue.Empty:
                break


# -----------------------------------------------------------------------------
def _daemon(cfg):
    """
    Service the request queue, forwarding requests to the OpenAI API.

    Each request in the queue is processed,
    pausing for secs_interval if no request
    is available at that time.

    Results and errors are enqueued onto
    their respective queues for further
    processing by the controlling process.

    This is intended to be a minimal daemon
    that sits in a separate process and
    handles communication with the OpenAI
    API.

    """
    openai.api_key = cfg['api_key']

    while True:

        try:
            request = cfg['queue_request'].get(block = False)
        except queue.Empty:
            time.sleep(cfg['secs_interval'])
            continue

        result = _process_request(request, default = cfg['default'])

        if result['error'] is not None:
            cfg['queue_error'].put(result['error'])

        try:
            cfg['queue_result'].put(result, block = False)
        except queue.Full as error:
            cfg['queue_error'].put(error)


# -----------------------------------------------------------------------------
def _process_request(request, default):
    """
    Process a single request, returning a (result, error) pair.

    We start by building a kwargs dict,
    falling back on default parameter
    values if any are not specified by
    the request input. We use a separate
    kwargs dict rather than just passing
    in the request dict directly so that
    the request can be augmented with
    additional fields for book-keeping
    purposes.

    We update the request dict with the
    kwargs dictionary to ensure that the
    request dict accurately reflects the
    values that were actually sent to the
    OpenAI API.

    This request dict is then used as book
    keeping information, returned along
    with the response so we can keep track
    of which request relates to which
    response.

    """
    kwargs = dict(
            prompt      = request['prompt'],
            engine      = request.get('engine',      default['engine']      ),
            max_tokens  = request.get('max_tokens',  default['max_tokens']  ),
            n           = request.get('n',           default['n']           ),
            stop        = request.get('stop',        default['stop']        ),
            temperature = request.get('temperature', default['temperature'] ))

    request.update(kwargs)

    result = dict(request  = request,
                  response = None,
                  error    = None)

    try:

        result['response'] = openai.Completion.create(**kwargs)

    except openai.OpenAIError as ex:
        result['error'] = ex.user_message

    return result
