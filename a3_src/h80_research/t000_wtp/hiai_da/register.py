# -*- coding: utf-8 -*-
"""
Item register functions.

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


import functools
import os

import da.lwc.discover

try:
    from functools import lru_cache
except ImportError:
    # Python 2 does not have an lru_cache, so
    # during da bootstrap we need to provide an
    # alternate implementation.
    #
    from da.memo import lru_cache  # type: ignore


# -----------------------------------------------------------------------------
@lru_cache(maxsize = 8)
def load(register_name, dirpath_lwc_root = None):
    """
    Return data read from the specified register.

    ---
    type:   function
    ...

    """
    dirpath_registry  = da.lwc.discover.path(
                                        key              = 'registry',
                                        dirpath_lwc_root = dirpath_lwc_root)

    # Try to load YAML file.
    #
    filename_yaml = '{name}.register.yaml'.format(name = register_name)
    filepath_yaml = os.path.join(dirpath_registry, filename_yaml)
    if os.path.isfile(filepath_yaml):
        import yaml
        with open(filepath_yaml, 'r') as file:
            return yaml.safe_load(file)['register']

    # Try to load JSON file.
    #
    filename_json = '{name}.register.json'.format(name = register_name)
    filepath_json = os.path.join(dirpath_registry, filename_json)
    if os.path.isfile(filepath_json):
        import json
        with open(filepath_json, 'r') as file:
            return json.load(file)['register']

    raise RuntimeError('Could not find register: {name} in {dirpath}'.format(
                                                name    = register_name,
                                                dirpath = dirpath_registry))


# -----------------------------------------------------------------------------
def update(register_name, register_data, dirpath_lwc_root = None):
    """
    Write data to the specified register.

    All registers use YAML as their serialisation
    format; excepting the dependencies register
    which uses JSON.

    This function supports writing to YAML format
    registers only. Attempting to write to a JSON
    format register will raise a RuntimeError.

    ---
    type:   function
    ...

    """
    if register_data is None:
        return

    dirpath_registry = da.lwc.discover.path(
                                        key              = 'registry',
                                        dirpath_lwc_root = dirpath_lwc_root)

    filename_yaml    = '{name}.register.yaml'.format(name = register_name)
    filepath_yaml    = os.path.join(dirpath_registry, filename_yaml)
    if os.path.isfile(filepath_yaml):

        try:
            import ruamel.yaml
            _load_yaml = functools.partial(ruamel.yaml.load,
                                       Loader = ruamel.yaml.RoundTripLoader)
            _dump_yaml = functools.partial(ruamel.yaml.dump,
                                       Dumper = ruamel.yaml.RoundTripDumper)
        except ImportError:
            import yaml
            _load_yaml = functools.partial(yaml.load)
            _dump_yaml = functools.partial(yaml.dump)

        with open(filepath_yaml, 'rt') as file:

            str_yaml = file.read()
            data     = _load_yaml(str_yaml)

            for (key, value) in register_data.items():
                data['register'][key] = value

            str_yaml = _dump_yaml(data)

        with open(filepath_yaml, 'wt') as file:
            file.write(str_yaml)

        return

    # We cannot write to a JSON file.
    #
    filename_json = '{name}.register.json'.format(name = register_name)
    filepath_json = os.path.join(dirpath_registry, filename_json)
    if os.path.isfile(filepath_json):
        raise RuntimeError('Cannot write to JSON register: {path}'.format(
                                                        path = filepath_json))

    # Unknown register.
    #
    raise RuntimeError('Could not find register: {name} in {dirpath}'.format(
                                                name    = register_name,
                                                dirpath = dirpath_registry))
