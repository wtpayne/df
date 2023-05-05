# -*- coding: utf-8 -*-
"""
Functional specification for stableflow tee.

"""


import stableflow.lib.test.component


# =============================================================================
class SpecifyTee:
    """
    Spec for tee module.

    """
    #--------------------------------------------------------------------------
    def it_duplicates_outputs(self):
        """
        Test that the tee component duplicates outputs.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'stableflow.lib.util.tee'],
                list_id_node_nocontrol = [
                        'pipeline_node_000'],
                list_pipeline_node_config = [{}],
                list_test_vectors = [
                        {'path':   ['signal', 'values'],
                         'signal': [0, 10, 20, 30, 40, 50]}],
                list_expected_outputs = [
                        {'path':   ['first_copy',  'values'],
                         'signal': [0, 10, 20, 30, 40, 50]},
                        {'path':   ['second_copy',  'values'],
                         'signal': [0, 10, 20, 30, 40, 50]}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0

