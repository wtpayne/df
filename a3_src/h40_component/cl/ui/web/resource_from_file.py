# -*- coding: utf-8 -*-
"""
Bowyer component for live web resource updating.

"""


import os.path
import time

import bowyer.lib.ui.web.markup.html as html
import bowyer.lib.web.util
import bowyer.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the bowyer component.

    """
    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    # Initialize state.
    #
    state['list'] = list()
    for cfg_item in cfg['list']:
        state_item = dict()
        state_item.update(cfg_item)
        state_item['last_modified'] = 0
        state['list'].append(state_item)


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the bowyer component.

    """
    bowyer.util.clear_outputs(
                    outputs             = outputs,
                    iter_name_output    = ('resources',),
                    iter_field_to_clear = ('list', ))

    if not inputs['control']['ena']:
        return

    map_ts  = inputs['control']['ts']
    map_res = bowyer.lib.web.util.ResMap()
    for state_item in state['list']:

        modified = os.path.getmtime(state_item['filepath'])
        if state_item['last_modified'] >= modified:
            return
        state_item['last_modified'] = modified

        if state_item['is_binary']:
            mode_file = 'rb'
        else:
            mode_file = 'rt'

        with open(state_item['filepath'], mode_file) as file:
            map_res.add(media_type = state_item['media_type'],
                        **{state_item['id_resource']: file.read()})

    if map_res:
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = True
            outputs[id_out]['ts'].update(map_ts)
            outputs[id_out]['list'].append(dict(map_res))
