# -*- coding: utf-8 -*-
"""
Xact component for UDP data reception.

"""


import sqlite3

import stableflow.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the udprx component.

    """
    pass


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the udprx component.

    """
    print('UDPRX')
