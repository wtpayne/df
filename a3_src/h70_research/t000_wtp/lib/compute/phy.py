# -*- coding: utf-8 -*-
"""
Physical node in a computational geometry layer.

"""


import dill


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the physical node.

    """
    state['logic'] = dict()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the physical node.

    """
    if inputs['logic']['ena']:
        for (key, value) in inputs['logic']['map'].items():
            thing = dill.loads(value)

        state['logic'].update()

    for (key, val) in state['logic'].items():
