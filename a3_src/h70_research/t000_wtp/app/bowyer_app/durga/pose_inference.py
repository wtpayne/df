# -*- coding: utf-8 -*-
"""
Pose inference component.

"""

# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Pose inference coroutine.

    """
    signal                 = None
    outputs['pose']['ena'] = False

    idx = 1

    while True:

        inputs = yield (outputs, signal)

        if not inputs['img']['ena']:
            continue

        idx = idx + 1

        outputs['pose']['ena'] = False
        outputs['pose']['msg'] = "Hello World"
        outputs['pose']['idx'] = idx


# -----------------------------------------------------------------------------
def finalize(runtime, config, inputs, state, outputs):
    """
    Clean up resources.

    """
    pass
