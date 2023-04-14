# -*- coding: utf-8 -*-
"""
Module for the generation of docx format documents.

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

import jinja2


# -----------------------------------------------------------------------------
def build(_, section_list, filepath):
    """
    Build and save the specified document.

    ---
    type:   function
    ...

    """
    environment = jinja2.Environment(
                    loader        = jinja2.PackageLoader(
                                                    'da.report', '_template'),
                    trim_blocks   = True,
                    lstrip_blocks = True)
    template = environment.get_template('engineering_document.template.html')

    # Filter out empty sections
    filtered_list = []
    for section in section_list:

        if section['level'] != 1 and len(section['para']) == 0:
            continue
        filtered_list.append(section)

    html = template.render(                             # pylint: disable=E1101
                    section_list = filtered_list)

    with open(filepath, 'wt') as file:
        file.write(html)

#     _add_title_section(document, doc_data['_metadata'])
#     _add_toc_section(document)
#     for item in sorted(_generate_content_items(doc_data),
#                        key = _doc_data_sortkey):

#         if item['section_level'] == 1:
#             _add_content_section(document)

#         if 0 < len(item['paragraph_list']):
#             _add_content_para(document,
#                               level   = item['section_level'],
#                               title   = item['section_title'],
#                               type    = item['section_type'],
#                               content = item['paragraph_list'])
#         else:
#             print('Skipping section: ' + item['section_title'])

#     # Save the document.
#     da.util.ensure_dir_exists(os.path.dirname(filepath))
#     document.save(filepath)
