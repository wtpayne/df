# -*- coding: utf-8 -*-
"""
Functional specification for cl.net.openai.client.ic00_edict

"""


import inspect

import pytest


# =============================================================================
class SpecifyClNetOpenAiClientIc00_edict:
    """
    Spec for the cl.net.openai.client.ic00_edict component.

    """

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

