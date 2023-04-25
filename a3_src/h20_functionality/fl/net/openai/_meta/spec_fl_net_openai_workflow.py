# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.openai.workflow

"""


import inspect

import pytest


# =============================================================================
class SpecifyFlNetOpenAiWorkflwo:
    """
    Spec for the fl.net.openai.workflow package.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_openai_workflow(self):
        """
        fl.net.openai.workflow can be imported.

        """
        import fl.net.openai.workflow
