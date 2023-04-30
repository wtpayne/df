# -*- coding: utf-8 -*-
"""
Functional specification for fl.test.component

"""


import pytest


# =============================================================================
class SpecifyFlTestComponent:
    """
    Spec for the fl.test.component module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_test_component(self):
        """
        fl.test.component can be imported with no errors.

        """
        import fl.test.component


# =============================================================================
class SpecifyFlTestComponent_baselineConfiguration:
    """
    Spec for the _baseline_configuration function.

    """

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_baseline_configuration(self):
        """
        _baseline_configuration generates the expected configuration data.

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


# =============================================================================
class SpecifyFlTestComponent_pipelineConfiguration:
    """
    Spec for the _pipeline_test_cfg function.

    """

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_pipeline_test_cfg(self):
        """
        _pipeline_test_cfg generates the expected configuration data.

        """
        import fl.test.component
        controller           = 'cl.core.ctrl.proc.ic00_edict'
        signal_generator     = 'fl.test._meta.signal_generator'
        signal_validator     = 'fl.test._meta.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        cfg_output           = fl.test.component._pipeline_test_cfg(
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
                    'functionality':    {'py_module':    controller},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'signal_generator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [1, 2, 3, 4, 5]}]},
                    'functionality':    {'py_module':   signal_generator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
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
                    'state_type':       'python_dict'}},

            'edge': [
                {'owner':   'signal_generator',
                 'src':     'signal_generator.outputs.data',
                 'dst':     'pipeline_node_000.inputs.data',
                 'data':    'python_dict'},
                {'owner':   'pipeline_node_000',
                 'src':     'pipeline_node_000.outputs.data',
                 'dst':     'output_evaluator.inputs.data',
                 'data':    'python_dict'},
                {'owner':   'controller',
                 'src':     'controller.outputs.control_000',
                 'dst':     'output_evaluator.inputs.control',
                 'data':    'python_dict'},
                {'owner':   'controller',
                 'src':     'controller.outputs.control_001',
                 'dst':     'pipeline_node_000.inputs.control',
                 'data':    'python_dict'},
                {'owner':   'controller',
                 'src':     'controller.outputs.control_002',
                 'dst':     'signal_generator.inputs.control',
                 'data':    'python_dict'}],

            'data': {
                'python_dict': 'py_dict'},

            'req_host_cfg': {
                'test_configuration': {}}}

        assert cfg_output == cfg_expected

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_functional_configuration(self):
        """
        functional_configuration generates the expected configuration data.

        """
        import fl.test.component
        controller           = 'cl.core.ctrl.proc.ic00_edict'
        signal_generator     = 'fl.test._meta.signal_generator'
        signal_validator     = 'fl.test._meta.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        cfg_output           = fl.test.component.functional_test_cfg(
                                    module = component_under_test,
                                    config = dict(),
                                    script = [{'in':  { 'data':  1 },
                                               'out': { 'data':  2 }},
                                              {'in':  { 'data':  2 },
                                               'out': { 'data':  3 }},
                                              {'in':  { 'data':  3 },
                                               'out': { 'data':  6 }},
                                              {'in':  { 'data':  4 },
                                               'out': { 'data':  8 }},
                                              {'in':  { 'data':  5 },
                                               'out': { 'data': 10 }}])
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
                    'functionality':    {'py_module':   controller},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'signal_generator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [1, 2, 3, 4, 5]}]},
                    'functionality':    {'py_module':   signal_generator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'pipeline_node_000': {
                    'config':           {},
                    'functionality': {  'py_module':    component_under_test},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'},
                'output_evaluator': {
                    'config':           {'channels':    [{'path': ['data'],
                                         'signal':      [2, 3, 6, 8, 10]}]},
                    'functionality':    {'py_module':   signal_validator},
                    'process':          'main_process',
                    'req_host_cfg':     'test_configuration',
                    'state_type':       'python_dict'}},

            'edge': [
                {'owner':   'signal_generator',
                 'src':     'signal_generator.outputs.data',
                 'dst':     'pipeline_node_000.inputs.data',
                 'data':    'python_dict'},
                {'owner':   'pipeline_node_000',
                 'src':     'pipeline_node_000.outputs.data',
                 'dst':     'output_evaluator.inputs.data',
                 'data':    'python_dict'},
                {'owner':   'controller',
                 'src':     'controller.outputs.control_000',
                 'dst':     'output_evaluator.inputs.control',
                 'data':    'python_dict'},
                {'owner':   'controller',
                 'src':     'controller.outputs.control_001',
                 'dst':     'pipeline_node_000.inputs.control',
                 'data':    'python_dict'},
                {'owner':   'controller',
                 'src':     'controller.outputs.control_002',
                 'dst':     'signal_generator.inputs.control',
                 'data':    'python_dict'}],

            'data': {
                'python_dict': 'py_dict'},

            'req_host_cfg': {
                'test_configuration': {}}}

        assert cfg_output == cfg_expected
