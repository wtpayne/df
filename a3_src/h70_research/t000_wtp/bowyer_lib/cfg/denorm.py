# -*- coding: utf-8 -*-
"""
Bowyer component for denormalizing bowyer configuration data.

"""


import copy

import bowyer.cfg


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Yield denormalized config data from the supplied raw config data.

    On each model step a dict of raw configuration
    data is recieved as input.

    For each of the received raw configuration data
    structures, a fully rehydrated / denormalized
    copy is created with all convenience duplicate
    and derived fields populated and in place.

    All copies created in the current model step
    are then placed in a dictionary and output.

    """
    signal = None

    # Initialize outputs when the system
    # first starts, preallocating memory
    # if appropriate.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena'] = True
        outputs[id_out]['ts']  = dict()
        outputs[id_out]['map'] = dict()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs at the beginning
        # of each simulation step.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['map'].clear()

        # If one or more raw configuration data
        # structures are supplied as input, then
        # create a denormalized copy of each of
        # then and store it in the map_cfg
        # dictionary.
        #
        map_ts  = dict()
        map_cfg = dict()
        for id_in in inputs.keys():
            if inputs[id_in]['ena']:
                map_ts = inputs[id_in]['ts']
                for (id_path, cfg_raw) in inputs[id_in]['map'].items():
                    map_cfg[id_path] = bowyer.cfg.denormalize(
                                                    copy.deepcopy(cfg_raw))

        # If any data has been denormalized,
        # then output it.
        #
        if map_cfg:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['map'].update(map_cfg)