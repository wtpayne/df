# -*- coding: utf-8 -*-
"""
Cache post-pipeline component.

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
    xact.util.clear_outputs(outputs             = outputs,
                            iter_name_output    = ('results', ),
                            iter_field_to_clear = ('list', ))

    if inputs['cached_results']['ena']:
        outputs['results'].update(inputs['cached_results'])

    elif inputs['computed_results']['ena']:
        outputs['results'].update(inputs['computed_results'])
        _try_write_cache(connection = state['connection'],
                         cursor     = state['cursor'],
                         parameters = inputs['parameters'],
                         item       = inputs['computed_results'])


# -----------------------------------------------------------------------------
def _ensure_cache_exists(cursor):
    """
    Make sure the cache table exists in the database.

    """
    cursor.execute(' '.join((
            'CREATE TABLE IF NOT EXISTS cache',
            '(key TEXT PRIMARY KEY, value BLOB NOT NULL);')))


# -----------------------------------------------------------------------------
def _try_write_cache(connection, cursor, parameters, item):
    """
    Try to write a line item to the cache.

    """
    try:
        cursor.execute(' '.join((
                'INSERT INTO cache VALUES',
                '("{key}", "{value}");'.format(
                        key   = xact.util.serialization.hexdigest(parameters),
                        value = xact.util.serialization.serialize(item)))))
    except sqlite3.OperationalError as err:
        raise
    else:
        connection.commit()