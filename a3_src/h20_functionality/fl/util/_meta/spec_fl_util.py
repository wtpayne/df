# -*- coding: utf-8 -*-
"""
Functional specification for fl.util

"""


import textwrap
import time

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
    def it_can_trigger_rules(self):
        """
        Editing fl.util.Bureau fields will trigger relevant rules.

        """

        value_written = None
        path_written  = None

        # ---------------------------------------------------------------------
        def _test_function(data, tup_cmd):
            """
            Test function.

            """
            nonlocal value_written
            nonlocal path_written
            value_written = tup_cmd[0].value_new
            path_written  = tup_cmd[0].path

        import fl.util
        soi   = fl.util.Bureau()
        key   = 'field_1'
        value = 100
        soi.add_rule(fl.util.Rule(condition = (lambda cmd: True,),
                                  action    = _test_function))

        with soi.batch_context():
            soi[key] = value

        assert value_written == value
        assert path_written  == (key,)

    # # -------------------------------------------------------------------------
    # @pytest.mark.e002_general_research
    # def it_can_support_callbacks_on_nested_fields(self):
    #     """
    #     fl.util.Bureau fields can support callbacks.

    #     """

    #     value_written = None
    #     path_written  = None

    #     # ---------------------------------------------------------------------
    #     def _test_callback(tup_cmd):
    #         """
    #         Test callback.

    #         """
    #         nonlocal value_written
    #         nonlocal path_written
    #         value_written = tup_cmd[0].value_new
    #         path_written  = tup_cmd[0].path

    #     import fl.util
    #     soi    = fl.util.Bureau()
    #     value1 = 100
    #     value2 = 200
    #     soi.add_callback('field_1.field_2', _test_callback)

    #     with soi.batch_context():
    #         soi.field_1.field_2 = value1
    #         soi.field3          = value2

    #     assert value_written == value1
    #     assert path_written  == ('field_1', 'field_2')

    # # -------------------------------------------------------------------------
    # @pytest.mark.e002_general_research
    # def it_triggers_callback_if_nested_field_is_changed(self):
    #     """
    #     fl.util.Bureau callbacks are called if a nested field is changed.

    #     """

    #     value_written = None
    #     path_written  = None

    #     # ---------------------------------------------------------------------
    #     def _test_callback(tup_cmd):
    #         """
    #         Test callback.

    #         """
    #         nonlocal value_written
    #         nonlocal path_written
    #         value_written = tup_cmd[0].value_new
    #         path_written  = tup_cmd[0].path

    #     import fl.util
    #     soi = fl.util.Bureau()
    #     soi.add_callback('field_1', _test_callback)

    #     with soi.batch_context():
    #         soi.field_1.field_2 = 100

    #     assert value_written == 100
    #     assert path_written  == ('field_1', 'field_2')

    # # -------------------------------------------------------------------------
    # @pytest.mark.e002_general_research
    # def it_can_be_represented_as_a_key_value_tuple(self):
    #     """
    #     fl.util.Bureau containers can be represented as key-value tuples.

    #     """
    #     import fl.util
    #     soi     = fl.util.Bureau()
    #     soi.a.c = 100
    #     soi.a.d = 200
    #     soi.b.e = 300
    #     soi.b.f = 400

    #     assert soi.to_tuple() == ((('a', 'c'), 100),
    #                               (('a', 'd'), 200),
    #                               (('b', 'e'), 300),
    #                               (('b', 'f'), 400))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_key_value_tuple(self):
        """
        fl.util.Bureau containers can be updated using key-value tuples.

        """
        import fl.util
        soi = fl.util.Bureau()
        soi.from_tuple(((('a', 'c'), 100),
                       (('a', 'd'), 200),
                       (('b', 'e'), 300),
                       (('b', 'f'), 400)))
        assert soi.a.c == 100
        assert soi.a.d == 200
        assert soi.b.e == 300
        assert soi.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_tuple_rooted_key_value_tuple(self):
        """
        fl.util.Bureau containers can be partly updated using key-value tuples.

        """
        import fl.util
        soi = fl.util.Bureau()
        soi.from_tuple(path_root = ('root', 'path'),
                       tup_kv    = ((('a', 'c'), 100),
                                    (('a', 'd'), 200),
                                    (('b', 'e'), 300),
                                    (('b', 'f'), 400)))
        assert soi.root.path.a.c == 100
        assert soi.root.path.a.d == 200
        assert soi.root.path.b.e == 300
        assert soi.root.path.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_string_rooted_key_value_tuple(self):
        """
        fl.util.Bureau containers can be partly updated using key-value tuples.

        """
        import fl.util
        soi = fl.util.Bureau()
        soi.from_tuple(path_root = 'root.path',
                       tup_kv    = ((('a', 'c'), 100),
                                    (('a', 'd'), 200),
                                    (('b', 'e'), 300),
                                    (('b', 'f'), 400)))
        assert soi.root.path.a.c == 100
        assert soi.root.path.a.d == 200
        assert soi.root.path.b.e == 300
        assert soi.root.path.b.f == 400

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

        assert soi.to_dict()   == {'a': {'c': 100, 'd': 200},
                                   'b': {'e': 300, 'f': 400}}
        assert soi.a.to_dict() == {'c': 100, 'd': 200}
        assert soi.b.to_dict() == {'e': 300, 'f': 400}

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_nested_dict(self):
        """
        fl.util.Bureau containers can be updated from a nested dict.

        """
        import fl.util
        soi = fl.util.Bureau()
        soi.from_dict({'a': {'c': 100, 'd': 200},
                       'b': {'e': 300, 'f': 400}})
        assert soi.a.c == 100
        assert soi.a.d == 200
        assert soi.b.e == 300
        assert soi.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_tuple_rooted_nested_dict(self):
        """
        fl.util.Bureau containers can be updated from a nested dict.

        """
        import fl.util
        soi = fl.util.Bureau()
        soi.from_dict(path_root = ('root', 'path'),
                      map_item  = {'a': {'c': 100, 'd': 200},
                                   'b': {'e': 300, 'f': 400}})
        assert soi.root.path.a.c == 100
        assert soi.root.path.a.d == 200
        assert soi.root.path.b.e == 300
        assert soi.root.path.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_string_rooted_nested_dict(self):
        """
        fl.util.Bureau containers can be updated from a nested dict.

        """
        import fl.util
        soi = fl.util.Bureau()
        soi.from_dict(path_root = 'rootpath',
                      map_item  = {'a': {'c': 100, 'd': 200},
                                   'b': {'e': 300, 'f': 400}})
        assert soi.rootpath.a.c == 100
        assert soi.rootpath.a.d == 200
        assert soi.rootpath.b.e == 300
        assert soi.rootpath.b.f == 400

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_provides_a_batch_update_context(self, monkeypatch):
        """
        fl.util.Bureau containers provide a batched-updates context manager.

        """

        import fl.util

        soi = fl.util.Bureau()

        # ---------------------------------------------------------------------
        ts = '1234.5678'
        def _mock_time():
            """
            Mock for time.time()

            """
            return ts

        with monkeypatch.context() as patch:

            patch.setattr(time, 'time', _mock_time)

            with soi.batch_context() as batch:

                soi.a.c = 100
                soi.a.d = 200
                soi.b.e = 300
                soi.b.f = 400
                soi.b.f = 500
                soi.undo()
                soi.redo()

        tup_tup_batch = tuple(tuple(item) for item in batch)

        assert tup_tup_batch == (('edit', 0, ts, ('a', 'c'), 100, None ),
                                 ('edit', 1, ts, ('a', 'd'), 200, None ),
                                 ('edit', 2, ts, ('b', 'e'), 300, None ),
                                 ('edit', 3, ts, ('b', 'f'), 400, None ),
                                 ('edit', 4, ts, ('b', 'f'), 500, 400  ),
                                 ('undo', 5, ts, ('b', 'f'), 400, 500  ),
                                 ('redo', 6, ts, ('b', 'f'), 500, 400  ))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_be_updated_from_a_batch_record(self, monkeypatch):
        """
        fl.util.Bureau containers can be updated with batches of commands.

        """

        import fl.util

        batch = (('edit', 0, 0.0, ('a', 'c'), 100, None ),
                 ('edit', 1, 0.0, ('a', 'd'), 200, None ),
                 ('edit', 2, 0.0, ('b', 'e'), 300, None ),
                 ('edit', 3, 0.0, ('b', 'f'), 400, None ),
                 ('edit', 4, 0.0, ('b', 'f'), 500, 400  ),
                 ('undo', 5, 0.0, ('b', 'f'), 400, 500  ),
                 ('redo', 6, 0.0, ('b', 'f'), 500, 400  ))

        soi = fl.util.Bureau()
        soi.from_batch(batch)

        assert soi.a.c == 100
        assert soi.a.d == 200
        assert soi.b.e == 300
        assert soi.b.f == 500


