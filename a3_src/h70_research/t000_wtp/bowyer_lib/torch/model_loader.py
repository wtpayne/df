# -*- coding: utf-8 -*-
"""
Neural network model loader node.

"""


import os
import importlib

import torch


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Model loader coroutine.

    """
    signal = None

    state['update_required']      = False
    state['filepath_model_state'] = cfg['filepath_model_state']

    if not os.path.isfile(state['filepath_model_state']):
        return

    state['update_required'] = True
    module = importlib.import_module(cfg['model_definition'])

    if 'Network' in module.__dict__:
        state['Network'] = module.Network

    if 'load' in module.__dict__:
        state['load'] = module.load

    while True:

        inputs = yield (outputs, signal)

        outputs['model']['ena']   = False
        outputs['model']['model'] = None

        if state['update_required']:

            model       = state['Network']()
            device      = torch.device(
                                'cuda' if torch.cuda.is_available() else 'cpu')
            model_state = torch.load(
                                state['filepath_model_state'],
                                map_location = device)
            state['load'](model, model_state)

            outputs['model']['model'] = model
            outputs['model']['ena']  = True
            state['update_required'] = False
