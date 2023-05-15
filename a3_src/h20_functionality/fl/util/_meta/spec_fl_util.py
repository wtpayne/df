# -*- coding: utf-8 -*-
"""
Functional specification for fl.util

"""

import pytest


# =============================================================================
class SpecifyFlUtil:
    """
    Spec for the fl.util module.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_imported(self):
        """
        fl.util can be imported with no errors.

        """
        import fl.util


# =============================================================================
class SpecifyFlUtilBureau:
    """
    Spec for the fl.util.Bureau class.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_instantiated(self):
        """
        fl.util.Bureau can be instantiated with no errors.

        """
        import fl.util
        soi = fl.util.Bureau()
        assert isinstance(soi, fl.util.Bureau)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_used_to_store_simple_values(self):
        """
        fl.util.Bureau can written to and read from.

        """
        import fl.util
        soi          = fl.util.Bureau()
        value        = 100
        soi['field'] = value
        assert soi['field'] == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_use_integer_keys(self):
        """
        fl.util.Bureau can use_integer_keys.

        """
        import fl.util
        soi      = fl.util.Bureau()
        key      = 10
        value    = 100
        soi[key] = value
        assert soi[key] == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_serialised_to_a_string(self):
        """
        fl.util.Bureau can be serialised to a string.

        """
        import fl.util
        soi          = fl.util.Bureau()
        soi['field'] = b'value'
        assert str(soi) == "{'field': b'value'}"

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_accessed_with_dot_notation(self):
        """
        fl.util.Bureau fields can be accessed using dot notation.

        """
        import fl.util
        soi       = fl.util.Bureau()
        value     = 100
        soi.field = value
        assert soi.field == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_fields_on_demand(self):
        """
        fl.util.Bureau creates nested bureaus as fields on demand.

        """
        import fl.util
        soi    = fl.util.Bureau()
        nested = soi['field1']['field2']['field3']
        assert isinstance(nested, fl.util.Bureau)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_write_to_nested_bureaus_as_fields_on_demand(self):
        """
        fl.util.Bureau creates nested bureaus for writing on demand.

        """
        import fl.util
        soi    = fl.util.Bureau()
        value  = 100
        soi['field1']['field2']['field3'] = value
        assert soi['field1']['field2']['field3'] == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_attributes(self):
        """
        fl.util.Bureau creates nested bureaus as attributes on demand.

        """
        import fl.util
        soi                      = fl.util.Bureau()
        value                    = 100
        soi.field1.field2.field3 = value

        assert soi['field1']['field2']['field3'] == value
        assert soi.field1.field2.field3          == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_a_string_path(self):
        """
        fl.util.Bureau creates nested bureaus as a string path on demand.

        """
        import fl.util
        soi                         = fl.util.Bureau()
        value                       = 100
        soi['field1.field2.field3'] = value

        assert soi['field1']['field2']['field3'] == value
        assert soi['field1.field2.field3']       == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_an_iterable_path(self):
        """
        fl.util.Bureau creates nested bureaus as a path on demand.

        """
        import fl.util
        soi                               = fl.util.Bureau()
        value                             = 100
        soi[('field1','field2','field3')] = value

        assert soi['field1']['field2']['field3'] == value
        assert soi[('field1','field2','field3')] == value


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_create_nested_bureaus_as_a_pathform_attribute(self):
        """
        fl.util.Bureau creates nested bureaus as a pathform attrib on demand.

        """
        import fl.util
        soi                      = fl.util.Bureau(path_delimiter = '_')
        value                    = 100
        soi.field1_field2_field3 = value

        assert soi['field1']['field2']['field3'] == value
        assert soi.field1_field2_field3          == value

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_support_undo(self):
        """
        fl.util.Bureau fields can support undoable mutations.

        """
        import fl.util
        soi       = fl.util.Bureau()
        value_1   = 100
        value_2   = 200
        soi.field = value_1
        assert soi.field == value_1
        soi.field = value_2
        assert soi.field == value_2
        soi.undo()
        assert soi.field == value_1
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_support_redo(self):
        """
        fl.util.Bureau fields can support undoable and redoable mutations.

        """
        import fl.util
        soi       = fl.util.Bureau()
        value_1   = 100
        value_2   = 200
        soi.field = value_1
        assert soi.field == value_1
        soi.field = value_2
        assert soi.field == value_2
        soi.undo()
        assert soi.field == value_1
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None
        soi.undo()
        assert soi.field == None
        soi.redo()
        assert soi.field == value_1
        soi.redo()
        assert soi.field == value_2

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_support_callbacks(self):
        """
        fl.util.Bureau fields can support callbacks.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_callback(cmd):
            """
            Test callback.

            """
            nonlocal value_written
            nonlocal path_written
            value_written = cmd.value_new
            path_written  = cmd.path

        import fl.util
        soi   = fl.util.Bureau()
        key   = 'field_1'
        value = 100
        soi.add_callback(key, _test_callback)
        soi[key] = value
        assert value_written == value
        assert path_written  == (key,)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_support_callbacks_on_nested_fields(self):
        """
        fl.util.Bureau fields can support callbacks.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_callback(cmd):
            """
            Test callback.

            """
            nonlocal value_written
            nonlocal path_written
            value_written = cmd.value_new
            path_written  = cmd.path

        import fl.util
        soi    = fl.util.Bureau()
        value1 = 100
        value2 = 200
        soi.add_callback('field_1.field_2', _test_callback)
        soi.field_1.field_2 = value1
        soi.field3          = value2
        assert value_written == value1
        assert path_written  == ('field_1', 'field_2')

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_triggers_callback_if_nested_field_is_changed(self):
        """
        fl.util.Bureau callbacks are called if a nested field is changed.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_callback(cmd):
            """
            Test callback.

            """
            nonlocal value_written
            nonlocal path_written
            value_written = cmd.value_new
            path_written  = cmd.path

        import fl.util
        soi = fl.util.Bureau()
        soi.add_callback('field_1', _test_callback)
        soi.field_1.field_2 = 100
        assert value_written == 100
        assert path_written  == ('field_1', 'field_2')

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_represented_as_a_key_value_tuple(self):
        """
        fl.util.Bureau containers can be represented as key-value tuples.

        """
        import fl.util
        soi     = fl.util.Bureau()
        soi.a.c = 100
        soi.a.d = 200
        soi.b.e = 300
        soi.b.f = 400

        assert soi.as_key_value_tuple() == ((('a', 'c'), 100),
                                            (('a', 'd'), 200),
                                            (('b', 'e'), 300),
                                            (('b', 'f'), 400))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_represented_as_a_nested_dict(self):
        """
        fl.util.Bureau containers can be represented as a nested dict.

        """
        import fl.util
        soi     = fl.util.Bureau()
        soi.a.c = 100
        soi.a.d = 200
        soi.b.e = 300
        soi.b.f = 400

        assert soi.as_nested_dict() == {'a': {'c': 100, 'd': 200},
                                        'b': {'e': 300, 'f': 400}}

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_keeps_a_journal(self):
        """
        fl.util.Bureau containers keep a journal of operations.

        """
        import fl.util
        soi     = fl.util.Bureau()
        soi.a.c = 100
        soi.a.d = 200
        soi.b.e = 300
        soi.b.f = 400
        soi.b.f = 500
        soi.undo()
        soi.redo()

        iter_journal    = soi.journal_pop()
        tup_tup_journal = tuple(tuple(item) for item in iter_journal)

        import pprint
        pprint.pprint(tup_tup_journal)

        assert tup_tup_journal == (('edit', ('a', 'c'), 100, None ),
                                   ('edit', ('a', 'd'), 200, None ),
                                   ('edit', ('b', 'e'), 300, None ),
                                   ('edit', ('b', 'f'), 400, None ),
                                   ('edit', ('b', 'f'), 500, 400  ),
                                   ('undo', ('b', 'f'), 400, 500  ),
                                   ('redo', ('b', 'f'), 500, 400  ))
