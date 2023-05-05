# -*- coding: utf-8 -*-
"""
Functional specification for the cl.net.crypt component package.

"""


import fl.test.component
import pl.stableflow.sys


# =============================================================================
class SpecifyClNetCrypt:
    """
    Spec for the cl.net.crypt component package.

    """

    #--------------------------------------------------------------------------
    def it_can_do_a_lossless_round_trip(self):
        """
        The obfuscator and deobfuscator components support round-tripping.

        """
        cfg = fl.test.component.pipeline_test_cfg(
                list_pipeline_modules = [
                        'cl.net.util.packer.ic00_edict',
                        'cl.net.crypt.obfuscator.ic00_edict',
                        'cl.net.crypt.deobfuscator.ic00_edict',
                        'cl.net.util.unpacker.ic00_edict'],
                list_pipeline_node_config = [
                        {'fields': ('foo', 'bar'), 'format': 'BB'},
                        {'key':    'ik4ofdebn478dxhb'},
                        {'key':    'ik4ofdebn478dxhb'},
                        {'fields': ('foo', 'bar'), 'format': 'BB'}],
                list_pipeline_edge_info = [
                        [('packed', 'data',   'python_dict')],
                        [('data',   'data',   'python_dict')],
                        [('data',   'packed', 'python_dict')]],
                list_test_vectors = [
                        {'path':   ['data',  'values'],
                         'signal': [{'foo': 0,   'bar': 0},
                                    {'foo': 255, 'bar': 255}]}],
                list_expected_outputs = [
                        {'path':   ['data', 'values'],
                         'signal': [{'foo':   0, 'bar':   0},
                                    {'foo': 255, 'bar': 255}]}])

        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0
