# -*- coding: utf-8 -*-
"""
Simplex processor component.

"""


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the processor.

    """
    outputs['data']['ena']  = False
    outputs['data']['list'] = list()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the processor.

    """
    outputs['data']['ena'] = False
    outputs['data']['list'].clear()

    if not inputs['control']['ena']:
        return

    if not inputs['data']['ena']:
        return

    for msg_in in inputs['data']['list']:
        outputs['data']['ena'] = True
        msg_out = {
            'value': msg_in['value'] + 42
        }
        outputs['data']['list'].append(msg_out)
