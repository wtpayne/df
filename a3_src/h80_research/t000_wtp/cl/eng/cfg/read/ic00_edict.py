# -*- coding: utf-8 -*-
"""
Bowyer component for reading stableflow configuration files.

"""


import stableflow.cfg


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Yield configuration data from the supplied filenames.

    On each model step a list of filesystem paths
    are received as input.

    For each of the recieved paths the corresponding
    file or directory is read and the resulting raw
    configuration data is loaded into memory.

    At the end of each model step, a dictionary is
    output which maps from each of the supplied
    filesystem paths to the corresponding raw
    configuration data.

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
        # of each model step.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['map'].clear()

        # If one or more filesystem paths
        # are supplied as input, then
        # read and deserialize the raw
        # configuration data stored within
        # each of them into the map_cfg
        # dictionary.
        #
        map_ts  = dict()
        map_cfg = dict()
        for id_in in inputs.keys():
            if not inputs[id_in]['ena']:
                continue
            map_ts = inputs[id_in]['ts']
            for path_cfg in inputs[id_in]['list']:
                try:
                    cfg_raw          = stableflow.cfg.prepare(path_cfg)
                    id_path          = cfg_raw['runtime']['id']['id_path']
                    map_cfg[id_path] = cfg_raw
                except stableflow.cfg.exception.CfgError:
                    continue

        # If one or more raw configuration
        # data structures has been loaded
        # from the filesystem then output
        # them from the coroutine.
        #
        if map_cfg:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['map'].update(map_cfg)
