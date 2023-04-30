# -*- coding: utf-8 -*-
"""
Functional specification for cl.net.openai.client.ic00_edict

"""


import inspect

import pytest

import fl.test.component
import pl.stableflow.sys


# =============================================================================
class SpecifyClNetOpenAiClientIc00_edict:
    """
    Spec for the cl.net.openai.client.ic00_edict component.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_cl_net_openai_client_e00_edict(self):
        """
        cl.net.openai.client.ic00_edict can be imported.

        """
        import cl.net.openai.client.ic00_edict

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_creation_of_the_main_coroutine(self):
        """
        cl.net.openai.client.ic00_edict:coro() can be created.

        """
        import cl.net.openai.client.ic00_edict
        component = cl.net.openai.client.ic00_edict.coro(
                                    runtime = None,
                                    cfg     = {},
                                    inputs  = dict(),
                                    state   = dict(),
                                    outputs = dict())
        assert inspect.isgenerator(component)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_runs(self):
        """
        cl.net.openai.client.ic00_edict:coro() rybs.

        """
        cfg = fl.test.component.functional_test_cfg(
                                    module = 'cl.net.openai.client.ic00_edict',
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
        exit_code = pl.stableflow.sys.prep_and_start(map_cfg  = cfg,
                                                     is_local = True)
        assert exit_code == 0
