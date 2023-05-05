# -*- coding: utf-8 -*-
"""
Xact immediate mode graphical user interface application service component.

"""


import collections
import importlib

import xact.lib.service.util
import xact.lib.ui.imgui.widget.main_menu_bar


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Message producer coroutine.

    """

    signal        = None
    set_id_inout  = xact.lib.service.util.get_inout_ids(inputs, outputs)
    xact.lib.service.util.reset_outputs(
                                set_id_port = set_id_inout,
                                outputs     = outputs)
    inputs = yield (outputs, signal)

    # Build a list of python modules,
    # one for each configured service.
    #
    list_module = list()
    for spec_module in cfg['service']:
        list_module.append(importlib.import_module(spec_module))

    # Build a map from data set specification
    # to the corresponding (instantiated and
    # primed) coroutine handler.
    #
    map_coro = collections.defaultdict(set)
    for module in list_module:
        coro = module.coro(id_node = runtime['id']['id_node'])
        coro.send(None)
        map_coro[module.SPEC].add(coro)

    # Make an offer for each distinct spec.
    #
    for spec in map_coro.keys():
        xact.lib.service.util.offer(spec    = spec,
                                    id_node = runtime['id']['id_node'],
                                    outputs = outputs);

    while True:

        inputs = yield (outputs, signal)
        xact.lib.service.util.reset_outputs(set_id_port = set_id_inout,
                                            outputs     = outputs)

        # if inputs['camera_00']['ena']:
        #     for frame in inputs['camera_00']['list']:
        #         disp(frame)


        # Respond to requests.
        #
        list_msg_out = list()
        for request in xact.lib.service.util.iter_msg_filter(
                                                set_id_port = set_id_inout,
                                                inputs      = inputs,
                                                _type       = 'request'):

            for (spec, set_coro) in map_coro.items():

                if xact.lib.service.util.is_match(spec_lhs = request['_spec'],
                                                  spec_rhs = spec):

                    for coro in set_coro:
                        list_msg_out.extend(coro.send([request]))

        for msg_out in list_msg_out:
            xact.lib.service.util.add_message(outputs, msg_out)
