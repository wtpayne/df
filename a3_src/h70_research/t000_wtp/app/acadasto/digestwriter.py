# -*- coding: utf-8 -*-
"""
Database file hash writer component for acadasto.

"""


import sqlite3

import xact.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the database file hash writer component.

    """
    state['connection'] = sqlite3.connect(cfg['filepath_db'])
    state['cursor']     = state['connection'].cursor()
    state['cursor'].execute(
            ' '.join(('CREATE TABLE IF NOT EXISTS file_digest',
                      '(hexdigest TEXT NOT NULL, filepath TEXT NOT NULL,'
                      'UNIQUE (hexdigest, filepath));')))
    state['cursor'].execute(
            ' '.join(('CREATE INDEX IF NOT EXISTS idx_hexdigest',
                      'ON file_digest (hexdigest);')))
    state['connection'].commit()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the database file hash writer component.

    """
    if not inputs['hexdigest']['ena']:
        return

    list_tuples = list()
    for item in inputs['hexdigest']['list']:
        list_tuples.append((item['hexdigest'], item['filepath']))
    try:
        state['cursor'].executemany(
                ' '.join(('INSERT OR REPLACE INTO file_digest',
                          '(hexdigest, filepath) VALUES (?,?)')),
                list_tuples)
    except sqlite3.OperationalError as err:
        raise
    else:
        state['connection'].commit()
