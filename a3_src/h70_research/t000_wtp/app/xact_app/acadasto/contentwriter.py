# -*- coding: utf-8 -*-
"""
Database file content writer component for acadasto.

"""


import sqlite3

import xact.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the database file content writer component.

    """
    state['connection'] = sqlite3.connect(cfg['filepath_db'])
    state['cursor']     = state['connection'].cursor()
    state['cursor'].execute(
            ' '.join(('CREATE TABLE IF NOT EXISTS file_content (',
                      'uid       TEXT    NOT NULL,',
                      'hexdigest TEXT    NOT NULL,',
                      'filepath  TEXT    NOT NULL,',
                      'idx_image INTEGER NOT NULL,',
                      'min_x     INTEGER NOT NULL,',
                      'max_x     INTEGER NOT NULL,',
                      'min_y     INTEGER NOT NULL,',
                      'max_y     INTEGER NOT NULL,',
                      'body      TEXT    NOT NULL)')))
    state['cursor'].execute(
            ' '.join(('CREATE INDEX IF NOT EXISTS idx_hexdigest',
                      'ON file_content (hexdigest);')))
    state['connection'].commit()


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the database file hash writer component.

    """
    if not inputs['chunk']['ena']:
        return

    print('WRITE CONTENT')

    list_tuples = list()
    for item in inputs['chunk']['list']:
        list_tuples.append((item['uid'],
                            item['hexdigest'],
                            item['filepath'],
                            item['idx_image'],
                            item['min_x'],
                            item['max_x'],
                            item['min_y'],
                            item['max_y'],
                            item['body']))
    try:
        state['cursor'].executemany(
                ' '.join(('INSERT OR REPLACE INTO file_content (',
                          'uid,',
                          'hexdigest,',
                          'filepath,',
                          'idx_image,',
                          'min_x,',
                          'max_x,',
                          'min_y,',
                          'max_y,',
                          'body',
                          ') VALUES (?,?,?,?,?,?,?,?,?)')),
                list_tuples)
    except sqlite3.OperationalError as err:
        raise
    else:
        state['connection'].commit()