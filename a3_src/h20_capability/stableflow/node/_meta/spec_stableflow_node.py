# -*- coding: utf-8 -*-
"""
Functional specification for the stableflow.node package.

"""

# =============================================================================
class SpecifyStableflowNode:
    """
    Spec for stableflow.node package.

    """

    # -------------------------------------------------------------------------
    def it_can_be_imported(self):
        """
        stableflow.node can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """
        import stableflow.node
