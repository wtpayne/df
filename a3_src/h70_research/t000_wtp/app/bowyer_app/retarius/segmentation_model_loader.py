# -*- coding: utf-8 -*-
"""
Neural network model loader node.

"""


import os
import sys
import importlib

import torch



# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Model loader coroutine.

    """
    signal = None

    state['update_required'] = False
    state['filepath']        = cfg['filepath']

    if not os.path.isfile(state['filepath']):
        # LOGGING?
        return

    state['update_required'] = True

    # module = importlib.import_module(cfg['model_definition'])

    # if 'Network' in module.__dict__:
    #     state['Network'] = module.Network

    # if 'load' in module.__dict__:
    #     state['load'] = module.load

    while True:

        inputs = yield (outputs, signal)

        outputs['model']['ena']   = False
        outputs['model']['model'] = None

        if state['update_required']:
            state['update_required'] = False

            os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = 'python'
            sys.path.append('/media/wtp/Data/dev/STEGO/src/')
            from train_segmentation import LitUnsupervisedSegmenter as ls
            outputs['model']['model'] = ls.load_from_checkpoint(
                                                    state['filepath'])
            outputs['model']['ena']   = True
