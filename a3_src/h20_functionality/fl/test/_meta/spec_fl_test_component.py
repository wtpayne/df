# -*- coding: utf-8 -*-
"""
Functional specification for fl.test.component

"""


import pprint

import click.testing
import pytest


# -----------------------------------------------------------------------------
def run(cfg,  # pylint: disable=R0913
        expected_exit_code = 0,
        do_expect_stdout   = False,
        do_expect_stderr   = False,
        expected_stdout    = None,
        expected_stderr    = None):
    """
    Run a test via the command line interface.

    """
    runner   = click.testing.CliRunner(mix_stderr = False)
    response = runner.invoke(xact.cli.command.grp_main,
                             ['system', 'start', '--local',
                              '--cfg', xact.util.serialization.serialize(cfg)])

    isok_exit_code = response.exit_code == expected_exit_code
    isok_stdout    = _isok(response.stdout, do_expect_stdout, expected_stdout)
    isok_stderr    = _isok(response.stderr, do_expect_stderr, expected_stderr)

    isok = (isok_exit_code and isok_stdout and isok_stderr)

    if isok:
        return

    msg = ''
    if not isok_exit_code:
        msg += 'exit_code:\n{exit_code}\n\n'.format(
                                                exit_code = response.exit_code)

    if not isok_stdout:
        msg += 'stdout:\n{stdout}\n\n'.format(stdout = response.stdout)

    if not isok_stderr:
        msg += 'stderr:\n{stderr}\n\n'.format(stderr = response.stderr)

    pytest.fail(msg = msg, pytrace = False)


# -----------------------------------------------------------------------------
def _isok(response_output, do_expect_output, expected_output):
    """
    Return true iff response is OK.

    """
    has_output = response_output != ''
    if has_output != do_expect_output:
        return False

    if expected_output is not None:
        if response_output != expected_output:
            return False

    return True


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
    Spec for the _pipeline_configuration function.

    """

    #--------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_generation_of_pipeline_configuration(self):
        """
        _pipeline_configuration generates the expected configuration data.

        """
        import fl.test.component
        controller           = 'pl.stableflow.lib.control.system'
        signal_generator     = 'pl.stableflow.lib.test.signal_generator'
        signal_validator     = 'pl.stableflow.lib.test.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        cfg_output           = fl.test.component._pipeline_configuration(
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
                {'data':    'python_dict',
                 'dst':     'pipeline_node_000.inputs.data',
                 'owner':   'signal_generator',
                 'src':     'signal_generator.outputs.data'},
                {'data':    'python_dict',
                 'dst':     'output_evaluator.inputs.data',
                 'owner':   'pipeline_node_000',
                 'src':     'pipeline_node_000.outputs.data'},
                {'data':    'python_dict',
                 'dst':     'controller_tee.inputs.control',
                 'owner':   'controller',
                 'src':     'controller.outputs.control'},
                {'data':    'python_dict',
                 'dst':     'output_evaluator.inputs.control',
                 'owner':   'controller_tee',
                 'src':     'controller_tee.outputs.control_000'},
                {'data':    'python_dict',
                 'dst':     'pipeline_node_000.inputs.control',
                 'owner':   'controller_tee',
                 'src':     'controller_tee.outputs.control_001'},
                {'data':    'python_dict',
                 'dst':     'signal_generator.inputs.control',
                 'owner':   'controller_tee',
                 'src':     'controller_tee.outputs.control_002'}],

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
        controller           = 'pl.stableflow.lib.control.system'
        signal_generator     = 'pl.stableflow.lib.test.signal_generator'
        signal_validator     = 'pl.stableflow.lib.test.signal_validator'
        component_under_test = 'fl.test._meta.multiply_by_two'
        cfg_output           = fl.test.component.functionalConfiguration(
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

            'edge':  [
                {'data':  'python_dict',
                 'dst':   'pipeline_node_000.inputs.data',
                 'owner': 'signal_generator',
                 'src':   'signal_generator.outputs.data'},

                {'data':  'python_dict',
                 'dst':   'output_evaluator.inputs.data',
                 'owner': 'pipeline_node_000',
                 'src':   'pipeline_node_000.outputs.data'},

                {'data':  'python_dict',
                 'dst':   'controller_tee.inputs.control',
                 'owner': 'controller',
                 'src':   'controller.outputs.control'},

                {'data':  'python_dict',
                 'dst':   'output_evaluator.inputs.control',
                 'owner': 'controller_tee',
                 'src':   'controller_tee.outputs.control_000'},

                {'data':  'python_dict',
                 'dst':   'pipeline_node_000.inputs.control',
                 'owner': 'controller_tee',
                 'src':   'controller_tee.outputs.control_001'},

                {'data':  'python_dict',
                 'dst':   'signal_generator.inputs.control',
                 'owner': 'controller_tee',
                 'src':   'controller_tee.outputs.control_002'}],

            'data': {
                'python_dict': 'py_dict'},

            'req_host_cfg': {
                'test_configuration': {}}}

        assert cfg_output == cfg_expected
