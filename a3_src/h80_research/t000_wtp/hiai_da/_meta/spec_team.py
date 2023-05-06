# -*- coding: utf-8 -*-
"""
Unit tests for the team module.

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
class SpecifyMemberId:
    """
    Specify the da.team.member_id() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_valid_member_id(self):
        """
        When given a valid user_id a valid member_id is returned.

        """
        import da.team
        member_id = da.team.member_id(user_id = 'wtp')
        assert member_id.startswith('t')


# =============================================================================
class Specify_CurrentUser:
    """
    Specify the da.team._current_user() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_valid_user_id(self):
        """
        A valid user_id is returned.

        """
        import da.team
        current_user = da.team._current_user()
        assert len(current_user) > 0


# =============================================================================
class Specify_GenerateMatchingMembers:
    """
    Specify the da.team._generate_matching_members() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _generate_matching_members() function is callable

        """
        import da.team
        assert callable(da.team._generate_matching_members)