# =============================================================================
# class SpecifyFlUtilApplyRules:
#     """
#     Spec for the fl.util.apply_rules function.

#     """

#     # -------------------------------------------------------------------------
#     @pytest.mark.e002_general_research
#     def it_can_modify_keys(self):
#         """
#         fl.util.apply_rules can modify keys.

#         """

#         import fl.util

#         Rule     = fl.util.Rule
#         item     = ('a', 'b')
#         tup_rule = (Rule(filter   = lambda it: it,
#                          function = lambda it: (it[0] + '_foo', it[1])),
#                     Rule(filter   = lambda it: it,
#                          function = lambda it: (it[0], it[1] + '_bar')))

#         result = fl.util.apply_rules(tup_rule = tup_rule,
#                                      item     = item)

#         assert result == ('a_foo', 'b_bar')


# =============================================================================
class SpecifyFlUtilSerialize:
    """
    Spec for the fl.util.serialize function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_pickle(self):
        """
        fl.util.serialize can serialize a dict to pickle

        """
        import fl.util
        map_input = dict(a = 1, b = 2)
        (bytes_output, map_error) = fl.util.serialize(map_input, 'pickle')

        assert map_error is None
        assert bytes_output == b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02u.'


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_xml(self):
        """
        fl.util.serialize can serialize a dict to xml

        """
        import fl.util
        map_input  = dict(a = dict(b = 1, c = 2, d = 3))
        (str_output, map_error) = fl.util.serialize(map_input, 'xml')

        assert map_error is None
        assert str_output == textwrap.dedent(
                                        """
                                        <?xml version="1.0" encoding="utf-8"?>
                                        <a>
                                          <b>1</b>
                                          <c>2</c>
                                          <d>3</d>
                                        </a>
                                        """).strip()

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_json(self):
        """
        fl.util.serialize can serialize a dict to json

        """
        import fl.util
        map_input  = dict(a = dict(b = 1, c = 2, d = 3))
        (str_output, map_error) = fl.util.serialize(map_input, 'json')

        assert str_output == textwrap.dedent(
                                        """
                                        {
                                          "a": {
                                            "b": 1,
                                            "c": 2,
                                            "d": 3
                                          }
                                        }
                                        """).strip()

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_toml(self):
        """
        fl.util.serialize can serialize a dict to toml

        """
        import fl.util
        map_input  = dict(a = dict(b = 1, c = 2, d = 3))
        (str_output, map_error) = fl.util.serialize(map_input, 'toml')

        assert str_output == textwrap.dedent(
                                        """
                                        [a]
                                        b = 1
                                        c = 2
                                        d = 3
                                        """).strip()

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_serialize_to_yaml(self):
        """
        fl.util.serialize can serialize a dict to yaml

        """
        import fl.util
        map_input  = dict(a_key = dict(a_long_key = 1, short = 2, tiny = 3))
        (str_output, map_error) = fl.util.serialize(map_input, 'yaml')

        assert str_output == textwrap.dedent(
                                        """
                                        a_key:
                                          a_long_key: 1
                                          short: 2
                                          tiny: 3
                                        """).strip()


# =============================================================================
class SpecifyFlUtilDeserialize:
    """
    Spec for the fl.util.deserialize function.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_pickle(self):
        """
        fl.util.deserialize can deserialize a dict from pickle bytes.

        Please note that XML does not inherently
        distinguish between different datatypes,
        and treats everything as text. This means
        that unless an application-specific type
        annotation mechanism is used, then all
        type information will be lost when using
        xml.

        """
        import fl.util
        bytes_input = b'\x80\x04\x95\x11\x00\x00\x00\x00\x00\x00\x00}\x94(\x8c\x01a\x94K\x01\x8c\x01b\x94K\x02u.'
        (map_output, map_error) = fl.util.deserialize(bytes_input, 'pickle')
        assert map_error is None
        assert map_output == dict(a = 1, b = 2)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_xml(self):
        """
        fl.util.deserialize can deserialize a dict from xml

        Please note that XML does not inherently
        distinguish between different datatypes,
        and treats everything as text. This means
        that unless an application-specific type
        annotation mechanism is used, then all
        type information will be lost when using
        xml.

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                <?xml version="1.0" encoding="utf-8"?>
                                <root>
                                  <a>1</a>
                                  <b>2.0</b>
                                  <c>Some string</c>
                                  <d>
                                    <e>345</e>
                                  </d>
                                </root>
                                """).strip()
        (map_output, map_error) = fl.util.deserialize(str_input, 'xml')
        assert map_error is None
        assert map_output == dict(a = 1,
                                  b = 2.0,
                                  c = 'Some string',
                                  d = dict(e = 345))


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_json(self):
        """
        fl.util.deserialize can deserialize a dict from json

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                {
                                  "a": 1,
                                  "b": 2.0,
                                  "c": "Some string",
                                  "d": {
                                    "e": 345
                                  }
                                }
                                """).strip()
        (map_output, map_error) = fl.util.deserialize(str_input, 'json')
        assert map_error is None
        assert map_output == dict(a = 1,
                                  b = 2.0,
                                  c = 'Some string',
                                  d = dict(e = 345))

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_toml(self):
        """
        fl.util.deserialize can deserialize a dict from toml

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                [a]
                                b = 1
                                c = 2
                                d = 3
                                """).strip()
        (map_output, map_error) = fl.util.deserialize(str_input, 'toml')
        assert map_error is None
        assert map_output == dict(a = dict(b = 1, c = 2, d = 3))


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_can_deserialize_from_yaml(self):
        """
        fl.util.deserialize can deserialize a dict from yaml

        """
        import fl.util
        str_input = textwrap.dedent(
                                """
                                a: 1
                                b: 2.0
                                c: "Some string"
                                d:
                                  e: 345
                                """).strip()
        (map_output, map_error) = fl.util.deserialize(str_input, 'yaml')
        assert map_error is None
        assert map_output == dict(a = 1,
                                  b = 2.0,
                                  c = 'Some string',
                                  d = dict(e = 345))
