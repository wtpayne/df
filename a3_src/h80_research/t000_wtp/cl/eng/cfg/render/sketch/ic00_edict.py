# -*- coding: utf-8 -*-
"""
Bowyer component for sketching the abstract layout of an activity diagram.

"""


import collections
import copy

import stableflow.util


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Augment provided configuration data with abstract layout information.

    """
    signal = None

    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena'] = False
        outputs[id_out]['ts']  = dict()
        outputs[id_out]['map'] = dict()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['map'].clear()

        # For each configuration data structure
        # received, augment it with abstract
        # layout information.
        #
        map_ts = dict()
        map_map_cfg_layout = dict()

        for id_in in inputs.keys():
            if not inputs[id_in]['ena']:
                continue

            if not map_ts:
                map_ts = inputs[id_in]['ts']

            for (id_path, map_cfg_denorm) in inputs[id_in]['map'].items():
                map_cfg_layout              = _layout(map_cfg_denorm)
                map_map_cfg_layout[id_path] = map_cfg_layout

        # Output all augmented configuration
        # data structures to all output ports.
        #
        if map_map_cfg_layout:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['map'].update(map_map_cfg_layout)


# -------------------------------------------------------------------------
def _layout(map_cfg_denorm):
    """
    Augment the specified cfg data with abstract layout information.

    """
    (map_idx_node, map_idx_proc, count_tranche) = _grid_layout(map_cfg_denorm)

    map_cfg_aug = copy.deepcopy(map_cfg_denorm)

    for (id_node, (idx_x, idx_y)) in map_idx_node.items():
        map_cfg_aug['node'][id_node]['idx_x'] = idx_x
        map_cfg_aug['node'][id_node]['idx_y'] = idx_y

    for (id_proc, (idx_x, size_x)) in map_idx_proc.items():
        map_cfg_aug['process'][id_proc]['idx_x']  = idx_x
        map_cfg_aug['process'][id_proc]['size_x'] = size_x

    map_cfg_aug['system']['count_tranche'] = count_tranche

    return map_cfg_aug


# -------------------------------------------------------------------------
def _grid_layout(map_cfg_denorm):
    """
    Lay out nodes, swimlanes and buses in an abstract grid.

    Each grid unit corresponds to a single node.

    """
    list_tranche_global  = stableflow.util.topological_sort(
                                        *_acyclic_data_flow(
                                                map_cfg_denorm['edge']))

    list_id_process      = _sorted_process_list(
                                        map_cfg_denorm,
                                        list_tranche_global)

    map_size_tranche_max = _max_tranche_size(
                                        map_cfg_denorm,
                                        list_tranche_global,
                                        list_id_process)

    map_idx_node         = _2d_node_indices(
                                        map_cfg_denorm,
                                        list_tranche_global,
                                        map_size_tranche_max)

    map_idx_proc         = _2d_process_indices(
                                        list_id_process,
                                        map_size_tranche_max)

    count_tranche        = len(list_tranche_global)

    return (map_idx_node, map_idx_proc, count_tranche)


# -----------------------------------------------------------------------------
def _acyclic_data_flow(iter_cfg_edge, id_process = None):
    """
    Return the data flow graph for the specified process.

    If the process is None, return the data flow graph
    for all edges in the graph.

    The data flow graph is returned as a pair of dicts.
    The first dict maps from upstream nodes to downstream
    nodes, and the second dict maps the reverse, from
    downstream nodes to upstream nodes.

    """
    do_include_all = id_process is None
    map_forward    = collections.defaultdict(set)
    map_backward   = collections.defaultdict(set)

    for cfg_edge in iter_cfg_edge:

        # Decide if we're going to
        # include the current edge.
        #
        is_intra_process = cfg_edge['ipc_type'] == 'intra_process'
        is_local_process = id_process in cfg_edge['list_id_process']
        is_local_edge    = is_intra_process and is_local_process
        do_include_edge  = is_local_edge or do_include_all

        if do_include_edge:

            id_node_src    = cfg_edge['id_node_src']
            id_node_dst    = cfg_edge['id_node_dst']
            is_feedforward = cfg_edge['dirn'] == 'feedforward'

            if is_feedforward:
                map_forward[id_node_src].add(id_node_dst)
                map_backward[id_node_dst].add(id_node_src)
            else:  # is_feedback
                map_backward[id_node_src].add(id_node_dst)
                map_forward[id_node_dst].add(id_node_src)

    return (map_forward, map_backward)


# -----------------------------------------------------------------------------
def _sorted_process_list(map_cfg_denorm, list_tranche_global):
    """
    Return a sorted list of process ids.

    This is intended to be a 'sensible' ordering
    of processes that can be used to arrange
    process-specific swimlanes in a SysML or
    UML activity diagram.

    The returned list of process ids is sorted
    by the index of the first tranche that they
    are involved in processing, then by id_host
    lexicographic order and finally by id_proc
    lexicographic order.

    This means that if the system is overall
    arranged as a pipeline, the swimlanes will
    be sorted in pipeline order, but if it is
    overall arranged as parallel pipelines, then
    the swimlanes will be sorted lexicographically
    by host id and then by process id, giving
    the developer some control over ordering by
    choosing appropirately sortable host and
    process ids.

    """
    # First we get the minimum tranche index
    # for each process (map_idx_tranche_min).
    #
    map_node            = map_cfg_denorm['node']
    map_process         = map_cfg_denorm['process']
    max_idx_tranche     = len(list_tranche_global)
    map_idx_tranche_min = collections.defaultdict(lambda: max_idx_tranche)
    for (idx_tranche, set_id_node) in enumerate(list_tranche_global):
        for id_node in sorted(set_id_node):
            id_process = map_node[id_node]['process']
            map_idx_tranche_min[id_process] = min(
                                idx_tranche, map_idx_tranche_min[id_process])

    # Then we build up a list of tuples containing
    # the keys that we want to sort by, and use
    # it to build a list of process id strings in
    # sorted order. (list_id_process)
    #
    list_tup_key    = list()
    list_id_process = list()
    for (id_process, idx_tranche_min) in map_idx_tranche_min.items():
        id_host = map_process[id_process]['host']
        tup_key = (idx_tranche_min, id_host, id_process)
        list_tup_key.append(tup_key)
    for tup_key in sorted(list_tup_key):
        id_process = tup_key[-1]
        list_id_process.append(id_process)

    return list_id_process


# -----------------------------------------------------------------------------
def _max_tranche_size(map_cfg_denorm, list_tranche_global, list_id_process):
    """
    Return a map from process id to the maximum tranche size for the process.

    This information is needed to size per process
    swimlanes correctly.

    """
    # Work out how many nodes are in each
    # tranche, broken down by process.
    #
    map_node              = map_cfg_denorm['node']
    count_tranche_global  = len(list_tranche_global)
    map_list_size_tranche = dict()
    for id_process in list_id_process:
        map_list_size_tranche[id_process] = [0] * count_tranche_global
    for (idx_tranche, set_id_node) in enumerate(list_tranche_global):
        for id_node in set_id_node:
            id_process = map_node[id_node]['process']
            map_list_size_tranche[id_process][idx_tranche] += 1

    # Work out the maximum tranche size for
    # each process, as this drives how 'wide'
    # the per-process swimlane will need to be.
    #
    map_size_tranche_max = dict()
    for id_process in list_id_process:
        map_size_tranche_max[id_process] = max(map_list_size_tranche[id_process])
    return map_size_tranche_max


# -----------------------------------------------------------------------------
def _2d_node_indices(map_cfg_denorm, list_tranche_global, map_size_tranche_max):
    """
    Return a map of two dimensional indices, one for each node in the graph.

    """
    # Grid positioning transverse to
    # swimlane direction. "x" axis,
    # assuming vertical swimlanes.
    #
    idx_x                 = 0
    map_idx_x_min_process = dict()
    for (id_process, size_tranche_max) in map_size_tranche_max.items():
        map_idx_x_min_process[id_process] = idx_x
        idx_x += size_tranche_max

    # x and y grid position for each node.
    #
    map_node     = map_cfg_denorm['node']
    map_idx_node = dict()
    for (idx_tranche, set_id_node) in enumerate(list_tranche_global):
        for (idx_node, id_node) in enumerate(sorted(set_id_node)):
            id_process            = map_node[id_node]['process']
            idx_x_min_process     = map_idx_x_min_process[id_process]
            idx_x_node            = idx_x_min_process + idx_node
            idx_y_node            = idx_tranche
            map_idx_node[id_node] = (idx_x_node, idx_y_node)

    # Sort by tranche and then by
    # position within the tranche.
    #
    map_idx_node = dict(sorted(map_idx_node.items(),
                               key = lambda item: (item[1], item[0])))

    return map_idx_node


# -----------------------------------------------------------------------------
def _2d_process_indices(list_id_process, map_size_tranche_max):
    """
    Return a map of tuples holding the start index and width of each process.

    This fundtion returns a map from id_process
    to a length two tuple describing the size
    of the corresponding process swimlane.

    The first element of the tuple is the start
    index (in abstract grid units).

    The second element of the tuple is the size
    of the swimlane (in abstract grid units).

    """
    map_idx_proc = dict()
    idx_x        = 0
    for id_proc in list_id_process:
        size_x = map_size_tranche_max[id_proc]
        map_idx_proc[id_proc] = (idx_x, size_x)
        idx_x  += size_x

    return map_idx_proc