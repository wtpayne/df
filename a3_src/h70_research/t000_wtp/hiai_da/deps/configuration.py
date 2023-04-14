# -*- coding: utf-8 -*-
"""
Support for configuring dependencies in readiness for their build.

This module provides functions that support the
build-time configuration of dependencies;

Functions are provided that fetch source configuation
items from configured repositories at configured versions
and arrange those source items as appropriate for the
dependency to be built. (Compiled or otherwise prepared
for use)

TODO: Functions that interpret configuration policy to
      update the specific configuration to build.
      (To enable us to follow branches, latest stable
      release, latest development release etc...)

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

import logging

import da.exception
import da.log


# -----------------------------------------------------------------------------
@da.log.trace
def configure(dep):
    """
    Fetch and update source files for the specified dependency.

    Makes sure that the source design documents for
    the specified dependency comply with the version
    specified in the env.depmap.json configuration
    file.

    ---
    type:   function
    ...

    """
    if dep['config']['method'] == 'manual':
        return

    scm_tool_lut = {
        'bzr':    _bzr,
        'git':    _git,
        'darcs':  _darcs,
        'hg':     _hg,
        'svn':    _svn,
        'manual': _manual,
    }
    try:
        scm_tool_lut[dep['config']['tool']](dep)
    except KeyError:
        raise da.exception.ImplementationNotPresentError(
            'Did not recognise auto-checkout tool for {dep}'.format(dep = dep))


# -----------------------------------------------------------------------------
def _bzr(_):
    """
    Update dependency source design documents using Bazaar.

    ---
    type:   function
    ...

    """
    raise da.exception.ImplementationNotPresentError(
        'Bazaar auto-checkout not yet supported')


# -----------------------------------------------------------------------------
def _git(dep):
    """
    Update dependency source design documents using Git.

    ---
    type:   function
    ...

    """
    import git
    import da.vcs as _vcs  # Rename to prevent conflict w/outer da import.
    try:

        da.util.ensure_dir_exists(dep['dirpath_src'])
        _vcs.delete_untracked(dep['dirpath_src'])
        _vcs.ensure_cloned(dirpath_local = dep['dirpath_src'],
                           url_remote    = dep['config']['url'],
                           ref           = _get_version(dep))

    except git.GitCommandError:
        logging.warning('Attempt to fetch failed for: %s', dep['name'])

    except AssertionError as error:
        logging.error('Failed to configure %s', dep['name'])
        raise error


# -----------------------------------------------------------------------------
def _darcs(_):
    """
    Update dependency source design documents using Darcs.

    ---
    type:   function
    ...

    """
    raise da.exception.ImplementationNotPresentError(
        'Darcs auto-checkout not yet supported')


# -----------------------------------------------------------------------------
def _hg(_):
    """
    Update dependency source design documents using Mercurial.

    ---
    type:   function
    ...

    """
    raise da.exception.ImplementationNotPresentError(
        'Mercurial auto-checkout not yet supported')


# -----------------------------------------------------------------------------
def _svn(_):
    """
    Update dependency source design documents using Subversion.

    ---
    type:   function
    ...

    """
    raise da.exception.ImplementationNotPresentError(
        'Subversion auto-checkout not yet supported')


# -----------------------------------------------------------------------------
def _manual(_):
    """
    Update dependency source design documents manually.

    ---
    type:   function
    ...

    """
    raise da.exception.ImplementationNotPresentError(
        'Cannot auto-checkout unless a tool is specified.')


# -----------------------------------------------------------------------------
@da.log.trace
def _get_version(dep):
    """
    Return the version of the dependency to build.

    ---
    type:   function
    ...

    """
    policy = dep['policy']
    is_fixed_version = policy.startswith('ver_')
    if is_fixed_version:
        policy_parts = policy.split('_')
        version = policy_parts[1]
        return version

    # TODO: Automatic dependency upgrades.
    #
    # At the moment, we only handle a single policy
    # type for our dependencies: downloading and
    # building a user-defined version. In the future,
    # we may wish to automate the process of upgrading
    # dependencies by downloading and building the
    # latest release (lexicograpically largest vcs
    # tag that is formatted like an x.y.z semantic
    # version number); or even the latest commit
    # from a specified branch.
    #
    # Suggested policy naming convention:
    #   - latest_<BRANCH_NAME>      - Most recent commit on specified branch.
    #   - greatest_semver_tag       - Tag with highest ranked semantic version.
    #   - greatest_<MAJOR>.<MINOR>  - Tag with highest version in MAJOR.MINOR.
