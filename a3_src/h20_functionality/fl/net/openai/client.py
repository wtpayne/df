# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI API support module."

description:
    "This Python module is designed to interact
    with the OpenAI API using a separate process
    for handling requests and responses. It uses
    the multiprocessing and queue libraries to
    manage inter-process communication, and the
    openai library to interact with the OpenAI
    API. The module defines three main functions:
    coro, _daemon, and _process_request.

    coro(cfg_client) is a coroutine function that
    acts as a bridge between the main process and
    the separate process running the OpenAI API
    client. It takes a configuration dictionary
    as input, initializes multiprocessing queues
    for requests, results, and errors, and starts
    the daemon process. It then enters a loop,
    yielding results and errors to the calling
    context while accepting new requests and
    sending them to the daemon process.

    _daemon(cfg) is the main function running in
    the separate process. It takes a configuration
    dictionary as input and services the request
    queue by forwarding requests to the OpenAI
    API. It processes each request, enqueues
    results and errors onto their respective
    queues, and sleeps for a specified interval
    if no request is available.

    _process_request(request, default) is a
    helper function that processes a single
    request, returning a dictionary with the
    original request, response, and error
    information. It first builds a dictionary
    of keyword arguments for the OpenAI API call,
    using default values for any unspecified
    parameters. It then calls the OpenAI API
    with the constructed keyword arguments,
    catches any errors, and returns the result
    dictionary containing the original request,
    the API response, and any error encountered.

    Here is an example of a result data structure:

    {'error':       None,
     'request':     {'engine':      '<OPENAI_MODEL_ID>',
                     'max_tokens':  100,
                     'n':           1,
                     'prompt':      '<PROMPT_TEXT>.',
                     'stop':        None,
                     'temperature': 0.5},
     'response':    {'choices':     [{'finish_reason':  'stop',
                                      'index':          0,
                                      'logprobs':       None,
                                      'text':           '<RESPONSE_TEXT>'}],
                     'created':    1682122855,
                     'id':         'cmpl-77vHj30k0S1k8pqz2lHUueiQDMSZj',
                     'model':      '<OPENAI_MODEL_ID>',
                     'object':     'text_completion',
                     'usage':      {'completion_tokens':   57,
                                    'prompt_tokens':       9,
                                    'total_tokens':        66}}}"


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
def coro(cfg):
    """
    Yield results for requests sent to the OpenAI web API.

    For each list of request items that are
    sent to this coroutine, it will yield a
    tuple containing a list of result items
    followed by a list of errors encountered.

    """
    assert 'api_key'           in cfg
    assert 'secs_interval'     in cfg
    assert 'is_bit'            in cfg
    assert 'default'           in cfg
    assert 'model'             in cfg['default']
    assert 'temperature'       in cfg['default']
    assert 'n'                 in cfg['default']
    assert 'stream'            in cfg['default']
    assert 'presence_penalty'  in cfg['default']
    assert 'frequency_penalty' in cfg['default']
    assert 'user'              in cfg['default']
    assert 'metadata'          in cfg['default']

    # Configure queues and start the
    # client in a separate process.
    #
    cfg['queue_request'] = multiprocessing.Queue()  # coro   --> daemon
    cfg['queue_result']  = multiprocessing.Queue()  # daemon --> coro
    cfg['queue_error']   = multiprocessing.Queue()  # daemon --> coro

    daemon = multiprocessing.Process(target = _daemon,
                                     args   = (cfg,),
                                     name   = 'openai-client',
                                     daemon = True)
    daemon.start()

    # Loop forever, sending data to
    # and from the openai client via
    # the multiprocessing queues.
    #
    list_item_result  = list()
    list_item_error   = list()

    # Loop forever
    #
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
                cfg['queue_request'].put(item_request, block = False)
            except queue.Full as err:
                list_item_error.append(err)

        # Dequeue any newly returned
        # results and errors.
        #
        while True:
            try:
                result = cfg['queue_result'].get(block = False)
                list_item_result.append(result)
            except queue.Empty:
                break

        while True:
            try:
                list_item_error.append(cfg['queue_error'].get(block = False))
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

        result = _process_request(request,
                                  default = cfg['default'],
                                  is_bit  = cfg['is_bit'])

        if result['error'] is not None:
            cfg['queue_error'].put(result['error'], block = False)

        try:
            cfg['queue_result'].put(result, block = False)
        except queue.Full as error:
            cfg['queue_error'].put(error, block = False)


