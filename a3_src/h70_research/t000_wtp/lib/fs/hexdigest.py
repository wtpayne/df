# -*- coding: utf-8 -*-
"""
File hash component for detecting duplicate (identical) files.

"""


import xact.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the file hash component.

    """
    pass


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Compute the hash of all supplied files.

    """
    xact.util.clear_outputs(
                    outputs             = outputs,
                    iter_name_output    = ('hexdigest',),
                    iter_field_to_clear = ('list', ))

    if not inputs['filepath']['ena']:
        return

    for filepath in inputs['filepath']['list']:
        outputs['hexdigest']['list'].append({
                                        'filepath':  filepath,
                                        'hexdigest': _hexdigest(filepath)})

    if outputs['hexdigest']['list']:
        outputs['hexdigest']['ena'] = True


# -----------------------------------------------------------------------------
def _hexdigest(filepath):
    """
    Return the hash hex digest for the specified file.

    """
    with open(filepath, 'rb') as file:
        bytes_buffer = file.read()
        str_hash     = xact.util.serialization.hexdigest(bytes_buffer)
        return str_hash
