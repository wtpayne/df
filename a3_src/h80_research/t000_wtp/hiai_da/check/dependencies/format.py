# -*- coding: utf-8 -*-
"""
Functions to support dependencies register format validation.

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


import io
import json

import da.exception


# -----------------------------------------------------------------------------
def get_reference_text(register_data):
    """
    Return text formatted in a conforming manner to act as a reference.

    ---
    type:   function
    ...

    """
    json_doc = VerticallyAlignedJSON()
    json_doc >>= None
    json_doc = _add_register_header(json_doc, register_data)
    json_doc >>= 'register'
    for (name, entry) in sorted(register_data['register'].items()):
        json_doc += None
        json_doc >>= name
        json_doc = _add_register_entry(json_doc, entry)
        json_doc <<= name
    json_doc <<= 'register'
    json_doc <<= None
    return str(json_doc)


# -----------------------------------------------------------------------------
def _add_register_header(json_doc, register_data):
    """
    Add the dependencies register header information to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc += None
    json_doc += ('title',           register_data['title'])
    json_doc += None
    json_doc += ('introduction',    register_data['introduction'])
    json_doc += None
    return json_doc


# -----------------------------------------------------------------------------
def _add_register_entry(json_doc, entry):
    """
    Add a single dependencies registry entry to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc += ('desc',    entry['desc'])
    json_doc += ('notes',   entry['notes'])
    json_doc += ('labels',  entry['labels'])
    json_doc += ('dirname', entry['dirname'])
    json_doc += ('policy',  entry['policy'])
    json_doc = _add_api_section(    json_doc, entry)
    json_doc = _add_cli_section(    json_doc, entry)
    json_doc = _add_gui_section(    json_doc, entry)
    json_doc += ('tgt',     entry['tgt'])
    json_doc = _add_config_section( json_doc, entry)
    json_doc = _add_build_section(  json_doc, entry)

    return json_doc


# -----------------------------------------------------------------------------
def _add_api_section(json_doc, entry):
    """
    Add an API section to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc >>= 'api'
    for (api_name, api_path) in sorted(entry['api'].items()):
        json_doc += (api_name, api_path)
    json_doc <<= 'api'
    return json_doc


# -----------------------------------------------------------------------------
def _add_cli_section(json_doc, entry):
    """
    Add a CLI section to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc >>= 'cli'
    for (cli_name, cli_path) in sorted(entry['cli'].items()):
        json_doc += (cli_name, cli_path)
    json_doc <<= 'cli'
    return json_doc


# -----------------------------------------------------------------------------
def _add_gui_section(json_doc, entry):
    """
    Add a GUI section to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc >>= 'gui'
    for (gui_name, gui_path) in sorted(entry['gui'].items()):
        json_doc += (gui_name, gui_path)
    json_doc <<= 'gui'
    return json_doc


