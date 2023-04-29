# -*- coding: utf-8 -*-
"""
Functional specification for fl.test.component

"""


import pprint

import pytest


# =============================================================================
class SpecifyFlTestComponent:
    """
    Spec for the fl.test.component package.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_test_component(self):
        """
        fl.test.component can be imported.

        """
        import fl.test.component

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_baseline_configuration(self):
        """
        fl.test.component supports skeleton config generation.

        """
        import fl.test.component
        assert fl.test.component._baseline_configuration() == {
            'data':         { 'python_dict': 'py_dict' },
            'edge':         [],
            'host':         { 'localhost': {
                                'acct_provision':   'stableflow',
                                'acct_run':         'stableflow',
                                'hostname':         '127.0.0.1' }},
            'node':         {},
            'process':      { 'main_process':       {'host': 'localhost'}},
            'req_host_cfg': { 'test_configuration': {}},
            'system':       { 'id_system':          'stableflow_test'}}

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_test_pipeline_configuration(self):
        """
        fl.test.component supports skeleton config generation.

        """
        signal_generator     = 'pl.stableflow.lib.test.signal_generator'
        signal_validator     = 'pl.stableflow.lib.test.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        import fl.test.component
        cfg_output = fl.test.component._pipeline_configuration(
                list_pipeline_modules     = [component_under_test],
                list_pipeline_node_config = [{}],
                list_pipeline_edge_info   = [],
                list_test_vectors         = [{'path':    ['data'],
                                              'signal':  [1, 2, 3, 4, 5]}],
                list_expected_outputs     = [{'path':    ['data'],
                                              'signal':  [2, 4, 6, 8, 10]}])

        cfg_expected = {

            'system': {
                'id_system':            'stableflow_test'},

            'host': {
                'localhost':            {'acct_provision':  'stableflow',
                                         'acct_run':        'stableflow',
                                         'hostname':        '127.0.0.1'}},

            'process': {
                'main_process':         {'host':            'localhost'}},

            'node': {
                'controller': {
                    'config':           {'idx_max': 2},
                    'functionality': {
                        'py_module':    'pl.stableflow.lib.control.system'},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'controller_tee': {
                    'functionality': {
                        'py_module':    'pl.stableflow.lib.util.tee'},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'signal_generator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [1, 2, 3, 4, 5]}]},
                    'functionality':    {'py_module':   signal_generator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'}},
                'pipeline_node_000': {
                    'config':           {},
                    'functionality':    {'py_module':   component_under_test},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'output_evaluator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [2, 4, 6, 8, 10]}]},
                    'functionality':    {'py_module':   signal_validator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},

            'edge': [
                {'data': 'python_dict',
                 'dst': 'pipeline_node_000.inputs.data',
                 'owner': 'signal_generator',
                 'src': 'signal_generator.outputs.data'},
                {'data': 'python_dict',
                 'dst': 'output_evaluator.inputs.data',
                 'owner': 'pipeline_node_000',
                 'src': 'pipeline_node_000.outputs.data'},
                {'data': 'python_dict',
                 'dst': 'controller_tee.inputs.control',
                 'owner': 'controller',
                 'src': 'controller.outputs.control'},
                {'data': 'python_dict',
                 'dst': 'pipeline_node_000.inputs.control',
                 'owner': 'controller_tee',
                 'src': 'controller_tee.outputs.control_000'},
                {'data': 'python_dict',
                 'dst': 'signal_generator.inputs.control',
                 'owner': 'controller_tee',
                 'src': 'controller_tee.outputs.control_001'},
                {'data': 'python_dict',
                 'dst': 'output_evaluator.inputs.control',
                 'owner': 'controller_tee',
                 'src': 'controller_tee.outputs.control_002'}],

            'data': {
                'python_dict': 'py_dict'},

            'req_host_cfg': {
                'test_configuration': {}}}

        str_cfg_output   = pprint.pformat(cfg_output,
                                          indent     = 2,
                                          width      = 100,
                                          compact    = True,
                                          sort_dicts = True)
        str_cfg_expected = pprint.pformat(cfg_expected,
                                          indent     = 2,
                                          width      = 100,
                                          compact    = True,
                                          sort_dicts = True)
        assert str_cfg_expected == str_cfg_expected


