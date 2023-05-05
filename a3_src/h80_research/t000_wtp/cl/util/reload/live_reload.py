# -*- coding: utf-8 -*-
"""
Live reload node.

"""


import importlib
import os.path
import time

import stableflow.log


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the live reload component.

    """
    state['runtime']       = runtime
    state['cfg']           = cfg
    state['name_module']   = cfg['py_module']
    state['module']        = importlib.import_module(state['name_module'])
    state['filepath']      = state['module'].__file__
    state['last_modified'] = os.path.getmtime(state['filepath'])
    map_func               = state['module'].__dict__
    state['is_coro']       = 'coro'  in map_func
    state['is_step']       = 'reset' in map_func and 'step' in map_func

    signal = _reset_impl(inputs, state, outputs)
    return signal


# -----------------------------------------------------------------------------
def _reset_impl(inputs, state, outputs):
    """
    Reset using either reset function or coroutine.

    """
    signal = None
    if state['is_step']:

        (outputs, signal) = state['module'].reset(state['runtime'],
                                                  state['cfg'],
                                                  inputs,
                                                  state,
                                                  outputs)

    elif state['is_coro']:

        if '__stableflow_coro__' in state:
            state['__stableflow_coro__'].close()

        state['__stableflow_coro__'] = state['module'].coro(state['runtime'],
                                                        state['cfg'],
                                                        inputs,
                                                        state,
                                                        outputs)

        (outputs, signal) = state['__stableflow_coro__'].send(None)

    else:

        stableflow.log.logger.exception(
                                'No compatible API found in module "{name}"',
                                name = state['name_module'])

    return signal


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the live reload component.

    """
    modified = os.path.getmtime(state['filepath'])
    if state['last_modified'] < modified:
        state['last_modified'] = modified
        _try_reload(inputs, state, outputs)
    _try_step(inputs, state, outputs)


# -----------------------------------------------------------------------------
def _try_reload(inputs, state, outputs):
    """
    Try to reload the specified component.

    """
    signal  = None
    err_msg = None

    while True:

        try:

            importlib.reload(state['module'])

        except Exception as err:

            if err_msg != str(err):
                err_msg = str(err)
                stableflow.log.logger.exception(
                            'Live module reload failed for "{module}"',
                            module = state['name_module'])

            time.sleep(2)

        else:

            # Reset on successful reload
            signal = _reset_impl(inputs, state, outputs)
            break

    return signal


# -----------------------------------------------------------------------------
def _try_step(inputs, state, outputs):
    """
    Try to step the specified component.

    """
    err_msg = None
    while True:
        try:

            if state['is_step']:
                state['module'].step(inputs, state, outputs)
            elif state['is_coro']:
                try:
                    (outputs, signal) = state['__stableflow_coro__'].send(inputs)
                    return signal
                except StopIteration:
                    return (stableflow.signal.exit_ok_controlled,)
            else:
                pass

        except (Exception) as err:
            if err_msg != str(err):
                err_msg = str(err)
                stableflow.log.logger.exception(
                            'Live module step function failed for "{module}"',
                            module = state['name_module'])
            time.sleep(2)
            _try_reload(inputs, state, outputs)
        else:
            return