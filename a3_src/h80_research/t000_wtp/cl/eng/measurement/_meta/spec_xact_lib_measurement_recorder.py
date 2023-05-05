# -*- coding: utf-8 -*-
"""
Functional specification for the stableflow recorder component.

"""


import os
import pathlib
import tempfile

import stableflow.lib.test
import stableflow.lib.test.component


# =============================================================================
class SpecifyRecorder:
    """
    Spec for the stableflow recorder component.

    """
    def it_records_and_replays(self):
        """
        Test that the data recorder component records and replays.

        """
        with tempfile.TemporaryDirectory() as dirpath_tmp:

            cfg = fl.test.component.pipeline_test_cfg(
                    list_pipeline_modules = [
                            'stableflow.lib.measurement.recorder'],
                    list_pipeline_node_config = [
                            { 'rootpath_rec': dirpath_tmp }],
                    list_pipeline_edge_info = [],
                    list_test_vectors = [
                            {'path':   ['data',  'values'],
                             'signal': [{'foo': 10, 'bar': 100},
                                        {'foo': 20, 'bar': 200},
                                        {'foo': 30, 'bar': 300},
                                        {'foo': 40, 'bar': 400}]}],
                    list_expected_outputs = [
                            {'path':   ['data', 'values'],
                             'signal': [{'foo': 10, 'bar': 100},
                                        {'foo': 20, 'bar': 200},
                                        {'foo': 30, 'bar': 300},
                                        {'foo': 40, 'bar': 400}]}])

            exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                         is_local = True)
            assert exit_code == 0

            list_filepath_rec = list(str(path) for path in
                                     pathlib.Path(dirpath_tmp).rglob('*.rec'))
            assert len(list_filepath_rec) == 1
            filepath_rec = list_filepath_rec[0]
            dirpath_rec  = os.path.dirname(filepath_rec)

            cfg = stableflow.lib.test.component.pipeline_test(
                    list_pipeline_modules = [
                            'stableflow.lib.measurement.player'],
                    list_pipeline_node_config = [
                            { 'dirpath_rec': dirpath_rec }],
                    list_pipeline_edge_info = [],
                    list_test_vectors = [
                            {'path':   ['data',  'values'],
                             'signal': [None,
                                        None,
                                        None,
                                        None]}],
                    list_expected_outputs = [
                            {'path':   ['data', 'values'],
                             'signal': [{'foo': 10, 'bar': 100},
                                        {'foo': 20, 'bar': 200},
                                        {'foo': 30, 'bar': 300},
                                        {'foo': 40, 'bar': 400}]}])

            exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                         is_local = True)
            assert exit_code == 0
