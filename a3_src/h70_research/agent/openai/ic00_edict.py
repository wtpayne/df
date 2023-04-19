# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI agent stableflow-edict component."

description:
    "Generic OpenAI agent."

id:
    "8d2b1939-cea9-4af0-9528-7cc5e44d0a5c"

type:
    dt004_python_stableflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2023 William Payne"

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
import openai


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    OpenAI agent coroutine

    """

    # loading secrets
    # from a .env file in the configured
    # location.
    #
    dotenv.load_dotenv(dotenv_path = cfg['filepath_env'],
                       verbose     = True,
                       override    = False)
    cfg_client                   = dict()
    cfg_client['api_key']        = os.environ[cfg['envvar_key']]
    cfg_client['secs_interval']  = cfg.get('secs_interval', 5)
    cfg_client['default']        = cfg['default']

    coro_openai = _openai_coroutine(cfg_client)
    coro_openai.send(None)

    # Initialize outputs.
    #
    signal = None
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Get stuff
        #
        map_ts            = dict()
        list_item_error   = list()
        list_item_request = list()
        for (id_in, packet_in) in inputs.items():
            if packet_in['ena']:
                map_ts = packet_in['ts']
                list_item_request.extend(packet_in['list'])

        (list_item_response,
         list_item_error) = coro_openai.send(list_item_request)

        if list_item_response and ('response' in outputs):
            outputs['response']['ena'] = True
            outputs['response']['ts'].update(map_ts)
            outputs['response']['list'][:] = list_item_response

        if list_item_error and ('error' in outputs):
            outputs['error']['ena'] = True
            outputs['error']['ts'].update(map_ts)
            outputs['error']['list'][:] = list_item_error


# -----------------------------------------------------------------------------
def _coro_openai(cfg_client):
    """
    OpenAI integration coroutine.

    """

    # Configure queues and start the
    # client in a separate process.
    #
    cfg_client['queue_request']  = multiprocessing.Queue()  # To client.
    cfg_client['queue_response'] = multiprocessing.Queue()  # From client.
    cfg_client['queue_error']    = multiprocessing.Queue()  # From client.

    daemon = multiprocessing.Process(target = _openai_client_daemon,
                                     args   = (cfg_client,),
                                     name   = 'openai-client',
                                     daemon = True)
    daemon.start()

    # Loop forever, sending data to
    # and from the openai client via
    # the two multiprocessing queue
    # objects.
    #
    list_item_response = list()
    list_item_error    = list()

    while True:

        # At each step, yield responses
        # and errors to the controlling
        # coroutine, and get any new
        # requests to send to the client
        # process.
        #
        list_item_request = yield (list_item_response, list_item_error)
        list_item_response.clear()
        list_item_error.clear()

        # Enqueue any newly received
        # requests.
        #
        for item_request in list_item_request:
            try:
                cfg_client['queue_request'].put(item_request, block = False)
            except queue.Full as err:
                list_item_error.append(err)

        # Dequeue any newly received
        # responses.
        #
        while True:
            try:
                item_response = cfg_client['queue_response'].get(block = False)
                list_item_response.append(item_response)
            except queue.Empty:
                break

        # Dequeue any newly received
        # errors.
        #
        while True:
            try:
                item_error = cfg_client['queue_error'].get(block = False)
                list_item_error.append(item_error)
            except queue.Empty:
                break


# -----------------------------------------------------------------------------
def _openai_client_daemon(cfg):
    """
    Service the request queue, forwarding requests to the OpenAI API.

    Responses and errors are enqueued
    onto their respective queues for
    further processing by the controlling
    process.

    This is intended to be a minimal daemon
    that sits in a separate process and
    handles communication with the OpenAI
    API.

    """

    import time
    import openai

    openai.api_key = cfg['api_key']
    default        = cfg['default']

    # Process each prompt in the queue,
    # pausing for secs_interval if no
    # prompt is available.
    #
    while True:

        try:
            req = cfg['queue_request'].get(block = False)
        except queue.Empty:
            time.sleep(cfg['secs_interval'])
            continue

        # Set default request parameters.
        #
        kwargs = dict()
        kwargs['prompt']      = req['prompt']
        kwargs['engine']      = req.get('engine',      default['engine']      )
        kwargs['max_tokens']  = req.get('max_tokens',  default['max_tokens']  )
        kwargs['n']           = req.get('n',           default['n']           )
        kwargs['stop']        = req.get('stop',        default['stop']        )
        kwargs['temperature'] = req.get('temperature', default['temperature'] )

        response = openai.Completion.create(**kwargs)

        # Augment the response so we
        # can keep track of which
        # request caused which
        # response.
        #
        req.update(kwargs)
        response['request'] = req

        try:
            cfg['queue_response'].put(response, block = False)
        except queue.Full as err:
            cfg['queue_error'].put(err)
