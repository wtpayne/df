# -*- coding: utf-8 -*-
"""
Exception thrower test component.

"""


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the exception thrower test component.

    """

    state['idx_max'] = cfg.get('idx_max', 0);


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the exception thrower test component.

    """

    print('[' + str(inputs['control']['idx']) + '] - APPLICATION NODE STEP.')
    if inputs['control']['ena']:
        if inputs['control']['idx'] == state['idx_max']:
            print('[' + str(inputs['control']['idx']) + '] - APPLICATION NODE RAISES EXCEPTION.')
            raise RuntimeError('Test runtime error')

