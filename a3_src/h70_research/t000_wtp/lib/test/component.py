# -*- coding: utf-8 -*-
"""
Component test utilities for xact systems.

"""


import pprint

import click.testing
import pytest

import xact.cfg.builder
import xact.cfg.validate
import xact.cli.command
import xact.util.serialization


# -----------------------------------------------------------------------------
def scripted(module, config, script):
    """
    Return configuration for a functional test.

    """

    # Determine all input, output ports mentioned
    # by the script.
    #
    set_name_input  = set()
    set_name_output = set()
    num_steps       = len(script)
    for istep in range(num_steps):
        try:
            set_name_input.update(script[istep]['in'].keys())
        except KeyError:
            pass
        try:
            set_name_output.update(script[istep]['out'].keys())
        except KeyError:
            pass

    # Preallocate some lists for our input and
    # output values from the script.
    #
    empty_msg = {'ena': False, 'list': []}
    map_input = dict()
    for name_input in set_name_input:
        map_input[name_input] = [empty_msg] * num_steps
    map_output = dict()
    for name_output in set_name_output:
        map_output[name_output] = [empty_msg] * num_steps

    # Fill in scripted input, output values
    # whenever they are defined in the script.
    #
    for istep in range(num_steps):
        for name_input in set_name_input:
            try:
                map_input[name_input][istep] = script[istep]['in'][name_input]
            except KeyError:
                pass
        for name_output in set_name_output:
            try:
                map_output[name_output][istep] = script[istep]['out'][name_output]
            except KeyError:
                pass

    list_test_vectors = list()
    for (name_input, list_input) in map_input.items():
        list_test_vectors.append({
            'path':   [name_input],
            'signal': list_input});

    list_expected_outputs = list()
    for (name_output, list_output) in map_output.items():
        list_expected_outputs.append({
            'path':   [name_output],
            'signal': list_output});

    return pipeline_test(
            list_pipeline_modules     = [module],
            list_pipeline_node_config = [config],
            list_pipeline_edge_info   = [],
            list_test_vectors         = list_test_vectors,
            list_expected_outputs     = list_expected_outputs)


# -----------------------------------------------------------------------------
def pipeline_test(list_pipeline_modules,
                  list_pipeline_node_config,
                  list_test_vectors,
                  list_expected_outputs,
                  list_pipeline_edge_info = [],
                  list_id_node_nocontrol  = []):
    """
    Return configuration for a pipeline test.

    """
    num_pipeline_nodes  = len(list_pipeline_modules)
    num_pipeline_config = len(list_pipeline_node_config)
    assert num_pipeline_nodes == num_pipeline_config

    list_id_node       = ['signal_generator']
    for idx in range(num_pipeline_nodes):
        node_name = 'pipeline_node_{idx:03d}'.format(idx = idx)
        list_id_node.append(node_name)
    list_id_node.append('output_evaluator')

    list_py_module = ['xact.lib.test.signal_generator']
    list_py_module.extend(list_pipeline_modules)
    list_py_module.append('xact.lib.test.signal_validator')

    list_config = [{ 'channels': list_test_vectors }]
    list_config.extend(list_pipeline_node_config)
    list_config.append({ 'channels': list_expected_outputs })

    test_vector_edge_info = list()
    for test_vector in list_test_vectors:
        path      = test_vector['path']
        port      = path[0]
        port_src  = port
        port_dst  = port
        data_type = 'python_dict'
        edge      = (port_src, port_dst, data_type)
        test_vector_edge_info.append(edge)

    expected_output_edge_info = list()
    for expected_output in list_expected_outputs:
        path      = expected_output['path']
        port      = path[0]
        port_src  = port
        port_dst  = port
        data_type = 'python_dict'
        edge      = (port_src, port_dst, data_type)
        expected_output_edge_info.append(edge)

    list_edge_info = [test_vector_edge_info]
    list_edge_info.extend(list_pipeline_edge_info)
    list_edge_info.append(expected_output_edge_info)

    cfg = _get_skeleton_component_test()
    xact.cfg.builder.add_pipeline(cfg,
            iter_id_node      = list_id_node,
            spec_id_process   = 'main_process',
            spec_req_host_cfg = 'test_configuration',
            spec_py_module    = list_py_module,
            spec_state_type   = 'python_dict',
            spec_config       = list_config,
            iter_edge_info    = list_edge_info)

    list_id_node_controlled = list(   set(list_id_node)
                                    - set(list_id_node_nocontrol))

    _add_controller(
            cfg,
            subordinate_nodes = list_id_node_controlled,
            idx_max           = _num_samples(list_test_vectors,
                                             key = 'signal'))

    try:
        xact.cfg.validate.normalized(cfg)  # Sanity check
    except xact.cfg.exception.CfgError as err:

        msg = pprint.pformat(cfg) + '\n\n' + str(err)

        pytest.fail(msg = msg, pytrace = False)


    return cfg


