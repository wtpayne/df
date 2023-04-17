# -*- coding: utf-8 -*-
"""
Tetra estimator component.

Estimation of environmental state including
tracking of collision hazards and other targets
of interest around the platform.

"""


import xact.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Tetra estimator component coroutine.

    """
    signal             = None
    tup_name_output    = ('object',)
    tup_field_to_clear = ('list',)

    xact.util.clear_outputs(
        outputs             = outputs,
        iter_name_output    = tup_name_output,
        iter_field_to_clear = tup_field_to_clear)

    while True:

        inputs = yield (outputs, signal)

        xact.util.clear_outputs(
            outputs             = outputs,
            iter_name_output    = tup_name_output,
            iter_field_to_clear = tup_field_to_clear)

        # IMPL