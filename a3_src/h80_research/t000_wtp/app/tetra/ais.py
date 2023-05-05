# -*- coding: utf-8 -*-
"""
Tetra AIS model component.

"""


import xact.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Tetra AIS model component coroutine.

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