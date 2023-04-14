# -*- coding: utf-8 -*-
"""
Bowyer component for transforming bowyer configuration data.

"""


import bowyer.cfg


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Yield transformed configuration data from the supplied raw config data.

    On each model step a dict of raw configuration
    data is recieved as input.

    For each of the received raw configuration data
    structures, SOMETHING STRANGE HAPPENS.

    All transformed variants created in the current
    model step are then placed in a dictionary and
    output.

    """
    signal          = None
    map_cfg_stored  = dict()
    map_cfg_changed = dict()

    # Initialize outputs when the system
    # first starts, preallocating memory
    # if appropriate.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena'] = True
        outputs[id_out]['ts']  = dict()
        outputs[id_out]['map'] = dict()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs at the beginning
        # of each simulation step.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['map'].clear()

        if not inputs['control']['ena']:
            continue
        map_ts = inputs['control']['ts']

        # Update list of commands.
        #
        list_cmd = list()
        if inputs['cmd']['ena']:
            list_cmd.extend(inputs['cmd']['list'])
            inputs['cmd']['ena'] = False

        # Update stored and changed config.
        #
        map_cfg_changed = dict()
        if inputs['cfg']['ena']:
            for (id_path, cfg_raw) in inputs['cfg']['map'].items():
                cfg_raw['last_edit'] = {}
                map_cfg_changed[id_path] = cfg_raw
        map_cfg_stored.update(map_cfg_changed)

        # Apply command and update stored and changed config.
        #
        for cmd in list_cmd:
            id_path     = cmd['id_path']
            id_system   = cmd['id_system']
            id_node     = cmd['id_node']
            id_resource = cmd['id_resource']
            cfg_stored  = map_cfg_stored[id_path]
            cfg_node    = cfg_stored['node'][id_node]

            if 'class' not in cfg_node:
                cfg_node['class'] = list()
            cfg_node['class'] = list(set(cfg_node['class']))  # Deduplicate

            if 'selected' in cfg_node['class']:
                cfg_node['class'].remove('selected')
            else:
                cfg_node['class'].append('selected')

            cfg_stored['last_edit'] = cmd

            map_cfg_changed[id_path] = cfg_stored

        # Lookup which cfg to transform.
        # Get transform parameters
        # Do model transforma
        #
        # path_cfg    = '/media/wtp/Data/dev/bowyer_lib/src/bowyer/app/ratio/ratio.cfg.yaml'
        # cfg_raw     = map_cfg_stored[path_cfg]
        # cfg_changed = _transform(cfg_raw, cmd)
        # map_cfg_changed

        # If any data has been loaded,
        # then output it.
        #
        if map_cfg_changed:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['map'].update(map_cfg_changed)


# -----------------------------------------------------------------------------
def _transform(cfg_raw, cmd):
    """
    Apply the transformation.

    """

    id_node_upstream = 'ctrl_sys'
    id_node_new      = 'do_nothing'

    cfg_raw['last_edit'] = cmd

    cfg_raw['node'].update({
        id_node_new: {
            'process':              'proc_main',
            'req_host_cfg':         'default_configuration',
            'functionality': {
                'py_module':        'bowyer.lib.util.noop' },
            'state_type':           'py_dict'}})

    cfg_raw['edge'].append({
        'owner': id_node_new,
        'data':  'py_dict',
        'src':   '{id_node}.outputs.dummy'.format(
                                            id_node = id_node_upstream),
        'dst':   '{id_node}.inputs.dummy'.format(
                                            id_node = id_node_new)})

    return cfg_raw