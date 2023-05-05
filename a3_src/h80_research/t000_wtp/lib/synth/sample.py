# -*- coding: utf-8 -*-
"""
Xact component for generating sample parameter values.

"""


import random


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the physical entity simulation component.

    """
    random.seed(cfg.get('seed', 0))
    state['rng_state'] = random.getstate()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the physical entity simulation component.

    """

    outputs['sample']['ena'] = False

    if not inputs['control']['ena']:
        return

    lo                 = 0
    hi                 = 1
    random.setstate(state['rng_state'])
    sample_value       = random.uniform(lo,hi)
    state['rng_state'] = random.getstate()

    outputs['sample']['ena']   = True
    outputs['sample']['idx']   = inputs['control']['idx']
    outputs['sample']['value'] = sample_value
