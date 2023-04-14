# -*- coding: utf-8 -*-
"""
Reporter component for acadasto.

"""


import sqlite3

import xact.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the reporter component.

    """
    pass


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the reporter component.

    """
    print('REPORTER')