# -----------------------------------------------------------------------------
def _num_samples(test_vectors, key):
  """
  Return the number of samples in the specified test vector.

  """
  tup_num_samples = tuple(len(channel[key]) for channel in test_vectors)
  assert _is_all_equal(tup_num_samples)
  num_samples = tup_num_samples[0]
  return num_samples


# -----------------------------------------------------------------------------
def _is_all_equal(itable):
    """
    Return true if all items in the supplied iterable are equal.

    """
    iter_items = iter(itable)
    item_first  = next(iter_items)
    return all(item == item_first for item in iter_items)


# -----------------------------------------------------------------------------
def _get_skeleton_component_test():
    """
    Return configuration data for a skeleton local system.

    """
    cfg = xact.cfg.builder.get_skeleton_config()

    xact.cfg.builder.set_system_id(cfg       = cfg,
                                   id_system = 'xact_test')

    xact.cfg.builder.add_host(cfg            = cfg,
                              id_host        = 'localhost',
                              hostname       = '127.0.0.1',
                              acct_run       = 'xact',
                              acct_provision = 'xact')

    xact.cfg.builder.add_process(cfg        = cfg,
                                 id_process = 'main_process',
                                 id_host    = 'localhost')

    xact.cfg.builder.add_data(cfg       = cfg,
                              id_data   = 'python_dict',
                              spec_data = 'py_dict')

    cfg['req_host_cfg'] = { 'test_configuration': dict() }

    return cfg


# -----------------------------------------------------------------------------
def _add_controller(cfg, subordinate_nodes, idx_max):
    """
    Add a controller.

    """
    xact.cfg.builder.add_node(
                        cfg          = cfg,
                        id_node      = 'controller',
                        id_process   = 'main_process',
                        req_host_cfg = 'test_configuration',
                        py_module    = 'xact.lib.control.system',
                        config       = { 'idx_max':  2 },
                        state_type   = 'python_dict')
    xact.cfg.builder.add_node(
                        cfg          = cfg,
                        id_node      = 'controller_tee',
                        id_process   = 'main_process',
                        req_host_cfg = 'test_configuration',
                        py_module    = 'xact.lib.util.tee',
                        state_type   = 'python_dict')

    xact.cfg.builder.add_edge(
                        cfg     = cfg,
                        id_src  = 'controller',
                        src_ref = 'outputs.control',
                        id_dst  = 'controller_tee',
                        dst_ref = 'inputs.control',
                        data    = 'python_dict')

    for (idx, id_node) in enumerate(subordinate_nodes):
        xact.cfg.builder.add_edge(
                        cfg     = cfg,
                        id_src  = 'controller_tee',
                        src_ref = 'outputs.control_{idx:03d}'.format(idx = idx),
                        id_dst  = id_node,
                        dst_ref = 'inputs.control',
                        data    = 'python_dict')
