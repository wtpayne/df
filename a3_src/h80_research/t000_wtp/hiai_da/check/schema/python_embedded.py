# -*- coding: utf-8 -*-
"""
Module for validation of embedded data structures in python files.

---
type:
    python_package

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


from good import (All,
                  Any,
                  Extra,
                  Optional,
                  Reject,
                  Required,
                  Schema)

import da.check.schema.common


# -----------------------------------------------------------------------------
def file_metadata_schema(idclass_tab):
    """
    Return the data validation schema for python file metadata.

    ---
    type:   function
    ...

    """
    python_file_type = Any('python_module',
                           'python_package')

    validation_level = All(idclass_tab['validation_level'],
                           Any('v00_minimum'))

    protection_level = All(idclass_tab['protection_level'],
                           Any('k00_public',
                               'k01_counterparty_confidential'))

    hiai_copyright = Schema(
        'Copyright 2019 High Integrity Artificial Intelligence Systems')

    hashdist_copyright = Schema(
        'Copyright 2012, Dag Sverre Seljebotn and Ondrej Certik')

    backported_lru_cache_copyright = Schema(
        'Copyright 2013 Raymond Hettinger')

    copyright_notice = Any(
        hiai_copyright,
        hashdist_copyright,
        backported_lru_cache_copyright)

    apache_license_v2 = Schema(
        'Licensed under the Apache License, Version 2.0 '
        '(the License); you may not use this file except in compliance '
        'with the License. You may obtain a copy of the License at\n'
        'http://www.apache.org/licenses/LICENSE-2.0\n'
        'Unless required by applicable law or agreed to in writing, '
        'software distributed under the License is distributed on an '
        'AS IS BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, '
        'either express or implied. See the License for the specific '
        'language governing permissions and limitations under the '
        'License.')

    bsd_3_clause_license = Schema(
        'Licensed under the BSD 3-clause license.\n'
        'Redistribution and use in source and binary forms, with or without '
        'modification, are permitted provided that the following conditions '
        'are met:\n'

        'Redistributions of source code must retain the above copyright '
        'notice, this list of conditions and the following disclaimer.\n'

        'Redistributions in binary form must reproduce the above '
        'copyright notice, this list of conditions and the following '
        'disclaimer in the documentation and/or other materials provided '
        'with the distribution.\n'

        'Neither the name of the copyright holders nor the names of '
        'other contributors may be used to endorse or promote products '
        'derived from this software without specific prior written '
        'permission.\n'

        'THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS '
        'AS IS AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT '
        'LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS '
        'FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE '
        'COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, '
        'INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, '
        'BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; '
        'LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER '
        'CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT '
        'LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN '
        'ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE '
        'POSSIBILITY OF SUCH DAMAGE.')

    mit_expat_license = Schema(
        'Licensed under the MIT Expat license:\n'

        'Permission is hereby granted, free of charge, to any person '
        'obtaining a copy of this software and associated documentation '
        'files, (the Software), to deal in the Software without '
        'restriction, including without limitation the rights to use, '
        'copy, modify, merge, publish, distribute, sublicense, and or '
        'sell copies of the Software, and to permit persons to whom '
        'the Software is furnished to do so, subject to the following '
        'conditions:\n'

        'The above copyright notice and this permission notice shall be '
        'included in all copies or substantial portions of the Software.\n'

        'THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND, '
        'EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES '
        'OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND '
        'NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT '
        'HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, '
        'WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING '
        'FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR '
        'OTHER DEALINGS IN THE SOFTWARE.')

    counterparty_confidential = Schema(
        'This document is not intended for redistribution. '
        'Counterparty confidentiality should be taken '
        'into consideration when handling this document. '
        'Nondisclosure agreements or other similar '
        'contractual obligations may be in force.')

    license_notice = Any(
        apache_license_v2,
        bsd_3_clause_license,
        mit_expat_license,
        counterparty_confidential)

    requirements_notice = Schema(
        'This design document may contain any number of requirements '
        'items embedded in comment blocks. Each requirements item '
        'that is present shall have one formal requirement statement '
        'with one modal verb. The modal verb shall be interpreted '
        'in accordance with iso29148:2011\n'
        'SHALL indicates a mandatory binding provision, the fulfillment '
        'of which must be proven through an appropriate test.\n'
        'WILL indicates a statement of fact; futurity; a declaration of '
        'purpose; or to establish a context or a limitation of use. These '
        'statements are not manadatory and not binding.\n'
        'SHOULD indicates a preference; a goal or an advantageous quality. '
        'These statements are not mandatory and not binding.\n'
        'MAY is used to grant permission or to make a suggestion. These '
        'statements are not mandatory and not binding.')

    return Schema({
        Required('type'):               python_file_type,
        Required('validation_level'):   validation_level,
        Required('protection'):         protection_level,
        Required('copyright'):          copyright_notice,
        Required('license'):            license_notice,
        Required('requirements'):       requirements_notice,
        Extra:                          Reject
    })


# -----------------------------------------------------------------------------
def function_metadata_schema():
    """
    Return the data validation schema for python function metadata.

    ---
    type:   function
    ...

    """
    key_value_pair = Schema({da.check.schema.common.LOWERCASE_NAME: str})
    function_type  = Any('constructor',
                         'context_manager',
                         'coroutine',
                         'function',
                         'method',
                         'generator')
    return Schema({
        'type':                     function_type,
        Optional('args'):           key_value_pair,
        Optional('yields'):         Any(key_value_pair, str),
        Optional('returns'):        Any(key_value_pair, str),
        Optional('preconditions'):  [str],
        Optional('side_effects'):   [str],
    })


# -----------------------------------------------------------------------------
def class_metadata_schema():
    """
    Return the data validation schema for python class metadata.

    ---
    type:   function
    ...

    """
    return Schema({
        'type':         'class',
        'attributes':   { da.check.schema.common.LOWERCASE_NAME: str }
    })


# -----------------------------------------------------------------------------
def file_scope_schema(idclass_tab):
    """
    Return the validation schema for data within python module scope.

    ---
    type:   function
    ...

    """
    return Schema(Any(

        Required(file_metadata_schema(idclass_tab)),

        Optional(da.check.schema.common.requirement_set_schema(idclass_tab))

    ))


# -----------------------------------------------------------------------------
def class_scope_schema(idclass_tab):
    """
    Return the validation schema for data within python class scope.

    ---
    type:   function
    ...

    """
    return Schema(Any(

        Required(class_metadata_schema()),

        Optional(da.check.schema.common.requirement_set_schema(idclass_tab))

    ))


# -----------------------------------------------------------------------------
def function_scope_schema(idclass_tab):
    """
    Return the validation schema for data within python function scope.

    ---
    type:   function
    ...

    """
    return Schema(Any(

        Required(function_metadata_schema()),

        Optional(da.check.schema.common.requirement_set_schema(idclass_tab))

    ))
