# -*- coding: utf-8 -*-
"""
Unit tests for the autodata.fundamental_type module.

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
class Specify_TypeinfoTable:
    """
    Specify the _typeinfo_table() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_tuple_of_typeinfo_named_tuples(self):
        """
        The _typeinfo_table() returns a tuple of typeinfo named tuples.

        """
        import autodata.fundamental_type

        # The _typeinfo_table is a tuple.
        table = autodata.fundamental_type._typeinfo_table()
        assert isinstance(table, tuple)

        expected_row_type   = 'TypeInfo'
        expected_row_fields = ('name', 'py', 'py_eq', 'c', 'c_eq', 'ctypes')

        # _typeinfo_table tuple contains only TypeInfo named tuples.
        for row in table:
            row_type = type(row)
            assert row_type.__name__ == expected_row_type
            assert row_type._fields == expected_row_fields


# =============================================================================
class Specify_TypeinfoIndex:
    """
    Specify the _typeinfo_index() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_map_of_typeinfo_named_tuples(self):
        """
        The _typeinfo_index() returns a dict of typeinfo named tuples.

        """
        import autodata.fundamental_type
        lut = autodata.fundamental_type._typeinfo_index()

        assert isinstance(lut, dict)


# =============================================================================
class SpecifyNames:
    """
    Specify the fundamental_type.names() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_tuple_of_unique_strings(self):
        """
        The name() function returns a tuple of strings, all unique.

        """
        import autodata.fundamental_type
        tup_names = autodata.fundamental_type.names()

        # names() returns a tuple.
        assert isinstance(tup_names, tuple)

        # The returned names are unique.
        assert len(set(tup_names)) == len(tup_names)

        # All of the names are strings.
        for str_name in tup_names:
            assert isinstance(str_name, str)


# =============================================================================
class SpecifyLookup:
    """
    Specify the fundamental_type.lookup() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_list_of_typeinfo_named_tuple(self):
        """
        The lookup() function returns a list of typeinfo named tuples.

        """
        import autodata.fundamental_type
        list_typeinfo = autodata.fundamental_type.lookup(int)

        # lookup() returns a list.
        assert isinstance(list_typeinfo, list)

        # All of the items in the returned list
        # are TypeInfo named tuples.
        expected_item_type   = 'TypeInfo'
        expected_item_fields = ('name', 'py', 'py_eq', 'c', 'c_eq', 'ctypes')

        for item in list_typeinfo:

            item_type = type(item)
            assert item_type.__name__ == expected_item_type
            assert item_type._fields == expected_item_fields

    # -------------------------------------------------------------------------
    def it_accepts_a_typename_string(self):
        """
        The lookup() function accepts as input a typename string.

        """
        import autodata.fundamental_type
        retval = autodata.fundamental_type.lookup('int64')
        assert retval

    # -------------------------------------------------------------------------
    def it_accepts_a_type_character_code(self):
        """
        The lookup() function accepts as input a typename string.

        """
        import autodata.fundamental_type
        retval = autodata.fundamental_type.lookup('i')
        assert retval


# =============================================================================
class SpecifyIsFundamental:
    """
    Specify the fundamental_type.is_fundamental() function.

    """

    # -------------------------------------------------------------------------
    def it_returns_a_boolean(self):
        """
        The is_fundamental() function returns a boolean.

        """
        import autodata.fundamental_type

        # unit8 is a fundamental type.
        assert autodata.fundamental_type.is_fundamental('uint8')

        # foobar is not a fundamental type.
        assert not autodata.fundamental_type.is_fundamental('foobar')