# -----------------------------------------------------------------------------
def _add_config_section(json_doc, entry):
    """
    Add a config section to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc >>= 'config'
    json_doc += ('method',  entry['config']['method'])
    json_doc += ('tool',    entry['config']['tool'])
    json_doc += ('url',     entry['config']['url'])
    json_doc <<= 'config'
    return json_doc


# -----------------------------------------------------------------------------
def _add_build_section(json_doc, entry):
    """
    Add a build section to the supplied JSON doc.

    ---
    type:   function
    ...

    """
    json_doc >>= 'build'
    json_doc += ('method',  entry['build']['method'])
    json_doc += ('tool',    entry['build']['tool'])
    json_doc <<= 'build'
    return json_doc


# =============================================================================
# disabled pylint rule R0903 - too-few-public-methods
# because this class mainly uses operator overloading
# rather than traditional methods. Probably not OK for
# safety critical stuff -- but fine for formatting
# configuration files as we are doing here. (IMHO).
#
class VerticallyAlignedJSON():                          # pylint: disable=R0903
    """
    Vertically aligned JSON serialisation.

    This class is used to feed my OCD by generating
    JSON format configuration files with content
    that is nicely vertically aligned for human
    comprehension.

    """

    # -------------------------------------------------------------------------
    def __init__(self,
                 indent_size = 4,
                 content_col = 32):
        """
        Return a newly constructed inprint.Doc class.

        ---
        type:   constructor
        ...

        """
        self.indent_size    = indent_size
        self.content_col    = content_col

        # The very first '{' in the file does not
        # need to be preceeded by a newline.
        #
        self.newline_needed = False

        # The brace character that opens a new
        # section does not need to be followed
        # by a comma, and neither does the last
        # item in the section.
        #
        self.comma_needed   = False
        self.stack          = []
        self.buffer         = io.StringIO()

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Return document content as a string.

        ---
        type:   method
        ...

        """
        self.buffer.write('\n')
        return self.buffer.getvalue()

    # -------------------------------------------------------------------------
    def __irshift__(self, name):
        """
        Add a new section to the document and return self.

        The operator >>= function adds a new section
        with the specified name to the document and
        increases the indentation level.

        The parameter on the RHS can be set to None
        to add an anonymous section.

        ---
        type:   method
        ...

        """
        if name is not None:
            self.buffer.write('{newline}{indent}"{name}": {{'.format(
                                                newline = self._get_newline(),
                                                indent  = self._get_indent(),
                                                name    = name))
        else:
            self.buffer.write('{newline}{indent}{{'.format(
                                                newline = self._get_newline(),
                                                indent  = self._get_indent()))
        self.stack.append(name)
        self.comma_needed = False
        return self

    # -------------------------------------------------------------------------
    def __ilshift__(self, name):
        """
        Set the end of the current section and return self.

        The operator <<= function ends the current
        section and reduces the indentation level.

        If the parameter on the RHS of the operator
        is not None, then it is compared with the
        current section and an exception raised in
        the case of a mismatch.

        ---
        type:   method
        ...

        """
        prev = self.stack.pop()
        self.comma_needed = False
        self.buffer.write('{newline}{indent}}}'.format(
                                            newline = self._get_newline(),
                                            indent  = self._get_indent()))
        self.comma_needed = True
        if name is not None:
            assert prev == name
        return self

    # -------------------------------------------------------------------------
    def __iadd__(self, item):
        """
        Add an item to the document and return self.

        The operator += function adds the specified
        item to the document.

        ---
        type:   method
        ...

        """
        if item is None:
            self.buffer.write('{newline}'.format(
                                            newline = self._get_newline()))
            self.comma_needed = False
        else:
            assert len(item) == 2
            self._add_key_value_pair(key   = item[0],
                                     value = item[1])
            self.comma_needed = True
        return self

    # -------------------------------------------------------------------------
    def _add_key_value_pair(self, key, value):
        """
        Add a key-value pair to the document.

        ---
        type:   method
        ...

        """
        assert len(self.stack) > 0
        assert isinstance(key, str)

        key = '{indent}"{key}": '.format(
                                    indent  = self._get_indent(),
                                    key     = key)
        tab = self.content_col - len(key)
        if tab > 0:
            key += (' ' * tab)

        # Handle short list. E.g. list of tags.
        #
        if isinstance(value, list):
            self.buffer.write('{newline}{key}{value}'.format(
                                                newline = self._get_newline(),
                                                key     = key,
                                                value   = json.dumps(value)))

        elif isinstance(value, str):
            self.buffer.write('{newline}{key}"{value}"'.format(
                                                newline = self._get_newline(),
                                                key     = key,
                                                value   = value))

        elif isinstance(value, dict):
            self.buffer.write('{newline}{key}{value}'.format(
                                                newline = self._get_newline(),
                                                key     = key,
                                                value   = json.dumps(value)))

        else:
            raise da.exception.ImplementationNotPresentError(
                                  "No serialisation for specified data type.")

    # -------------------------------------------------------------------------
    def _get_newline(self):
        """
        Return an appropriate line termination and newline as a string.

        ---
        type:   method
        ...

        """
        # The very first '{' in the file does not
        # need to be preceeded by a newline.
        #
        if not self.newline_needed:
            self.newline_needed = True
            return ''
        if self.comma_needed:
            return ',\n'
        else:
            return '\n'

    # -------------------------------------------------------------------------
    def _get_indent(self):
        """
        Return the current top-level indent as a string.

        ---
        type:   method
        ...

        """
        num_indents = len(self.stack)
        num_spaces  = num_indents * self.indent_size
        indent      = ' ' * num_spaces
        return indent
