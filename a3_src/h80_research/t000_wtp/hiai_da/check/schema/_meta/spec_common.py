# -*- coding: utf-8 -*-
"""
Unit tests for the da.check.schema.common package.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."

requirements:
    "This design document may contain any number of requirements
    items embedded in comment blocks. Each requirements item
    that is present shall have one formal requirement statement
    with one modal verb. The modal verb shall be interpreted
    in accordance with iso29148:2011

    SHALL indicates a mandatory binding provision, the fulfillment
    of which must be proven through an appropriate test.

    WILL indicates a statement of fact; futurity; a declaration
    of purpose; or to establish a context or a limitation of use.
    These statements are not manadatory and not binding.

    SHOULD indicates a preference; a goal or an advantageous
    quality. These statements are not mandatory and not binding.

    MAY is used to grant permission or to make a suggestion.
    These statements are not mandatory and not binding."
...
"""


# =============================================================================
class SpecifyIdclassSchema:
    """
    Specify the da.check.schema.common.idclass_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_nonempty_dict(self):
        """
        When called, the idclass_schema() function returns a nonempty dict.

        """
        import da.check.schema.common
        idclass_schema_tab = da.check.schema.common.idclass_schema()
        assert idclass_schema_tab
        assert isinstance(idclass_schema_tab, dict)


# =============================================================================
class SpecifyRequirementItemSchema:
    """
    Specify the da.check.schema.common.requirement_item_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_accepts_a_valid_requirement_item(self, idclass_tab, load):
        """
        The da.check.schema._requirement_item_schema accepts a valid item.

        """
        import da.check.schema.common
        schema = da.check.schema.common.requirement_item_schema(idclass_tab)
        assert schema(load("""
              - "REQUIREMENTS_TEXT_GOES_HERE."
              - type:     information
              - state:    draft
              - ref:
                - i00005_mission
            """)) is not None

        # item_direct = [
        #     "REQUIREMENTS_TEXT_GOES_HERE.",
        #     {'type':     'information'},
        #     {'state':    'draft'},
        #     {'ref':      ['i00005_mission']}
        # ]


# =============================================================================
class SpecifyRequirementSetSchema:
    """
    Specify the da.check.schema.common.requirement_set_schema() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The requirement_set_schema() function is callable.

        """
        import da.check.schema.common
        assert callable(da.check.schema.common.requirement_set_schema)
