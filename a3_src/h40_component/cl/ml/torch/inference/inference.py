# -*- coding: utf-8 -*-
"""
Pytorch inference node.

"""


import torch


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Model inference coroutine.

    """
    signal = None

    state['device'] = None
    state['model']  = None

    while True:

        inputs = yield (outputs, signal)

        outputs['result']['ena']  = False

        if inputs['model']['ena']:
            state['device'] = torch.device(
                                "cuda" if torch.cuda.is_available() else "cpu")
            state['model'] = inputs['model']['model']
            state['model'].to(state['device'])
            state['model'].eval()

        if state['model'] and inputs['sample']['ena']:
            outputs['result']['ena']  = True
            outputs['result']['ts']   = inputs['sample']['ts']
            outputs['result']['data'] = state['model'](
                                                inputs['sample']['buff'].to(
                                                            state['device']))