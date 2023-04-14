# -*- coding: utf-8 -*-
"""
Dynamic topology layer worker component.

"""


import datetime
import time

import dill


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the worker.

    """
    pass


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Worker step.

    """
    function = dill.loads(pickled_function)

