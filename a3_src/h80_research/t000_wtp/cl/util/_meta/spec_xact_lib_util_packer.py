# -*- coding: utf-8 -*-
"""
Functional specification for stableflow tee.

"""


import stableflow.lib.test.component


# =============================================================================
class SpecifyPacker:
    """
    Spec for packer module.

    """
    #--------------------------------------------------------------------------
    def it_packs_data(self):
        """
        Test that the packer component packs data.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'stableflow.lib.util.packer'],
                list_pipeline_node_config = [
                        {'fields': ('foo', 'bar'), 'format': 'BB'}],
                list_test_vectors = [
                        {'path':   ['data', 'values'],
                         'signal': [{'foo':   0, 'bar':   0},
                                    {'foo': 255, 'bar': 255}]}],
                list_expected_outputs = [
                        {'path':   ['packed',  'buffer'],
                         'signal': [b'\x00\x00',
                                    b'\xFF\xFF']}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0


    #--------------------------------------------------------------------------
    def it_can_roundtrip_losslessly(self):
        """
        Round trip test for the packer component.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'stableflow.lib.util.packer',
                        'stableflow.lib.util.unpacker'],
                list_pipeline_node_config = [
                        {'fields': ('foo', 'bar'), 'format': 'BB'},
                        {'fields': ('foo', 'bar'), 'format': 'BB'}],
                list_pipeline_edge_info = [
                        [('packed', 'packed', 'python_dict')]],
                list_test_vectors = [
                        {'path':   ['data', 'values'],
                         'signal': [{'foo':   0, 'bar':   0},
                                    {'foo': 255, 'bar': 255}]}],
                list_expected_outputs = [
                        {'path':   ['data', 'values'],
                         'signal': [{'foo':   0, 'bar':   0},
                                    {'foo': 255, 'bar': 255}]}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0
