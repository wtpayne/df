# -*- coding: utf-8 -*-
"""
Simple analytics component.

"""


import datetime.datetime
import textwrap
import time


#------------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the analytics component.

    """
    state['st_previous'] = None


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the analytics component.

    """
    outputs['rollup']['ena'] = False
    if _is_new_period(inputs['control'], state, 'min'):
        st_most_recent = inputs['time']['gmtime']

        if state['st_previous'] is None:
            state['st_previous'] = _prev_time(st_most_recent, minutes = 1)

        sql_query = ' '.join(textwrap.dedent("""
                SELECT * FROM analytics
                WHERE (minute_idx >= {lo} AND minute_idx < {hi})
                """).splitlines()).format(
                        lo = _minute_index(state['st_previous']),
                        hi = _minute_index(st_most_recent))

        state['st_previous'] = st_most_recent

        outputs['rollup']['ena']   = True
        outputs['rollup']['query'] = sql_query

    outputs['analytics']['ena'] = False
    if inputs['analytics']['ena']:

        outputs['analytics'].clear()
        outputs['analytics']['ena']        = True
        outputs['analytics']['gmtime']     = []
        outputs['analytics']['ts']         = []
        outputs['analytics']['hour_idx']   = []
        outputs['analytics']['minute_idx'] = []

        for analytic in inputs['analytics']['list']:

            gmtime   = inputs['analytics']['gmtime']
            iso_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', gmtime)

            outputs['analytics']['gmtime'].append(iso_time)
            outputs['analytics']['ts'].append(inputs['analytics']['ts'])
            outputs['analytics']['hour_idx'].append(_hour_index(gmtime))
            outputs['analytics']['minute_idx'].append(_minute_index(gmtime))

            for (key, value) in analytic.items():
                if key not in outputs['analytics']:
                    outputs['analytics'][key] = [value]
                else:
                    outputs['analytics'][key].append(value)


# -----------------------------------------------------------------------------
def _minute_index(tup_time):
    """
    Return an integer minute-precision time value to use as the index.

    """
    return int(time.strftime('%Y%j%H%M', tup_time))


# -----------------------------------------------------------------------------
def _hour_index(tup_time):
    """
    Return an integer hour-precision time value to use as the index.

    """
    return int(time.strftime('%Y%j%H', tup_time))


# -----------------------------------------------------------------------------
def _prev_time(gmtime, **kwargs):
    """
    Return the time.

    """
    dt_most_recent = datetime.datetime.fromtimestamp(time.mktime(gmtime))
    dt_previous    = dt_most_recent - datetime.timedelta(**kwargs)
    return dt_previous.timetuple()


# -----------------------------------------------------------------------------
def _is_new_period(input_ctrl, state, name_period):
    """
    Return true if we are in a new period. False otherwise.

    """
    if not input_ctrl['ena']:
        return False

    gmt = input_ctrl['gmtime']
    if name_period == 'mon':
        id_period = (gmt.tm_year, gmt.tm_mon),
    elif name_period == 'week':
        dt_day    = datetime.datetime(gmt.tm_year, gmt.tm_mon, gmt.tm_mday)
        iso_date  = dt_day.isocalendar()
        iso_week  = iso_date[1]
        id_period = (iso_week,)
    elif name_period == 'day':
        id_period = (gmt.tm_year, gmt.tm_yday),
    elif name_period == 'hour':
        id_period = (gmt.tm_year, gmt.tm_yday, gmt.tm_hour),
    elif name_period == 'min':
        id_period = (gmt.tm_year, gmt.tm_yday, gmt.tm_hour, gmt.tm_min),
    elif name_period == 'sec':
        id_period = (gmt.tm_year, gmt.tm_yday,
                     gmt.tm_hour, gmt.tm_min, gmt.tm_sec)
    else:
        raise RuntimeError('Did not recognize name_period.')

    recent_period = 'recent_' + name_period
    if recent_period not in state:
        state[recent_period] = []

    is_new = id_period not in state[recent_period]
    if is_new:
        state[recent_period].append(id_period)
        if len(state[recent_period]) > 2:
            state[recent_period] = sorted(state[recent_period])[2:]

    return is_new
