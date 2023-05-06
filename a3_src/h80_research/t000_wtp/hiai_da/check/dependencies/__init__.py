# -*- coding: utf-8 -*-
"""
Dependencies register format and content validation functions.

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


import bisect
import copy
import difflib
import json
import os.path
import pprint
import textwrap

import da.check.constants
import da.check.dependencies.content
import da.check.dependencies.format
import da.lwc.discover
import da.lwc.env
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(dirpath_lwc_root, build_monitor):
    """
    Check the dependencies register for nonconformities.

    ---
    type:   coroutine
    ...

    """
    while True:

        build_unit = (yield)
        if not build_unit['filepath'].endswith('dependencies.register.json'):
            continue

        register = _load_register(dirpath_lwc_root)
        on_disk  = da.check.dependencies.content.get_reference_data(
                                        dirpath_lwc_root = dirpath_lwc_root)

        _check_register_format(       register,          build_monitor )
        _check_missing_sources(       register, on_disk, build_monitor )
        # TODO: _check_missing_documentation()
        _check_missing_from_register( register, on_disk, build_monitor )
        _check_content_consistency(   register, on_disk, build_monitor )


# -----------------------------------------------------------------------------
def _load_register(dirpath_lwc_root):
    """
    Return collated and loaded dependencies register file information.

    ---
    type:   function
    ...


    """
    dirpath  = da.lwc.discover.path(key = 'registry',
                                    dirpath_lwc_root = dirpath_lwc_root)
    filepath = os.path.join(dirpath, 'dependencies.register.json')

    with open(filepath, 'r') as file:
        json_text = file.read()

    data_raw  = json.loads(json_text)
    data_copy = copy.deepcopy(data_raw)
    register  = data_copy['register']
    da.lwc.env.set_register_absolute_paths(register         = register,
                                           dirpath_lwc_root = dirpath_lwc_root)
    data_with_paths = register
    return {
        'filepath':         filepath,
        'text':             json_text,
        'data_raw':         data_raw,
        'data_with_paths':  data_with_paths
    }


# -----------------------------------------------------------------------------
def _check_register_format(register, build_monitor):
    """
    Check the register format.

    We do this by generating a perfectly formatted version and
    then comparing it to the version on disc.

    Any discrepancy will be reported as a design nonconformity.

    ---
    type:   function
    ...

    """
    register_text  = register['text']
    reference_text = da.check.dependencies.format.get_reference_text(
                                                        register['data_raw'])
    if reference_text != register_text:

        reference_lines = reference_text.splitlines()
        register_lines  = register_text.splitlines()
        iline = 0
        for iline, lines in enumerate(zip(reference_lines, register_lines)):
            (ref_line, reg_line) = lines
            if ref_line != reg_line:
                break

        diff_text = '\n'.join((line for line in difflib.context_diff(
                                                        reference_lines,
                                                        register_lines,
                                                        'reference_format',
                                                        'current_register')))
        msg = 'Dependencies register format error '\
              'on line {line}:\n{diff}'.format(line = iline,
                                               diff = diff_text)

        build_monitor.report_nonconformity(
                            tool    = 'da.check.dependencies',
                            msg_id  = da.check.constants.DEP_REGISTER_FORMAT,
                            msg     = msg,
                            path    = register['filepath'],
                            line    = iline)


# -----------------------------------------------------------------------------
def _check_missing_sources(register, reference_data, build_monitor):
    """
    Check that all registered dependencies have sources on disk.

    ---
    type:   function
    ...

    """
    register_keys = set(register['data_with_paths'].keys())
    keys_on_disk  = set(reference_data.keys())
    missing_keys  = register_keys - keys_on_disk

    for key in missing_keys:
        # We don't necessarily expect to see the source code for
        # dependencies configured with a 'manual' build method.
        # Many of these dependencies are obtained as pre-built
        # binaries and do not have any available source code.
        #
        build_method = register['data_with_paths'][key]['build']['method']
        if build_method == 'manual':
            continue

        build_monitor.report_nonconformity(
                    tool    = 'da.check.dependencies',
                    msg_id  = da.check.constants.DEP_REGISTER_MISSING_FILES,
                    msg     = 'Dependency in register but not on disk: ' + key,
                    path    = register['filepath'])
        continue


# -----------------------------------------------------------------------------
def _check_missing_from_register(register, on_disk, build_monitor):
    """
    Check that all on-disk dependencies have a corresponding register entry.

    ---
    type:   function
    ...

    """
    register_keys = set(register['data_with_paths'].keys())
    on_disk_keys  = set(on_disk.keys())
    missing_keys  = on_disk_keys - register_keys

    for key in missing_keys:
        msg = textwrap.dedent("""
        Unregistered dependency detected: {key}

            (one of {shortfall} unregistered dependencies.)

        Suggested registry entry:

                "{key}": {{
                    "desc":             "TBD.",
                    "notes":            "TBD",
                    "labels":           [],
                    "dirname":          "{dirname}",
                    "policy":           "{policy}",
                    "api": {{
                    }},
                    "cli": {{
                    }},
                    "gui": {{
                    }},
                    "tgt":              ["e00_x86_64_linux_ubuntu_xenial"],
                    "config": {{
                        "method":       "{config_method}",
                        "tool":         "{config_tool}",
                        "url":          "{config_url}"
                    }},
                    "build": {{
                        "method":       "manual",
                        "tool":         "TBD"
                    }}
                }},""".format(
                        key           = key,
                        shortfall     = len(missing_keys),
                        dirname       = on_disk[key]['dirname'],
                        policy        = on_disk[key]['policy'],
                        config_method = on_disk[key]['config']['method'],
                        config_tool   = on_disk[key]['config']['tool'],
                        config_url    = on_disk[key]['config']['url'])).strip()

        build_monitor.report_nonconformity(
                        tool   = 'da.check.dependencies',
                        msg_id = da.check.constants.DEP_REGISTER_MISSING_ENTRY,
                        msg    = msg,
                        path   = register['filepath'],
                        line   = _line_number(register, key))


# -----------------------------------------------------------------------------
def _check_content_consistency(register, on_disk, build_monitor):
    """
    Compare the content of the dependencies register with the filesystem.

    Is the dependencies register consistent with the content of the
    depencencies directories (a0_env) on the filesystem?

    ---
    type:   function
    ...

    """
    register_keys = set(register['data_with_paths'].keys())
    on_disk_keys  = set(on_disk.keys())
    common_keys   = register_keys & on_disk_keys

    for key in common_keys:

        in_register_item   = register['data_with_paths'][key]
        on_disk_item       = on_disk[key]

        msg = _check_registered_config_method(
                    key       = key,
                    reg_item  = in_register_item,
                    disk_item = on_disk_item)
        if msg is not None:
            build_monitor.report_nonconformity(
                    tool    = 'da.check.dependencies',
                    msg_id  = da.check.constants.DEP_REGISTER_CONFIG_MISMATCH,
                    msg     = msg,
                    path    = register['filepath'],
                    line    = _line_number(register, key))

        msg = _check_registered_build_method(
                    key       = key,
                    reg_item  = in_register_item['build'],
                    disk_item = on_disk_item['build'])
        if msg is not None:
            build_monitor.report_nonconformity(
                    tool    = 'da.check.dependencies',
                    msg_id  = da.check.constants.DEP_REGISTER_BUILD_MISMATCH,
                    msg     = msg,
                    path    = register['filepath'],
                    line    = _line_number(register, key))


# -----------------------------------------------------------------------------
def _check_registered_config_method(key, reg_item, disk_item):
    """
    Compare the registered configuration method with the files on disk.

    Report a design nonconformity if the registered
    dependency configuration method is not consistent
    with the files that are physically present on disk.

    ---
    type:   function
    ...

    """
    registered_build  = reg_item['build']
    registered_config = reg_item['config']
    on_disk_config    = disk_item['config']

    # We dont check manual downloads.
    #
    if (     registered_config['method'] == 'manual'
         and on_disk_config['method']    == 'manual'):
        return

    # We don't necessarily expect to see the source code for
    # dependencies configured with a 'manual' build method.
    # Many of these dependencies are obtained as pre-built
    # binaries and do not have any available source code.
    #
    reg_build_method  = registered_build['method']
    reg_config_method = registered_config['method']
    if reg_build_method == 'manual' and reg_config_method == 'manual':
        return

    if registered_config != on_disk_config:

        msg = ('Version control or configuration management '
               'discrepancy detected for dependency: {key} \n\n'
               'in_register = \n {in_register} \n\n'
               'on_disk = \n {on_disk} \n').format(
                            key         = key,
                            in_register = pprint.pformat(registered_config),
                            on_disk     = pprint.pformat(on_disk_config))
        return msg


# -----------------------------------------------------------------------------
def _check_registered_build_method(key, reg_item, disk_item):
    """
    Compare the registered build method with the files on disk.

    Report a design nonconformity if the registered
    build method is not consistent with the files
    that are physically present on disk.

    ---
    type:   function
    ...

    """
    if reg_item['method'] != disk_item['method']:

        msg = ('Build method discrepancy detected for dependency: {key} \n\n'
               'in_register = \n {reg_item} \n\n'
               'on_disk = \n {disk_item} \n').format(
                            key       = key,
                            reg_item  = pprint.pformat(reg_item),
                            disk_item = pprint.pformat(disk_item))
        return msg


# -----------------------------------------------------------------------------
def _line_number(register, key):
    """
    Find the insertion point for the new registry entry.

    ---
    type:   function
    ...

    """
    line_number = 0
    register_keys = set(register['data_with_paths'].keys())
    with open(register['filepath']) as register_file:
        register_lines     = list(register_file)
        list_register_keys = sorted(list(register_keys))
        next_idx = bisect.bisect(list_register_keys, key)
        if next_idx == len(list_register_keys):
            last_line   = len(register_lines) - 1
            line_number = last_line
        else:
            next_key      = list_register_keys[next_idx]
            search_string = '"{key}": {{'.format(key = next_key)
            for (iline, line) in enumerate(register_lines):
                if line.strip().startswith(search_string):
                    line_number = iline
                    return line_number
    return line_number
