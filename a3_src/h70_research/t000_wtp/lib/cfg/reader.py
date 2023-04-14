# -*- coding: utf-8 -*-
"""
Xact component for reading configuration.

"""


import xact.cfg
import xact.cfg.exception


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the filesystem walk component.

    """
    pass

# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the filesystem walk component.

    """
    xact.util.clear_outputs(outputs             = outputs,
                            iter_name_output    = ('cfg', ),
                            iter_field_to_clear = ('map', ))

    if inputs['filepath']['ena']:
        for filepath in inputs['filepath']['list']:
            try:
                cfg = xact.cfg.prepare(filepath)
            except xact.cfg.exception.CfgError:
                continue
            else:
                if cfg:
                    id_system = cfg['system']['id_system']
                    outputs['cfg']['map'][id_system] = cfg

    if outputs['cfg']['map']:
        outputs['cfg']['ena'] = True