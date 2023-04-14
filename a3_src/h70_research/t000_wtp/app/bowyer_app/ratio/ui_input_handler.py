# -*- coding: utf-8 -*-
"""
Bowyer component to handle input from a web based UI.

This is responsible for extracting commands and
forwarding them to the bits of the system that
can action them.

Authentication, sessions and cookies may also be
handled here in future.

"""


import collections
import copy
import textwrap

import bowyer.lib.ui.web.markup.aframe
import bowyer.lib.ui.web.markup.html
import bowyer.lib.ui.web.util
import bowyer.lib.web.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Handle input from a web based UI.

    """
    signal = None

    # Initialize outputs.
    #
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

        # Handle input from UI.
        #
        list_commands = list()
        for id_in in inputs.keys():
            if not inputs[id_in]['ena']:
                continue

            map_ts = inputs[id_in]['ts']

            list_commands.extend(
                    cmd for cmd in _iter_commands(
                                    list_map_request = inputs[id_in]['list']))

        # Fill outputs with commands from input.
        #
        if list_commands:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'].extend(list_commands)


# -----------------------------------------------------------------------------
def _iter_commands(list_map_request):
    """
    Yield all commands in the specified list of requests.

    An example of a request:-

        {
            'accept':          '*/*',
            'accept_encoding':  'gzip, deflate, br',
            'accept_language':  'en-GB,en;q=0.5',
            'client_ip':        '127.0.0.1',
            'id_node':          ['ui_2d'],
            'id_resource':      'click',
            'id_session':       'df27de51-0774-4aff-844f-3ed71f095bb2',
            'id_system':        ['ratio'],
            'id_user':          'd2078090-9ea7-40de-94d3-fa4f50b86acc',
            'url':              'https://0.0.0.0:8080/click?id_system=ratio&id_node=ui_2d',
            'user_agent':       'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) 'Gecko/20100101 Firefox/106.0'}]
        }

    """
    set_key_scalar = frozenset(('id_resource',))
    set_key_vector = frozenset(('id_event', 'id_path', 'id_system', 'id_node'))
    set_key_expected = set_key_scalar | set_key_vector
    for map_request in list_map_request:

        set_key_actual    = set(map_request.keys())
        has_expected_keys = set_key_expected <= set_key_actual
        if not has_expected_keys:
            continue

        cmd = dict()
        for key in set_key_scalar:
            cmd[key] = map_request[key]
        for key in set_key_vector:
            cmd[key] = map_request[key][0]
        yield cmd