# -----------------------------------------------------------------------------
def _process_request(request, default, is_bit):
    """
    Process a single request, returning a result dict.

    We start by building a 'request_full'
    dict, falling back on default parameter
    values if any are missing in the input
    request dict.

    The result contains

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
    (fcn_endpoint,
     request_new,
     metadata) = _build_callback_request_and_metadata(request_raw = request,
                                                      default     = default)

    result  = dict(request  = request_new,
                   response = None,
                   error    = None,
                   metadata = metadata)

    if is_bit:
        result['response'] = built_in_test_response()
    else:
        try:
            result['response'] = fcn_endpoint(**request_new)
        except openai.OpenAIError as err:
            result['error'] = err.user_message

    # TODO: Update budget/spend?

    return result


# -----------------------------------------------------------------------------
def _build_callback_request_and_metadata(request_raw, default):
    """
    Return a tuple with endpoint function, updated request and metadata.

    This information is extracted from the input
    request_raw structure and any default values
    from the supplied configuration.

    """

    # Determine which endpoint is being requested.
    #
    id_endpoint = request_raw.get('endpoint', None)
    if id_endpoint is None:
        id_endpoint = default.get('endpoint', None)
    if id_endpoint is None:
        raise RuntimeError('Could not determine endpoint.')

    # Determine which endpoint API callback to use.
    #
    map_fcn_endpoint = dict(
        completions           = openai.Completion.create,
        chat_completions      = openai.ChatCompletion.create,
        edits                 = openai.Edit.create,
        images_generations    = openai.Image.create,
        images_edits          = openai.Image.create_edit,
        images_variations     = openai.Image.create_variation,
        embeddings            = openai.Embedding.create,
        audio_transcriptions  = openai.Audio.transcribe,
        audio_translations    = openai.Audio.translate)
    fcn_endpoint = map_fcn_endpoint[id_endpoint]

    # Determine how to handle request parameters.
    #
    # Tuple is (required-internally, required-OpenAI, name-in-api, type)
    #
    Y = True
    N = False
    map_tup_tup_params = dict(  # RI, RO, name-api,           type
        completions           = (( N,  Y, 'model',             (str,)      ),
                                 ( Y,  N, 'prompt',            (str, list) ),
                                 ( N,  N, 'suffix',            (str,)      ),
                                 ( N,  N, 'max_tokens',        (int,)      ),
                                 ( N,  N, 'temperature',       (float,)    ),
                                 ( N,  N, 'top_p',             (float,)    ),
                                 ( N,  N, 'n',                 (int,)      ),
                                 ( N,  N, 'stream',            (bool,)     ),
                                 ( N,  N, 'logprobs',          (int,)      ),
                                 ( N,  N, 'echo',              (bool,)     ),
                                 ( N,  N, 'stop',              (str, list) ),
                                 ( N,  N, 'presence_penalty',  (float,)    ),
                                 ( N,  N, 'frequency_penalty', (float,)    ),
                                 ( N,  N, 'best_of',           (int,)      ),
                                 ( N,  N, 'logit_bias',        (dict,)     ),
                                 ( N,  N, 'user',              (str,)      )),
        chat_completions      = (( N,  Y, 'model',             (str,)      ),
                                 ( Y,  Y, 'messages',          (list,)     ),
                                 ( N,  N, 'temperature',       (float,)    ),
                                 ( N,  N, 'top_p',             (float,)    ),
                                 ( N,  N, 'n',                 (int,)      ),
                                 ( N,  N, 'stream',            (bool,)     ),
                                 ( N,  N, 'stop',              (str, list) ),
                                 ( N,  N, 'max_tokens',        (int,)      ),
                                 ( N,  N, 'presence_penalty',  (float,)    ),
                                 ( N,  N, 'frequency_penalty', (float,)    ),
                                 ( N,  N, 'logit_bias',        (dict,)     ),
                                 ( N,  N, 'user',              (str,)      )),
        edits                 = (( N,  Y, 'model',             (str,)      ),
                                 ( Y,  N, 'input',             (str,)      ),
                                 ( Y,  Y, 'instruction',       (str,)      ),
                                 ( N,  N, 'n',                 (int,)      ),
                                 ( N,  N, 'temperature',       (float,)    ),
                                 ( N,  N, 'top_p',             (float,)    )),
        images_generations    = (( Y,  Y, 'prompt',            (str,)      ),
                                 ( N,  N, 'n',                 (int,)      ),
                                 ( N,  N, 'size',              (str,)      ),
                                 ( N,  N, 'response_format',   (str,)      ),
                                 ( N,  N, 'user',              (str,)      )),
        images_edits          = (( Y,  Y, 'image',             (str,)      ),
                                 ( N,  N, 'mask',              (str,)      ),
                                 ( Y,  Y, 'prompt',            (str,)      ),
                                 ( N,  N, 'n',                 (int,)      ),
                                 ( N,  N, 'size',              (str,)      ),
                                 ( N,  N, 'response_format',   (str,)      ),
                                 ( N,  N, 'user',              (str,)      )),
        images_variations     = (( Y,  Y, 'image',             (str,)      ),
                                 ( N,  N, 'n',                 (int,)      ),
                                 ( N,  N, 'size',              (str,)      ),
                                 ( N,  N, 'response_format',   (str,)      ),
                                 ( N,  N, 'user',              (str,)      )),
        embeddings            = (( N,  Y, 'model',             (str,)      ),
                                 ( Y,  Y, 'input',             (str,list)  ),
                                 ( N,  N, 'user',              (str,)      )),
        audio_transcriptions  = (( Y,  Y, 'file',              (str,)      ),
                                 ( N,  Y, 'model',             (str,)      ),
                                 ( N,  N, 'prompt',            (str,)      ),
                                 ( N,  N, 'response_format',   (str,)      ),
                                 ( N,  N, 'temperature',       (float,)    ),
                                 ( N,  N, 'language',          (str,)      )),
        audio_translations    = (( Y,  Y, 'file',              (str,)      ),
                                 ( N,  Y, 'model',             (str,)      ),
                                 ( N,  N, 'prompt',            (str,)      ),
                                 ( N,  N, 'response_format',   (str,)      ),
                                 ( N,  N, 'temperature',       (float,)    )))

    # Build the request_new structure.
    #
    request_new    = dict()
    tup_tup_params = map_tup_tup_params[id_endpoint]
    for (is_required_by_internal_api,  # Cannot be given a default value.
         is_required_by_openai_api,    # Must be given a value of some sort.
         id_param,
         tup_type) in tup_tup_params:

        # Try to get value from request_raw.
        #
        param = request_raw.get(id_param, None)
        if param is not None:
            _check_type(id_param, param, tup_type)
            request_new[id_param] = param
            continue

        if is_required_by_internal_api:
            raise RuntimeError('{id} not in request_raw'.format(id = id_param))

        # Try to get value from default.
        #
        param = default.get(id_param, None)
        if param is not None:
            _check_type(id_param, param, tup_type)
            request_new[id_param] = param
            continue

        if is_required_by_openai_api:
            raise RuntimeError('{id} not in request_raw or default'.format(
                                                                id = id_param))

    metadata = request_raw.get('metadata', None)
    if metadata is None:
        metadata = default.get('metadata', None)
    if metadata is None:
        metadata = dict()  # TODO: Work out if this should be dict() or None?

    return (fcn_endpoint, request_new, metadata)


# -----------------------------------------------------------------------------
def _check_type(id_param, param, tup_type):
    """
    Raise an exception if param is not in tup_type.

    """
    if isinstance(param, tup_type):
        return
    raise RuntimeError(
        'Type error for request["{id}"]: ({typename} != {reqired})'.format(
                                                    id       = id_param,
                                                    typename = type(param),
                                                    required = repr(tup_type)))

# -----------------------------------------------------------------------------
def built_in_test_response():
    """
    Return the built-in-test response.

    """
    return {
        "id":       "chatcmpl-abc123",
        "object":   "chat.completion",
        "created":  1677858242,
        "model":    "gpt-3.5-turbo-0301",
        "usage":    { "prompt_tokens":     13,
                      "completion_tokens": 7,
                      "total_tokens":      20},
        "choices":  [ { "message":         { "role":    "assistant",
                                             "content": "\n\nTest"},
                        "finish_reason":   "stop",
                        "index":           0}]}