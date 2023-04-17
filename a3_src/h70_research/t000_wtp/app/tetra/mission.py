# -*- coding: utf-8 -*-
"""
Tetra mission management component.

"""


import xact.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Tetra planner component coroutine.

    """
    signal             = None
    tup_name_output    = ('objective',)
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