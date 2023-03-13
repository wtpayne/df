# -*- coding: utf-8 -*-
"""
Functional specification for the stableflow.host package.

"""

# =============================================================================
class SpecifyStableflowHost:
    """
    Spec for stableflow.host package.

    """

    # -------------------------------------------------------------------------
    def it_can_be_imported(self):
        """
        stableflow.host can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """
        import stableflow.host
