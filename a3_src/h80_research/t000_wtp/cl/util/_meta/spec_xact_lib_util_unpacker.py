# -*- coding: utf-8 -*-
"""
Functional specification for the stableflow data unpacker component.

"""


import fl.test.component


# =============================================================================
class SpecifyUnpacker:
    """
    Spec for unpacker module.

    """
    #--------------------------------------------------------------------------
    def it_unpacks_data(self):
        """
        Test that the packer component packs data.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'stableflow.lib.util.unpacker'],
                list_pipeline_node_config = [
                        {'fields': ('foo', 'bar'), 'format': 'BB'}],
                list_test_vectors = [
                        {'path':   ['packed',  'buffer'],
                         'signal': [b'\x00\x00',
                                    b'\xFF\xFF']}],
                list_expected_outputs = [
                        {'path':   ['data', 'values'],
                         'signal': [{'foo':   0, 'bar':   0},
                                    {'foo': 255, 'bar': 255}]}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0
