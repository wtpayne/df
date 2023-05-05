# -*- coding: utf-8 -*-
"""
Functional specification for stableflow bus component.

"""


import fl.test.component
import pl.stableflow.sys


# =============================================================================
class SpecifyBus:
    """
    Spec for bus component.

    """
    #--------------------------------------------------------------------------
    def it_buses_data(self):
        """
        Test that the bus component buses data.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'stableflow.lib.util.bus'],
                list_pipeline_node_config = [
                        None],
                list_test_vectors = [
                        {'path':   ['in1'],
                         'signal': [{'it': 1},
                                    {'it': 2},
                                    {'it': 3},
                                    {'it': 4}]},
                        {'path':   ['in2'],
                         'signal': [{'it': 5},
                                    {'it': 6},
                                    {'it': 7},
                                    {'it': 8}]}],
                list_expected_outputs = [
                        {'path':   ['bus'],
                         'signal': [{ 'in1': {'it': 1}, 'in2': {'it': 5}},
                                    { 'in1': {'it': 2}, 'in2': {'it': 6}},
                                    { 'in1': {'it': 3}, 'in2': {'it': 7}},
                                    { 'in1': {'it': 4}, 'in2': {'it': 8}}]}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0


    #--------------------------------------------------------------------------
    def it_can_roundtrip_with_debus(self):
        """
        Round trip test for the bus component.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'stableflow.lib.util.bus',
                        'stableflow.lib.util.debus'],
                list_pipeline_node_config = [
                        None,
                        None],
                list_pipeline_edge_info = [
                        [('bus', 'bus', 'python_dict')]],
                list_test_vectors = [
                        {'path':   ['in1'],
                         'signal': [{'it': 1},
                                    {'it': 2},
                                    {'it': 3},
                                    {'it': 4}]},
                        {'path':   ['in2'],
                         'signal': [{'it': 5},
                                    {'it': 6},
                                    {'it': 7},
                                    {'it': 8}]}],
                list_expected_outputs = [
                        {'path':   ['in1'],
                         'signal': [{'it': 1},
                                    {'it': 2},
                                    {'it': 3},
                                    {'it': 4}]},
                        {'path':   ['in2'],
                         'signal': [{'it': 5},
                                    {'it': 6},
                                    {'it': 7},
                                    {'it': 8}]}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0
