# -*- coding: utf-8 -*-
"""
Unit tests for the da.timebox module.

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
class SpecifyIdent:
    """
    Specify the da.timebox.ident() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_timebox_identifier(self):
        """
        When given a date, it returns the correponding timebox identifier.

        """
        import datetime
        import da.timebox
        assert da.timebox.ident(datetime.datetime(year   = 2015,
                                                  month  = 10,
                                                  day    = 21)) == '1510B'


# =============================================================================
class SpecifyTimeboxYear:
    """
    Specify the da.timebox.timebox_year() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The timebox_year() function is callable.

        """
        import da.timebox
        assert callable(da.timebox.timebox_year)


# =============================================================================
class SpecifyTimeboxDatesForMonth:
    """
    Specify the da.timebox.timebox_dates_for_month() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The timebox_dates_for_month() function is callable.

        """
        import da.timebox
        assert callable(da.timebox.timebox_dates_for_month)


# =============================================================================
class SpecifyTimeboxStartDate:
    """
    Specify the da.timebox.timebox_start_date() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The timebox_start_date() function is callable.

        """
        import da.timebox
        assert callable(da.timebox.timebox_start_date)
