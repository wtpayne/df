# -*- coding: utf-8 -*-
"""
Module for design documentation generation.

module
    metadata
    class
        method
            design
            code
            abstract_syntax_tree
            control_flow_graph
            data_dependency_graph
            test_coverage
            blame

        method
    function
    function

---
type:
    python_package

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


import html
import os
import textwrap
import xml.etree.ElementTree

import baron
import baron.path
import baron.render
import baron.utils

import da.lwc
import da.lwc.file
import da.util
import da.python_source


TEMP_DELETEME = set()


# -----------------------------------------------------------------------------
def _split(text):
    """
    Return an iterator over the lines and line-endings in a piece of text.

    ---
    type:   function
    ...

    """
    return baron.utils.split_on_newlines(text)


# -----------------------------------------------------------------------------
def _is_newline(text):
    """
    Return true if text is a newline, false otherwise.

    ---
    type:   function
    ...

    """
    return baron.utils.is_newline(text)


# =============================================================================
class Walker(baron.render.RenderWalker):
    """
    Walk the AST building a HTML representation.

    """

    BLOCK_NODES = ('def', 'class')
    FLOW_NODES  = ('assignment',
                   'associative_parenthesis',
                   'atomtrailers',
                   'binary_operator',
                   'call',
                   'call_argument',
                   'comma',
                   'comment',
                   'comparison',
                   'comparison_operator',
                   'continue',
                   'decorator',
                   'def_argument',
                   'dict',
                   'dict_argument',
                   'dictitem',
                   'dot',
                   'dotted_as_name',
                   'dotted_name',
                   'elif',
                   'else',
                   'endl',
                   'for'
                   'getitem',
                   'if',
                   'ifelseblock',
                   'import',
                   'int',
                   'list',
                   'name',
                   'print',
                   'return',
                   'space',
                   'string',
                   'tuple',
                   'unitary_operator',
                   'while',
                   'with',
                   'with_context_item',
                   'yield_atom')

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Walker ctor.

        ---
        type:   constructor
        ...

        """
        super(Walker, self).__init__(strict=True)

        self.xml_root     = None
        self.xml_element  = None
        self.xml_path     = None
        self.fst_path     = None
        self.prev_element = None
        self.iline        = None

    # -------------------------------------------------------------------------
    def walk(self, tree):
        """
        Walk over the python FST tree building an XML tree.

        ---
        type: method
        ...

        """
        # Root of the XML tree
        #
        self.xml_root = xml.etree.ElementTree.Element('div')

        # Pointer to the current element in the tree.
        #
        self.xml_element = self.xml_root

        # Path from the root of the xml tree to the current element.
        #
        self.xml_path = [self.xml_root]

        # Path from the root of the FST tree to the current element.
        #
        self.fst_path = [(None, None, tree)]

        # Previous sibling in the current node or None.
        #
        self.prev_element = None

        # Current line order.
        # This relies on walk performing a depth-first
        # traversal so that line numbers increment
        # monotonically.
        #
        self.iline = 0

        super(Walker, self).walk(tree)
        return self

    # -------------------------------------------------------------------------
    def before(self, key_type, item, render_key):
        """
        Render starting tag and content before each FST node is visited.

        ---
        type: method

        args:
            self:
                An object of type Walker.
            key_type:
                "key_type is a string argument that
                indicates the type of the node and
                thus the data type of the item
                argument. It can take one of five
                values:- 'constant', 'node', 'key',
                'list', or 'formatting'. A 'constant'
                key_type indicates that item is a
                string. A 'node' key_type indicates
                that item is a dict. A 'key'
                key_type indicates that item is an
                element of a dict. A 'list' key_type
                indicates that item is a list, and
                a 'formatting' key_type indicates
                that the item is a list specialised
                in formatting."
            item:
                "The item argument represents a node
                in the FST. It can take the form of
                a string, a dict, or a list."
            render_key:
                "The render_key argument represents
                    the key used to access this child
                node from its parent. It is represented
                by a string if the parent node was
                a dict or by an integer if the
                parent node was a list."

        returns:
            None
        ...

        """
        is_dict     = key_type in ('node',   'key')
        is_string   = key_type in ('string', 'constant')
        # is_list     = key_type in ('list',)

        block_tag   = 'div'
        flow_tag    = 'span'

        if is_dict:
            # is_whitespace = fst_type in ('endl', 'space')
            fst_type = item['type']

            TEMP_DELETEME.add(fst_type)

            if fst_type in Walker.FLOW_NODES:
                self._add_child(flow_tag, **{
                    'class': html.escape(fst_type, quote = True)
                })
            if fst_type in Walker.BLOCK_NODES:
                self._add_child(block_tag, **{
                    'class': html.escape(fst_type, quote = True)
                })
        elif is_string:
            self._add_content(item)

        self.fst_path.append((key_type, render_key, item))
        super(Walker, self).before(key_type, item, render_key)

    # -------------------------------------------------------------------------
    def after(self, key_type, item, render_key):
        """
        Render ending tag after each FST node is visited.

        ---
        type: method

        args:
            self:
                An object of type Walker.
            key_type:
                "key_type is a string argument that
                indicates the type of the node and
                thus the data type of the item
                argument. It can take one of five
                values:- 'constant', 'node', 'key',
                'list', or 'formatting'. A 'constant'
                key_type indicates that item is a
                string. A 'node' key_type indicates
                that item is a dict. A 'key'
                key_type indicates that item is an
                element of a dict. A 'list' key_type
                indicates that item is a list, and
                a 'formatting' key_type indicates
                that the item is a list specialised
                in formatting."
            item:
                "The item argument represents a node
                in the FST. It can take the form of
                a string, a dict, or a list."
            render_key:
                "The render_key argument represents
                the key used to access this child
                node from its parent. It is represented
                by a string if the parent node was
                a dict or by an integer if the
                parent node was a list."

        returns:
            None
        ...

        """
        stop = super(Walker, self).after(key_type, item, render_key)
        self.fst_path.pop()
        if key_type in ('node', 'key'):
            if item['type'] in Walker.FLOW_NODES:
                self._pop_xml()
            if item['type'] in Walker.BLOCK_NODES:
                self._pop_xml()
        return stop

    # -------------------------------------------------------------------------
    def _pop_xml(self):
        """
        Pop the stack.

        ---
        type:   method
        ...

        """
        self.prev_element = self.xml_path.pop()
        self.xml_element  = self.xml_path[-1]

    # -------------------------------------------------------------------------
    def _add_sibling(self, tag, **attrib):
        """
        Create a sibling XML element.

        ---
        type:   method
        ...

        """
        self._pop_xml()
        self._add_child(tag, **attrib)

    # -------------------------------------------------------------------------
    def _add_child(self, tag, **attrib):
        """
        Create a child XML element.

        ---
        type:   method
        ...

        """
        self.xml_element = xml.etree.ElementTree.SubElement(
                                                        self.xml_element, tag)
        self.xml_path.append(self.xml_element)
        self.prev_element = None

        for (key, value) in attrib.items():
            self.xml_element.attrib[key] = value

    # -------------------------------------------------------------------------
    def _add_empty_child(self, tag, **attrib):
        """
        Add an empty (self-closing) XML element.

        ---
        type:   method
        ...

        """
        self._add_child(tag, **attrib)
        self._pop_xml()

    # -------------------------------------------------------------------------
    def _add_content(self, content):
        """
        Add content to the current XML element.

        Content is either added to the text field
        of the current element or to the tail field
        of the previous element.

        ---
        type:   method
        ...

        """
        for fragment in _split(content.replace(' ', '\u00A0')):

            if fragment is None:
                continue

            elif _is_newline(fragment):
                self.iline += 1
                self._add_empty_child('br')

            elif self.prev_element is not None:
                self._add_tail(fragment)

            else:
                self._add_text(fragment)

    # -------------------------------------------------------------------------
    def _add_tail(self, fragment):
        """
        Add a fragment of content to the tail field of the previous element.

        ---
        type:   method
        ...

        """
        if self.prev_element.tail is None:
            self.prev_element.tail = fragment
        else:
            self.prev_element.tail += fragment

    # -------------------------------------------------------------------------
    def _add_text(self, fragment):
        """
        Add a fragment of content to the text field of the current element.

        ---
        type:   method
        ...

        """
        if self.xml_element.text is None:
            self.xml_element.text = fragment
        else:
            self.xml_element.text += fragment


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(_):
    """
    Generate design docs for each build unit sent to this coroutine.

    ---
    type:   coroutine
    ...

    """
    # -------------------------------------------------------------------------
    def force_indent(num_space, text):
        """
        Return text with a specified number of spaces for indentation.

        ---
        type:   function
        ...

        """
        return textwrap.indent(textwrap.dedent(text), prefix = ' ' * num_space)

    css_style = force_indent(
        num_space = 8,
        text = """
        :root {

          /* Greys. */
          --black:            #000000;
          --black_tint:       #070707;
          --grey_shade_2:     #101010;
          --grey_shade_1:     #202020;
          --grey_shade_0:     #303030;
          --grey:             #606060;
          --grey_tint_0:      #C0C0C0;
          --white_shade:      #FAFAFA;
          --white:            #FFFFFF;

          /* Blues. */
          --blue_shade:       #303F9F;
          --blue:             #3F51B5;
          --blue_tint:        #C5CAE9;

          /* Oranges. */
          --orange:           #FF9800;

          --red_shade:        #9b2525;
          --green_shade:      #269b25;
          --blue_shade:       #26259b;
          --brown_shade:      #9b4c25;
          --pink_shade:       #9b256b;
          --purple_shade:     #77259b;
          --violet_shade:     #53259b;

          /* Brand palette */
          --brand_dark:       var(--blue_shade);
          --brand_mid:        var(--blue);
          --brand_light:      var(--blue_tint);
          --brand_accent:     var(--orange);

          /* Functional colours */
          --brand_id_0:       var(--red_shade);
          --brand_id_1:       var(--green_shade);
          --brand_id_2:       var(--blue_shade);
          --brand_id_3:       var(--brown_shade);
          --brand_id_4:       var(--pink_shade);
          --brand_id_5:       var(--purple_shade);
          --brand_id_6:       var(--violet_shade);

          /* Structural elements */
          --divider:          var(--light_grey);

          /* Text colours. (White or off-white bg) */
          --backgound:        var(--white_shade);
          --text_very_strong: var(--grey_shade_2);
          --text_strong:      var(--grey_shade_1);
          --text_mid:         var(--grey_shade_0);
          --text_weak:        var(--grey);
          --text_very_weak:   var(--grey_tint_0);

          /* Text colours. (Inverted) */
          --inv_backgound:    var(--brand_dark);
          --inv_very_strong:  var(--white);
          --inv_strong:       var(--white_shade);
          --inv_mid:          var(--grey_tint_0);
          --inv_weak:         var(--grey);
          --inv_very_weak:    var(--grey_shade_0);

        }

        html, body * {
            background-color: var(--backgound);
            border-bottom:    none;
            border:           none;
            color:            var(--text_mid);
            display:          inline;
            font-family:      monospace;
            font-size:        14px;
            font-style:       normal;
            font-weight:      normal;
            list-style-type:  none;
            margin:           0;
            padding:          0;
            text-align:       left;
            text-decoration:  none;
        }
        div.def {
            color: var(--brand_id_0);
            border-width: 1;
            border-color: var(--brand_id_0);
            background-color: var(--grey_tint_0);
        }
        div.class {
            color: var(--brand_id_1);
            border-width: 1;
            border-color: var(--brand_id_1);
            background-color: var(--grey_tint_0);
        }
        span {
            color: var(--text_very_weak);
        }""")

    html_template = textwrap.dedent(
        """
        <!DOCTYPE html>
        <html>
            <head><meta charset="UTF-8"></head>
            <style>{css_style}</style>
            <header></header>
        {html_body}
            <footer></footer>
        </html>
        """)

    while True:

        # Select only python build units.
        #
        build_unit = (yield)
        filepath   = build_unit['filepath']
        if not da.lwc.file.is_python_file(filepath):
            continue

        # Render HTML.
        #
        xml_tree  = Walker().walk(baron.parse(build_unit['content']))

        xml_text  = xml.etree.ElementTree.tostring(
                        xml_tree.xml_root, encoding = 'utf-8').decode('utf-8')
        html_text = html_template.format(css_style = css_style,
                                         html_body = xml_text)

        # Write to file.
        #
        dirpath_doc  = build_unit['dirpath_log']
        filename_doc = 'design.html'
        filepath_doc = os.path.join(dirpath_doc, filename_doc)
        os.makedirs(dirpath_doc, exist_ok = True)
        with open(filepath_doc, 'wt') as file_doc:
            file_doc.write(html_text)
