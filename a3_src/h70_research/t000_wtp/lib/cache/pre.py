# -*- coding: utf-8 -*-
"""
Cache pre-pipeline component.

"""


import sqlite3

import xact.util.serialization


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the cache reader component.

    """
    state['connection'] = sqlite3.connect(cfg['filepath_db'])
    state['cursor']     = state['connection'].cursor()
    _ensure_cache_exists(cursor = state['cursor'])


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the cache reader component.

    """
    outputs['cached_results'].clear()
    outputs['cached_results']['ena'] = False

    outputs['params_compute'].clear()
    outputs['params_compute']['ena'] = False

    outputs['params_cache'].clear()
    outputs['params_cache']['ena'] = False

    if not inputs['parameters']['ena']:
        return

    print('TRY READ')
    cache_item = _try_read_cache(cursor     = state['cursor'],
                                 parameters = inputs['parameters'])
    print('TRY READ COMPLETE')
    if cache_item:
        outputs['cached_results'].update(cache_item)

    else:
        outputs['params_compute'].update(inputs['parameters'])
        outputs['params_cache'].update(inputs['parameters'])


# -----------------------------------------------------------------------------
def _ensure_cache_exists(cursor):
    """
    Make sure the cache table exists in the database.

    """
    cursor.execute(' '.join((
            'CREATE TABLE IF NOT EXISTS cache',
            '(key TEXT PRIMARY KEY, value BLOB NOT NULL);')))


# -----------------------------------------------------------------------------
def _try_read_cache(cursor, parameters):
    """
    Try to read a line item from the cache.

    """
    try:
        cursor.execute(' '.join((
                'SELECT value FROM cache',
                'WHERE key = "{key}";'.format(
                        key = xact.util.serialization.hexdigest(parameters)))))
    except sqlite3.OperationalError as err:
        raise
    else:
        result = cursor.fetchone()
        if result:
            return xact.util.serialization.deserialize(result[0])
        else:
            return None
