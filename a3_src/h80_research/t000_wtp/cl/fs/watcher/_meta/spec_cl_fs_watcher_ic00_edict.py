# -*- coding: utf-8 -*-
"""
Functional specification for cl.db.sqlite.ic00_edict.

"""

import pytest


# =============================================================================
class SpecifyClDbSqliteIc00_edict:
    """
    Spec for the cl.db.sqlite.ic00_edict component.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        cl.db.sqlite.ic00_edict can be imported.

        """
        import cl.db.sqlite.ic00_edict

