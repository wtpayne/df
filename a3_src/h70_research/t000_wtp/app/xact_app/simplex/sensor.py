# -*- coding: utf-8 -*-
"""
Simplex sensor component.

"""


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the sensor.

    """
    state['value'] = 0
    outputs['data']['ena']  = False
    outputs['data']['list'] = list()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the sensor.

    """
    outputs['data']['ena'] = False
    outputs['data']['list'].clear()

    if not inputs['control']['ena']:
        return

    msg_out = {
        'value': state['value']
    }
    state['value'] = state['value'] + 1

    outputs['data']['ena'] = True
    outputs['data']['list'].append(msg_out)