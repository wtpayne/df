# -*- coding: utf-8 -*-
"""
Functions to support building binary dependencies.

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


import re
import logging

import da.log
import da.lwc.env


# -----------------------------------------------------------------------------
@da.log.trace
def build(dep_build_cfg, dirpath_lwc_root):
    """
    Compile or otherwise prepare dependencies for use.

    This function compiles or otherwise prepares
    all tools, libraries and other dependencies
    that support the current runtime environment.

    Cross compiling of dependencies is not currently
    supported and is unlikely ever to be supported.

    ---
    type:   function
    ...

    """
    from . import configuration

    for (key, register_entry) in _gen_entries(dep_build_cfg, dirpath_lwc_root):

        if dep_build_cfg['enable_dep_fetch_src']:
            logging.debug('Configure source documents for: %s', key)
            configuration.configure(register_entry)

        if dep_build_cfg['enable_dep_build']:
            logging.debug('Build: %s', key)
            _build_dependency(register_entry   = register_entry,
                              dep_build_cfg    = dep_build_cfg,
                              dirpath_lwc_root = dirpath_lwc_root)

    return


# -----------------------------------------------------------------------------
@da.log.trace
def _gen_entries(dep_build_cfg, dirpath_lwc_root):
    """
    Yield the register entry for each dependency configured to be built.

    """
    limitation = dep_build_cfg['limitation']
    exclusion  = dep_build_cfg['exclusion']
    register = da.lwc.env.dependencies_register(dirpath_lwc_root)

    # Adjust the build order to prevent
    # issues during bootstrapping.
    #
    keylist = sorted(register.keys())
    keylist.remove('setuptools')
    keylist.insert(0, 'setuptools')

    for key in keylist:

        # Skip dependency module if it matches exclusion criteria.
        #
        if (exclusion is not None) and re.match(exclusion, key):
            continue

        # Skip dependency module if it does not match limitation criteria.
        #
        if (limitation is not None) and (not re.match(limitation, key)):
            continue

        register_entry = register[key]
        yield (key, register_entry)


# -----------------------------------------------------------------------------
@da.log.trace
def _build_dependency(register_entry, dep_build_cfg, dirpath_lwc_root):
    """
    Construct the dependency from its design documents.

    In early iterations of the system the dependency
    build process would overwrite the dependency
    binaries.

    The dependency build process is itself a client
    of these dependencies, which led to situations
    where a failed dependency build would completely
    break the dependency build logic, requiring
    time-consuming manual intervention to set right.

    The following requirements are intended to prevent
    this and similar regressions from recurring.

    ---
    i00081_dependency_builds_should_not_cause_regressions:
      - "When a dependency is built all clients of
        that dependecy SHOULD be able to continue
        operating correctly with no regressions."
      - notes: "This is desirable but not economically
               viable as it would require comprehensive
               automated testing for every dependency.
               It should be possible to achieve some
               more limited requirements however."
      - type: guidance
      - state: draft

    i00083_failed_dependency_builds_shall_not_cause_regressions:
      - "When the build process for a dependency
        does not complete successfully and previously
        configured dependency build output exists
        then the dependency build logic SHALL provide
        clients of the dependency with the previously
        configured dependency build output."
      - notes: "When the dependency build process
               reports failure there is no real
               reason why we should not be able to
               back out and restore the previously
               configured dependency binaries."
      - type: mandate
      - state: draft
    ...
    """
    if register_entry['build']['method'] == 'manual':
        logging.debug('Manual build. (Skip)')
        return

    from . import python
    if register_entry['build']['tool'] == 'python_distutils':
        logging.debug('Build python library using distutils')
        python.build(
                extra_args       = None,
                register_entry   = register_entry,
                dep_build_cfg    = dep_build_cfg,
                dirpath_lwc_root = dirpath_lwc_root)

    elif register_entry['build']['tool'] == 'python_setuptools':
        logging.debug('Build python library using setuptools')
        python.build(
                extra_args       = ['--single-version-externally-managed'],
                register_entry   = register_entry,
                dep_build_cfg    = dep_build_cfg,
                dirpath_lwc_root = dirpath_lwc_root)

    # Commands to build CMAKE:
    # ./bootstrap --no-qt-gui
    #             --prefix={OUTPUT_DIR}x
    #             --datadir=data
    #             --docdir=doc
    #             --mandir=man
    #             --xdgdatadir=xdg && make && make install

    else:
        raise RuntimeError(
                'Did not recognise build tool for {name}'.format(
                                               name = register_entry['name']))
