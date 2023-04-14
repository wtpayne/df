# -*- coding: utf-8 -*-
"""
The console_reporter module reports build progress to the console.

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


import contextlib
import datetime
import itertools
import os
import os.path

import click
import py

import da
import da.constants
import da.util


# -----------------------------------------------------------------------------
@da.util.coroutine
def coro(cfg, url_build_report):
    """
    Coroutine for reporting build progress to the command line interface.

    ---
    type:   coroutine
    ...

    """
    _print_cli_header(
        build_id         = cfg['build_id'],
        relpath_cfg      = cfg['relpath_cfg'],
        commit_summary   = cfg['defined_baseline']['commit_summary'],
        url_build_report = url_build_report)

    # For the progress bar to work fully, we
    # need an estimate of the total number of
    # build units that we will be processing
    # in the build.
    #
    # Build units are (in general) generated
    # lazily, so this information is not
    # readily available at the start of the
    # build.
    #
    # To generate an estimate for this figure,
    # we use a cache to store the number (count)
    # of build_units processed in previous builds,
    # indexed by build configuration id and branch
    # name, so we can retrieve the matching count
    # -- on the assumption that little of
    # significance has changed.
    #
    # It won't always be correct, but it should
    # not often be wrong by much. Good enough.
    #
    with _cache_context(
                dirpath_cache = cfg['paths']['rootpath_tmp'],
                branch_name   = cfg['safe_branch_name'],
                cfg_name      = cfg['cfg_name']) as cache:

        # TODO: Configure progressbar on/off;
        # TODO: Consider alternate curses based UI.
        build_unit = (yield)

        # ---------------------------------------------------------------------
        def _item_show_closure(_):
            """
            Return the string to be displayed on the RHS of the progressbar.

            ---
            type:   function
            ...

            """
            relpath        = build_unit['relpath']
            relpath_parts  = relpath.split(os.sep, maxsplit = 1)
            display_string = relpath_parts[-1]
            return display_string

        iunit      = 0
        if build_unit != da.constants.BUILD_COMPLETED:
            with click.progressbar(
                    length         = cache['num_build_units'],
                    show_eta       = False,
                    show_percent   = False,
                    show_pos       = True,
                    item_show_func = _item_show_closure,
                    label          = _pad_key('Progress:')) as progressbar:
                for iunit in itertools.count(0):
                    if build_unit == da.constants.BUILD_COMPLETED:
                        break
                    else:
                        progressbar.update(1)
                    build_unit = (yield)

        # Update the cache.
        cache['num_build_units'] = iunit

    _print_cli_footer(
        start_time = cfg['timestamp']['datetime_utc'],
        end_time   = datetime.datetime.utcnow())
    os.sync()

    _ = (yield)  # Prevent StopIteration from being raised.


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _cache_context(dirpath_cache, branch_name, cfg_name):
    """
    Yield build cache data as a context object, saving any changes upon exit.

    ---
    type:   context_manager
    ...

    """
    filepath = os.path.join(dirpath_cache, 'build_monitor_cache.json')
    key      = '{branch_name}.{cfg_name}'.format(branch_name = branch_name,
                                                 cfg_name    = cfg_name)

    if os.path.isfile(filepath):
        cache = da.util.load(filepath)
    else:
        cache = dict()

    if key not in cache or 'num_build_units' not in cache[key]:
        cache[key] = { 'num_build_units': 130 }

    yield cache[key]

    da.util.save(filepath, cache)


# -----------------------------------------------------------------------------
def _print_cli_header(build_id, relpath_cfg, commit_summary, url_build_report):
    """
    Print a build-process header to the console.

    ---
    type:   function
    ...

    """
    click.clear()
    _msg('Build id:',    build_id)          # Identify the build
    _msg('Config file:', relpath_cfg)       # Build configuration file
    _msg('Last commit:', commit_summary)    # Provide some human-scale context.
    _msg('Report:',      url_build_report)  # Link to more detailed info.


# -----------------------------------------------------------------------------
def _print_cli_footer(start_time, end_time):
    """
    Print a build-process footer to the console.

    ---
    type:   function
    ...

    """
    delta_secs = (end_time - start_time).total_seconds()
    _msg('Completed in:', '{secs:0.0f}s.'.format(secs = delta_secs))


# -----------------------------------------------------------------------------
def _sort_key(nonconformity):
    """
    Return a sort key for the nonconformity list.

    We sort by filepath in ascending lexicographic
    order then by line number in descending numerical
    order.

    This enables us to systematically address each
    nonconformity report in the list in turn. Because
    we will be fixing issues starting at the end of
    each file, working our way towards the
    beginning, our edits are not likely to change
    the validity of the line number for subsequent
    nonconformity reports.

    Sorting by line in descending order helps us
    when we are going through the nonconformities

    ---
    type:   function
    ...

    """
    try:
        order = -1 * int(nonconformity['line'])
    except KeyError:
        order = 0
    return (nonconformity['path'], order)


# -----------------------------------------------------------------------------
def print_all_nonconformities(nonconformity_list):
    """
    Log every nonconformity in the list.

    TODO: LOG NONCONFORMITY IN A FILE SOMEWHERE

    ---
    type:   function
    ...

    """
    click.echo('')
    nonconformity_count = len(nonconformity_list)
    termwriter          = py.io.TerminalWriter()        # pylint: disable=E1101
    for (idx, nonconformity) in enumerate(sorted(
                                        nonconformity_list, key = _sort_key)):

        is_even = (idx % 2) == 0
        if is_even:
            style = dict(fg   = 'blue', bold = True)
        else:
            style = dict(fg   = 'blue', bold = False)

        termwriter.sep(
            '=', 'Nonconformity {idx} / {total}'.format(
                                                idx   = idx + 1,
                                                total = nonconformity_count))

        _print_one_nonconformity(nonconformity, style)
    termwriter.sep('=', 'End of nonconformity report')


# -----------------------------------------------------------------------------
def _print_one_nonconformity(nonconformity, styles):
    """
    Print one nonconformity from the list of nonconformities.

    Alternating colours for readability.

    ---
    type:   function
    ...

    """
    noncon_id = '{tool}.{msg_id}'.format(tool   = nonconformity['tool'],
                                         msg_id = nonconformity['msg_id'])
    _msg('Id:', noncon_id, **styles)

    _msg('Path:', nonconformity['path'], **styles)

    line = nonconformity['line']
    if line is not None:
        _msg('Line:', line, **styles)

    click.secho('Msg:\n\n{msg}\n'.format(msg = nonconformity['msg']), **styles)


# -----------------------------------------------------------------------------
def _msg(key, value = None, **styles):
    """
    Write a key: value pair to the console.

    ---
    type:   function
    ...

    """
    click.secho('{key}  {value}'.format(key   = _pad_key(key),
                                        value = value if value else ''),
                **styles)


# -----------------------------------------------------------------------------
def _pad_key(key):
    """
    Return a key string padded out to 14 characters.

    ---
    type:   function
    ...

    """
    return '{key:14s}'.format(key = key)
