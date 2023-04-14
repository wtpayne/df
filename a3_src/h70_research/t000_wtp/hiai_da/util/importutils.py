# -*- coding: utf-8 -*-
"""
Module import utility functions.

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


import importlib
import os
import sys


# -----------------------------------------------------------------------------
def import_fcn(module_dot_fcn):
    """
    Import the specified function.

    ---
    type:   function
    ...

    """
    (module_name, function_name) = module_dot_fcn.rsplit(".", 1)
    module   = importlib.import_module(module_name)
    function = getattr(module, function_name)
    return function


# -----------------------------------------------------------------------------
def import_module_file(filepath):
    """
    Import the specified module.

    ---
    type:   function
    ...

    """
    filename  = os.path.basename(filepath)
    (name, _) = os.path.splitext(filename)
    loader    = importlib.machinery.SourceFileLoader(name, filepath)
    module    = loader.load_module()
    return module


# -----------------------------------------------------------------------------
def import_from_dir(dirpath, module_name):
    """
    Import a module from a specified_directory.

    ---
    type:   function
    ...

    """
    if dirpath in sys.path:
        module = importlib.__import__(module_name)
    else:
        sys.path.insert(0, dirpath)
        try:
            module = importlib.__import__(module_name)
        finally:
            del sys.path[0]
    return module
