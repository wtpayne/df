# -*- coding: utf-8 -*-
"""
Distribute a list of input data item evenly onto all outputs.

"""


import itertools


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the round robin.

    """
    pass


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the round robin.

    """
    for key in outputs.keys():
        outputs[key]['ena'] = False
        outputs[key]['list'].clear()

    assert len(inputs) == 1
    input_data = next(iter(inputs.values()))

    if not input_data['ena']:
        return

    for (key, item) in zip(itertools.cycle(outputs.keys()), input_data['list']):
        outputs[key]['list'].append(item)

    for key in outputs.keys():
        if outputs[key]['list']:
            outputs[key]['ena'] = True
