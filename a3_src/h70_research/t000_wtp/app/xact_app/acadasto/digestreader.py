# -*- coding: utf-8 -*-
"""
Database file hash reader component for acadasto.

"""


import os.path
import sqlite3

import xact.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the database file hash writer component.

    """
    state['batch_size'] = cfg['batch_size']
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
    _run_query(cursor = state['cursor'])


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the database file hash writer component.

    """
    xact.util.clear_outputs(
                    outputs             = outputs,
                    iter_name_output    = ('hexdigest',),
                    iter_field_to_clear = ('list', ))

    if not inputs['control']['ena']:
        return

    list_missing = list()
    list_tuple   = state['cursor'].fetchmany(state['batch_size'])
    if len(list_tuple) == 0:
        _run_query(cursor = state['cursor'])
    else:
        for (hexdigest, filepath) in list_tuple:
            if os.path.isfile(filepath):
                outputs['hexdigest']['list'].append({
                                            'filepath':  filepath,
                                            'hexdigest': hexdigest})
            else:
                list_missing.append((hexdigest, filepath))

    for (hexdigest, filepath) in list_missing:
        print('DELETE: ' + filepath)
        state['cursor'].execute(
            'DELETE FROM file_digest WHERE hexdigest = ? AND filepath = ?',
            (hexdigest, filepath))

    if outputs['hexdigest']['list']:
        outputs['hexdigest']['ena'] = True


# -----------------------------------------------------------------------------
def _run_query(cursor):
    """
    Find files.

    """
    try:
        cursor.execute(
                ' '.join(('SELECT hexdigest, filepath',
                          'FROM file_digest',
                          'ORDER BY hexdigest ASC')))
    except sqlite3.OperationalError as err:
        raise
