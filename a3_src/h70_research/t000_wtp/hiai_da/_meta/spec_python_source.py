# -*- coding: utf-8 -*-
"""
Unit tests for the python_source module.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2019 High Integrity Artificial Intelligence Systems"

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


import ast
import io
import textwrap

import pytest


# =============================================================================
class SpecifyGenTopLevelClassNames:
    """
    Specify the da.python_source.gen_top_level_class_names() function.

    """

    # -------------------------------------------------------------------------
    def it_yields_class_names(self):
        """
        The gen_top_level_class_names() function yields class names.

        """
        import da.python_source

        test_vector = ast.parse(textwrap.dedent('''
                            class FirstClass:
                                def first_method_in_first_class():
                                    pass
                                def second_method_in_first_class():
                                    pass
                            class SecondClass:
                                def first_method_in_second_class():
                                    pass
                                def second_method_in_second_class():
                                    pass
                            class ThirdClass:
                                def first_method_in_third_class():
                                    pass
                                def second_method_in_third_class():
                                    pass
                            '''))

        coroutine = da.python_source.gen_top_level_class_names(test_vector)
        assert next(coroutine) == 'FirstClass'
        assert next(coroutine) == 'SecondClass'
        assert next(coroutine) == 'ThirdClass'
        with pytest.raises(StopIteration):
            next(coroutine)

    # -------------------------------------------------------------------------
    def it_does_not_yield_inner_class_names(self):
        """
        gen_top_level_class_names() does not yield inner class names.

        """
        import da.python_source

        test_vector = ast.parse(textwrap.dedent('''
                            class FirstClass:
                                def first_method_in_first_class():
                                    pass
                                def second_method_in_first_class():
                                    pass
                                class SecondClass:
                                    def first_method_in_second_class():
                                        pass
                                    def second_method_in_second_class():
                                        pass
                            class ThirdClass:
                                def first_method_in_third_class():
                                    pass
                                def second_method_in_third_class():
                                    pass
                            '''))

        coroutine = da.python_source.gen_top_level_class_names(test_vector)
        assert next(coroutine) == 'FirstClass'
        assert next(coroutine) == 'ThirdClass'
        with pytest.raises(StopIteration):
            next(coroutine)

    # -------------------------------------------------------------------------
    def it_does_not_yield_when_no_classes_are_present(self):
        """
        gen_top_level_class_names() does not yield inner class names.

        """
        import da.python_source

        test_vector = ast.parse(textwrap.dedent('''
                            def first_function():
                                pass
                            def second_function():
                                pass
                            '''))

        coroutine = da.python_source.gen_top_level_class_names(test_vector)
        with pytest.raises(StopIteration):
            next(coroutine)

    # -------------------------------------------------------------------------
    def it_does_not_yield_when_only_inner_classes_are_present(self):
        """
        gen_top_level_class_names() does not yield inner class names.

        """
        import da.python_source

        test_vector = ast.parse(textwrap.dedent('''
                            def first_function():
                                class FirstClass:
                                    def first_method_in_first_class():
                                        pass
                                    def second_method_in_first_class():
                                        pass
                            def second_function():
                                pass
                            '''))

        coroutine = da.python_source.gen_top_level_class_names(test_vector)
        with pytest.raises(StopIteration):
            next(coroutine)


# =============================================================================
class SpecifyGenTopLevelFunctionNames:
    """
    Specify the da.python_source.gen_top_level_function_names() function.

    """

    # -------------------------------------------------------------------------
    def it_yields_function_names(self):
        """
        The gen_top_level_function_names() function yields function names.

        """
        import da.python_source

        test_vector = ast.parse(textwrap.dedent('''
                            def first_function():
                                pass
                            def second_function():
                                pass
                            def third_function():
                                pass
                            '''))

        coroutine = da.python_source.gen_top_level_function_names(test_vector)
        assert next(coroutine) == 'first_function'
        assert next(coroutine) == 'second_function'
        assert next(coroutine) == 'third_function'
        with pytest.raises(StopIteration):
            next(coroutine)


# =============================================================================
class SpecifyGenTopLevelMethodNames:
    """
    Specify the da.python_source.gen_top_level_method_names() function.

    """

    # -------------------------------------------------------------------------
    def it_yields_method_names(self):
        """
        The gen_top_level_method_names() function yields method names.

        """
        import da.python_source

        test_vector = ast.parse(textwrap.dedent('''
                            class FirstClass:
                                def first_method_in_first_class():
                                    pass
                                def second_method_in_first_class():
                                    pass
                            class SecondClass:
                                def first_method_in_second_class():
                                    pass
                                def second_method_in_second_class():
                                    pass
                            class ThirdClass:
                                def first_method_in_third_class():
                                    pass
                                def second_method_in_third_class():
                                    pass
                            '''))

        coroutine = da.python_source.gen_top_level_method_names(test_vector)
        assert next(coroutine) == 'FirstClass.first_method_in_first_class'
        assert next(coroutine) == 'FirstClass.second_method_in_first_class'
        assert next(coroutine) == 'SecondClass.first_method_in_second_class'
        assert next(coroutine) == 'SecondClass.second_method_in_second_class'
        assert next(coroutine) == 'ThirdClass.first_method_in_third_class'
        assert next(coroutine) == 'ThirdClass.second_method_in_third_class'
        with pytest.raises(StopIteration):
            next(coroutine)


# =============================================================================
class SpecifyIterEmbeddedData:
    """
    Specify the iter_embedded_data() function.

    """

    # -------------------------------------------------------------------------
    def _fixture(self, test_vector):
        """
        Text fixture to run iter_embedded_data on the specified source text.

        """
        import da.python_source
        encoded_input = io.BytesIO(textwrap.dedent(test_vector).encode())
        root          = ast.parse(encoded_input.read())
        iter_out      = da.python_source.iter_embedded_data(
                                                'mod', root, encoded_input)
        return [(embed.dat, embed.meta.path) for embed in iter_out]

    # -------------------------------------------------------------------------
    def it_yields_module_level_docstring_data(self):
        """
        It yields data encoded as yaml in module level docstrings.

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      '''
        assert self._fixture(test_vector) == [
                        ({'key':  'value'},  'mod')]

    # -------------------------------------------------------------------------
    def it_yields_module_level_comment_data(self):
        """
        It yields data encoded as yaml in module level comments.

        """
        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      '''
        assert self._fixture(test_vector) == [
                        ({'key': 'value'}, 'mod')]

    # -------------------------------------------------------------------------
    def it_yields_data_from_comments_preceeding_a_function(self):
        """
        It yields data encoded in doxygen style comments preceeding a function.

        """
        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      def test_func():
                          pass
                      '''
        assert self._fixture(test_vector) == [
                        ({'key': 'value'}, 'mod.test_func')]

    # -------------------------------------------------------------------------
    def it_yields_data_from_preceeding_comments_and_docstrings(self):
        """
        It yields data encoded both before and after the function def.

        """
        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      def test_func():
                          """
                          ---
                          key2: value2
                          ...
                          """
                          pass
                      '''
        assert self._fixture(test_vector) == [
                        ({'key':  'value'},  'mod.test_func'),
                        ({'key2': 'value2'}, 'mod.test_func')]

    # -------------------------------------------------------------------------
    def it_distinguishes_between_module_and_function_level_data(self):
        """
        It distinguishes between module level and function level data.

        The module docstring is correctly associated
        with the module and both the doxygen style
        comment that preceeds the function def and
        the docstring that follows the function def
        are correctly associated with the function.

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      def test_func():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          pass
                      '''
        assert self._fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_func'),
                        ({'key3': 'value3'}, 'mod.test_func')]

    # -------------------------------------------------------------------------
    def it_yields_data_in_inner_function_docstrings(self):
        """
        It yields data embedded in inner/nested function docstrings.

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      def test_func():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          def inner_func():
                              """
                              ---
                              key4: value4
                              ...
                              """
                              pass
                      '''
        assert self._fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_func'),
                        ({'key3': 'value3'}, 'mod.test_func'),
                        ({'key4': 'value4'}, 'mod.test_func.inner_func')]

    # -------------------------------------------------------------------------
    def it_yields_data_from_comments_preceeding_an_inner_function(self):
        """
        It yields data from comments preceeding an inner function.

        The module docstring is correctly associated
        with the module. The doxygen style comment
        that preceeds the top level function def is
        correctly associated with the top level
        function def. The docstring that follows
        the top level function def is correctly
        associated with the top level function def.
        The doxygen style comment that preceeds the
        inner function def is correctly associated
        with the inner function def. The docstring
        that follows the inner function def is
        correctly associated with the inner function
        def.

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      def test_func():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          # ---
                          # key4: value4
                          # ...
                          def inner_func():
                              """
                              ---
                              key5: value5
                              ...
                              """
                              pass
                      '''
        assert self._fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_func'),
                        ({'key3': 'value3'}, 'mod.test_func'),
                        ({'key4': 'value4'}, 'mod.test_func.inner_func'),
                        ({'key5': 'value5'}, 'mod.test_func.inner_func')]

    # -------------------------------------------------------------------------
    def it_yields_data_from_classes_and_methods(self):
        """
        It yields data from classes and methods

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      class test_class():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          # ---
                          # key4: value4
                          # ...
                          def test_method():
                              """
                              ---
                              key5: value5
                              ...
                              """
                              pass
                      '''
        assert self._fixture(test_vector) == [
                        ({'key':  'value'},  'mod'),
                        ({'key2': 'value2'}, 'mod.test_class'),
                        ({'key3': 'value3'}, 'mod.test_class'),
                        ({'key4': 'value4'}, 'mod.test_class.test_method'),
                        ({'key5': 'value5'}, 'mod.test_class.test_method')]

    # -------------------------------------------------------------------------
    def it_yields_data_from_inner_classes_and_methods(self):
        """
        It yields data from inner classes and methods

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      class class1():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          # ---
                          # key4: value4
                          # ...
                          def method1():
                              """
                              ---
                              key5: value5
                              ...
                              """
                          # ---
                          # key6: value6
                          # ...
                          class class2():
                              """
                              ---
                              key7: value7
                              ...
                              """
                              # ---
                              # key8: value8
                              # ...
                              def method2():
                                  """
                                  ---
                                  key9: value9
                                  ...
                                  """
                                  pass
                      '''
        assert self._fixture(test_vector) == [
                    ({'key':  'value'},  'mod'),
                    ({'key2': 'value2'}, 'mod.class1'),
                    ({'key3': 'value3'}, 'mod.class1'),
                    ({'key4': 'value4'}, 'mod.class1.method1'),
                    ({'key5': 'value5'}, 'mod.class1.method1'),
                    ({'key6': 'value6'}, 'mod.class1.class2'),
                    ({'key7': 'value7'}, 'mod.class1.class2'),
                    ({'key8': 'value8'}, 'mod.class1.class2.method2'),
                    ({'key9': 'value9'}, 'mod.class1.class2.method2')]

    # -------------------------------------------------------------------------
    def it_yields_data_from_classes_inside_methods(self):
        """
        It yields data from inner classes defined inside a method.

        """
        test_vector = '''
                      """
                      ---
                      key: value
                      ...
                      """
                      # ---
                      # key2: value2
                      # ...
                      class class1():
                          """
                          ---
                          key3: value3
                          ...
                          """
                          # ---
                          # key4: value4
                          # ...
                          def method1():
                              """
                              ---
                              key5: value5
                              ...
                              """
                              # ---
                              # key6: value6
                              # ...
                              class class2():
                                  """
                                  ---
                                  key7: value7
                                  ...
                                  """
                                  # ---
                                  # key8: value8
                                  # ...
                                  def method2():
                                      """
                                      ---
                                      key9: value9
                                      ...
                                      """
                                      pass
                      '''
        assert self._fixture(test_vector) == [
                    ({'key':  'value'},  'mod'),
                    ({'key2': 'value2'}, 'mod.class1'),
                    ({'key3': 'value3'}, 'mod.class1'),
                    ({'key4': 'value4'}, 'mod.class1.method1'),
                    ({'key5': 'value5'}, 'mod.class1.method1'),
                    ({'key6': 'value6'}, 'mod.class1.method1.class2'),
                    ({'key7': 'value7'}, 'mod.class1.method1.class2'),
                    ({'key8': 'value8'}, 'mod.class1.method1.class2.method2'),
                    ({'key9': 'value9'}, 'mod.class1.method1.class2.method2')]

    # -------------------------------------------------------------------------
    def it_yields_complex_hierarchical_data_structures(self):
        """
        It yields data containing complex hierarchical data structures.

        """
        test_vector = '''
                      def test_func():
                          # ---
                          # key1:
                          #     key2:
                          #         key3: value
                          # ...
                          pass
                      '''
        assert self._fixture(test_vector) == [
                    ({'key1': {'key2': {'key3': 'value'}}}, 'mod.test_func')]


# =============================================================================
class SpecifyGenFunctionsAndMethods:
    """
    Specify the da.python_source.gen_functions_and_methods() function.

    """

    # -------------------------------------------------------------------------
    def it_yields_all_functions_and_methods(self):
        """
        It yields all functions and methods in the file.

        Including nested functions and methods in nested classes.

        """
        import da.python_source

        test_text = textwrap.dedent('''
                            """
                            ---
                            key1: value1
                            ...
                            """
                            # ---
                            # key2: value2
                            # ...
                            def func1():
                                """
                                ---
                                key3: value3
                                ...
                                """
                                pass
                                # ---
                                # key4: value4
                                # ...
                                def func2():
                                    """
                                    ---
                                    key5: value5
                                    ...
                                    """
                                    pass
                                # ---
                                # key6: value6
                                # ...
                                class class1():
                                    """
                                    ---
                                    key7: value7
                                    ...
                                    """
                                    # ---
                                    # key8: value8
                                    # ...
                                    def method1():
                                        """
                                        ---
                                        key9: value9
                                        ...
                                        """
                                        # ---
                                        # key10: value10
                                        # ...
                                        class class2():
                                            """
                                            ---
                                            key11: value11
                                            ...
                                            """
                                            # ---
                                            # key12: value12
                                            # ...
                                            def method2():
                                                """
                                                ---
                                                key13: value13
                                                ...
                                                """
                                                pass
                            ''')
        test_ast  = ast.parse(test_text)
        coroutine = da.python_source.gen_functions_and_methods(
                                                    module_name = 'mod',
                                                    source_text = test_text,
                                                    root_node   = test_ast)
        first = next(coroutine)
        assert first.name == 'func1'

        second = next(coroutine)
        assert second.name == 'func2'

        third = next(coroutine)
        assert third.name == 'method1'
        assert textwrap.dedent(third.da_text) == textwrap.dedent(
                            '''
                            def method1():
                                """
                                ---
                                key9: value9
                                ...
                                """
                                # ---
                                # key10: value10
                                # ...
                                class class2():
                                    """
                                    ---
                                    key11: value11
                                    ...
                                    """
                                    # ---
                                    # key12: value12
                                    # ...
                                    def method2():
                                        """
                                        ---
                                        key13: value13
                                        ...
                                        """
                                        pass
                            ''').strip()

        fourth = next(coroutine)
        assert fourth.name == 'method2'
        assert textwrap.dedent(fourth.da_text) == textwrap.dedent(
                            '''
                            def method2():
                                """
                                ---
                                key13: value13
                                ...
                                """
                                pass
                            ''').strip()

        with pytest.raises(StopIteration):
            next(coroutine)


# =============================================================================
class SpecifyGenAstPathsDepthFirst:
    """
    Specify the da.python_source.gen_ast_paths_depth_first() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The gen_ast_paths_depth_first() function is callable.

        """
        import da.python_source
        test_vector = ast.parse(textwrap.dedent('''
                            """
                            ---
                            key1: value1
                            ...
                            """
                            # ---
                            # key2: value2
                            # ...
                            def func1():
                                """
                                ---
                                key3: value3
                                ...
                                """
                                pass
                                # ---
                                # key4: value4
                                # ...
                                def func2():
                                    """
                                    ---
                                    key5: value5
                                    ...
                                    """
                                    pass
                                # ---
                                # key6: value6
                                # ...
                                class class1():
                                    """
                                    ---
                                    key7: value7
                                    ...
                                    """
                                    # ---
                                    # key8: value8
                                    # ...
                                    def method1():
                                        """
                                        ---
                                        key9: value9
                                        ...
                                        """
                                        # ---
                                        # key10: value10
                                        # ...
                                        class class2():
                                            """
                                            ---
                                            key11: value11
                                            ...
                                            """
                                            # ---
                                            # key12: value12
                                            # ...
                                            def method2():
                                                """
                                                ---
                                                key13: value13
                                                ...
                                                """
                                                pass
                            '''))
        coroutine = da.python_source.gen_ast_paths_depth_first(
                                                        root = test_vector,
                                                        module_name = 'mod')
        first   = next(coroutine)
        assert first[-1].da_addr == 'mod'

        second  = next(coroutine)
        assert second[-1].da_addr == 'mod.func1'

        third   = next(coroutine)
        assert third[-1].da_addr == 'mod.func1.func2'

        fourth  = next(coroutine)
        assert fourth[-1].da_addr == 'mod.func1.class1'

        fifth   = next(coroutine)
        assert fifth[-1].da_addr == 'mod.func1.class1.method1'

        sixth   = next(coroutine)
        assert sixth[-1].da_addr == 'mod.func1.class1.method1.class2'

        seventh = next(coroutine)
        assert seventh[-1].da_addr == 'mod.func1.class1.method1.class2.method2'

        with pytest.raises(StopIteration):
            next(coroutine)

# =============================================================================
class SpecifyGetModuleName:
    """
    Specify the da.python_source.get_module_name() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The get_module_name() function is callable.

        """
        import da.python_source
        assert callable(da.python_source.get_module_name)


# =============================================================================
class Specify_GenCommentAndDocstrToks:
    """
    Specify the _gen_comment_and_docstr_toks() function.

    """

    # -------------------------------------------------------------------------
    def it_can_extract_a_single_line_comment(self):
        """
        A single line comment is extracted from the input stream.

        ---
        i00047_extract_comments_from_python_files:
          - "The system SHALL extract comment text from files conforming to
            the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      # One comment
                      def a_function:
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            [' One comment']

    # -------------------------------------------------------------------------
    def it_can_extract_a_function_docstring(self):
        """
        A function docstring is extracted from the input stream.

        ---
        i00048_extract_function_docstrings_from_python_files:
          - "The system SHALL extract function level docstring text from
            files conforming to the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      def a_function:
                          """
                          One function level docstring
                          """
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            ['One function level docstring']

    # -------------------------------------------------------------------------
    def it_can_extract_a_class_docstrings(self):
        """
        A class docstring is extracted from the input stream.

        ---
        i00049_extract_class_docstrings_from_python_files:
          - "The system SHALL extract class level docstring text from
            files conforming to the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      class a_class:
                          """
                          One class level docstring
                          """
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            ['One class level docstring']

    # -------------------------------------------------------------------------
    def it_can_extract_a_module_docstring(self):
        """
        A module docstring is extracted from the input stream.

        ---
        i00050_extract_module_docstrings_from_python_files:
          - "The system SHALL extract module level docstring text from
            files conforming to the Python 3 language syntax specification."
          - type: mandate
          - state: draft
        ...
        """
        test_vector = '''
                      """
                      One module level docstring
                      """
                      def a_function:
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            ['One module level docstring']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_followed_by_a_single_line_comment(self):
        """
        A function docstring followed by a single line comment is extracted.

        """
        test_vector = '''
                      def a_function:
                          """
                          One function level docstring
                          """
                          # And one comment
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            ['One function level docstring',
                             ' And one comment']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_followed_by_a_multiline_comment(self):
        """
        A function docstring followed by a multi line comment is extracted.

        """
        test_vector = '''
                      def a_function:
                          """
                          One function level docstring
                          """
                          # And one comment
                          # Over multiple lines
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            ['One function level docstring',
                             ' And one comment',
                             ' Over multiple lines']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_between_comments(self):
        """
        A function docstring between two single line comments is extracted.

        """
        test_vector = '''
                      # A Comment
                      def a_function:
                          """
                          A Docstring
                          on multiple lines
                          """
                          # And another comment after.
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            [' A Comment',
                             'A Docstring\non multiple lines',
                             ' And another comment after.']

    # -------------------------------------------------------------------------
    def it_can_extract_a_docstring_but_ignore_a_string_literal(self):
        """
        A function docstring is extracted but a string literal is ignored.

        """
        test_vector = '''
                      def a_function:
                          """
                          One docstring
                          """
                          x = """And one string literal"""
                          pass
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            ['One docstring']


    # -------------------------------------------------------------------------
    def it_can_extract_a_multiline_comment_containing_yaml(self):
        """
        A multiline comment containing some yaml is extracted.

        """
        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      '''
        assert self._get_list_of_tokens_from_text(test_vector) == \
                            [' ---',
                             ' key: value',
                             ' ...']

    # -------------------------------------------------------------------------
    def _get_list_of_tokens_from_text(self, text_content):
        """
        Test fixture. Return a list of tokens parsed from the provided text.

        """
        import da.python_source
        bytes_content = io.BytesIO(textwrap.dedent(text_content).encode())
        token_list    = list()
        for token in da.python_source._gen_comment_and_docstr_toks(
                                                                bytes_content):
            token_list.append(token.txt)
        return token_list


# =============================================================================
class Specify_MergeCommentBlocks:
    """
    Specify the _merge_comment_blocks() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the _merge_comment_blocks function.

        """
        import da.python_source
        _gen_tok = da.python_source._gen_comment_and_docstr_toks
        _merge   = da.python_source._merge_comment_blocks

        def _testitem(raw):
            return _merge(_gen_tok(_to_file(raw)))

        def _to_file(raw):
            return io.BytesIO(textwrap.dedent(raw).encode())

        def _fixture(raw):
            return [blk.txt for blk in _testitem(raw)]

        test_vector = '''
                      # Comment 1.
                      # Comment 2.
                      '''
        assert _fixture(test_vector) == [' Comment 1.\n Comment 2.']

        test_vector = '''
                      # Comment 1.
                      this_is_a_gap = 1
                      # Comment 2.
                      '''
        assert _fixture(test_vector) == [' Comment 1.',
                                         ' Comment 2.']

        test_vector = '''
                      # Comment 1.
                      # Comment 2.
                      this_is_a_gap = 1
                      # Comment 3.
                      '''
        assert _fixture(test_vector) == [' Comment 1.\n Comment 2.',
                                         ' Comment 3.']

        test_vector = '''
                      # ---
                      # key: value
                      # ...
                      '''
        assert _fixture(test_vector) == [' ---\n key: value\n ...']


# =============================================================================
class Specify_GenEmbeddedData:
    """
    Specify the _gen_embedded_data() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the _gen_embedded_data_in_file function.

        """
        import da.python_source
        _gen_data   = da.python_source._gen_embedded_data_in_file

        def _testitem(raw):
            return _gen_data(_to_file(raw))

        def _to_file(raw):
            return io.BytesIO(textwrap.dedent(raw).encode())

        def _fixture(raw):
            return [yaml.dat for yaml in _testitem(raw)]

        test_vector = '''
                      # ---
                      # a_key: "A Value"
                      # ...
                      '''
        assert _fixture(test_vector) == [{'a_key': 'A Value'}]


# =============================================================================
class Specify_IterWindowedPairs:
    """
    Specify the _iter_windowed_pairs() function.

    """

    # -------------------------------------------------------------------------
    def it_does_marvellous_things(self):
        """
        Test basic use cases for the _iter_windowed_pairs function.

        """
        import da.python_source

        def _fixture(test_vector):
            return list(da.python_source._iter_windowed_pairs(test_vector))

        test_vector = []
        assert _fixture(test_vector) == [(None, None)]

        test_vector = ['A']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', None)]

        test_vector = ['A', 'B']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', 'B'),
                                         ('B', None)]

        test_vector = ['A', 'B', 'C']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', 'B'),
                                         ('B', 'C'),
                                         ('C', None)]

        test_vector = ['A', 'B', 'C', 'D']
        assert _fixture(test_vector) == [(None, 'A'),
                                         ('A', 'B'),
                                         ('B', 'C'),
                                         ('C', 'D'),
                                         ('D', None)]


# =============================================================================
class Specify_IndentLevel:
    """
    Specify the da.python_source._indent_level() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _indent_level() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._indent_level)


# =============================================================================
class Specify_HasName:
    """
    Specify the da.python_source._has_name() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _has_name() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._has_name)


# =============================================================================
class Specify_HasBody:
    """
    Specify the da.python_source._has_body() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _has_body() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._has_body)


# =============================================================================
class Specify_IterChildrenWithBodies:
    """
    Specify the da.python_source._iter_children_with_bodies() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _iter_children_with_bodies() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._iter_children_with_bodies)


# =============================================================================
class Specify_LastLineIn:
    """
    Specify the da.python_source._last_line_in() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _last_line_in() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._last_line_in)


# =============================================================================
class Specify_GenEmbeddedDataInFile:
    """
    Specify the da.python_source._gen_embedded_data_in_file() function.

    """

    # -------------------------------------------------------------------------
    def it_is_callable(self):
        """
        The _gen_embedded_data_in_file() function is callable.

        """
        import da.python_source
        assert callable(da.python_source._gen_embedded_data_in_file)
