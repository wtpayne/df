# -*- coding: utf-8 -*-
"""
---

title:
    "Configuration file loader module."

description:
    "This component has utilities to load
    various different sorts of configuration
    file."

id:
    "5e57efae-330b-4c0e-b31e-cb6769ef2c5b"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""

import glob
import os.path

import fl.stableflow.cfg.util



# -----------------------------------------------------------------------------
def from_path(path_cfg):
    """
    Return configuration loaded from the specified path.

    """
    if path_cfg is None:
        return dict()

    if os.path.isdir(path_cfg):
        return from_dirpath(dirpath_cfg = path_cfg)

    if os.path.isfile(path_cfg):
        return from_filepath(path_cfg)

    raise RuntimeError('The specified configuration path does not exist.')


# -----------------------------------------------------------------------------
def from_dirpath(dirpath_cfg):
    """
    Return configuration loaded from the specified directory path.

    Files with the shortest filenames are loaded
    first. These files correspond to branches
    rooted close to the overall root of the
    configuration tree.

    Files with the longest filenames are loaded
    last, overriding any previously loaded values.
    These files correspond to the narrowest, most
    specific branches and leaves of the
    configuration tree.

    In this way, files containing configuration
    which is more specific and narrower in scope
    overrides the configuration loaded earlier
    on in the process, from files which are
    broader in scope and less specific.

    """
    suffix        = '.cfg.*'
    glob_expr     = dirpath_cfg + os.sep + '*' + suffix
    glob_result   = glob.glob(glob_expr)
    list_fileinfo = []
    for filepath_cfg in glob_result:
        filepath_parts  = os.path.split(filepath_cfg)
        filename        = filepath_parts[-1]
        filename_parts  = filename.split('.')
        filename_prefix = '.'.join(filename_parts[:-2])
        section_address = filename_prefix
        if section_address == 'root':
            sort_key = 0
        else:
            sort_key = len(section_address)
        list_fileinfo.append((sort_key, filepath_cfg, section_address))

    cfg = dict()
    for (_, filepath_cfg, section_address) in sorted(list_fileinfo):
        cfg = _apply(cfg,
                    section_address,
                    from_filepath(filepath_cfg),
                    delim_cfg_addr = '.')
    return cfg


# -----------------------------------------------------------------------------
def _apply(data, address, value, delim_cfg_addr = '.'):
    """
    Apply a single configuration field override on the specified path.

    """
    addr_parts = address.split(delim_cfg_addr)
    subtree    = data

    for key in addr_parts[:-1]:
        if key not in subtree:
            subtree[key] = dict()
        subtree = subtree[key]
    key = addr_parts[-1]
    subtree[key] = value
    return data


# -----------------------------------------------------------------------------
def from_filepath(filepath_cfg):
    """
    Return confiuguration data loaded from the specified file path.

    """
    map_reader = {
        '.xml':  _from_xml_file,
        '.json': _from_json_file,
        '.yaml': _from_yaml_file,
        '.toml': _from_toml_file,
    }
    for (str_ext, fcn_reader) in map_reader.items():
        if filepath_cfg.endswith(str_ext):
            with open(filepath_cfg) as file_cfg:
                return fcn_reader(filepath_cfg, file_cfg)
    raise CfgError('Did not recognize filename extension.')


# -----------------------------------------------------------------------------
def _from_xml_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified XML file path.

    """
    import xmltodict  # pylint: disable=C0415
    cfg = xmltodict.parse(file_cfg.read())
    if tuple(cfg.keys()) == ('root',):
        cfg = cfg['root']
    return cfg


# -----------------------------------------------------------------------------
def _from_json_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified JSON file path.

    """
    import json  # pylint: disable=C0415
    list_str_line = []
    for str_line in file_cfg:
        str_line_naked = str_line.strip()
        if str_line_naked.startswith('//') or str_line_naked.startswith('#'):
            continue
        list_str_line.append(str_line)
    return json.loads(''.join(list_str_line))


# -----------------------------------------------------------------------------
def _from_yaml_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified YAML file path.

    """
    return from_yaml_string(str_yaml     = file_cfg.read(),
                            filepath_cfg = filepath_cfg)


# -----------------------------------------------------------------------------
def from_yaml_string(str_yaml, filepath_cfg = 'memory'):
    """
    Return confiuguration data loaded from the specified YAML format string.

    """
    try:
        import yaml  # pylint: disable=C0415
        loader = yaml.SafeLoader
        yaml.add_constructor('!regex',
                             lambda l, n: str(n.value),
                             Loader = loader)
        return yaml.load(str_yaml, Loader = loader)
    except yaml.YAMLError as err:
        if hasattr(err, 'problem_mark'):
            mark = err.problem_mark
            location = '({line}:{column})'.format(line   = mark.line   + 1,
                                                  column = mark.column + 1)
        else:
            location = ''
        raise fl.stableflow.cfg.exception.CfgError(
                'Error reading file: {path} {loc}\n\n{msg}\n'.format(
                                                        path = filepath_cfg,
                                                        loc  = location,
                                                        msg  = str(err)))


# -----------------------------------------------------------------------------
def _from_toml_file(filepath_cfg, file_cfg):  # pylint: disable=W0613
    """
    Return confiuguration data loaded from the specified TOML file path.

    """
    import toml  # pylint: disable=C0415
    return toml.loads(file_cfg.read())
