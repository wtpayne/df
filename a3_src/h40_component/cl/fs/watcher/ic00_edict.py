# -*- coding: utf-8 -*-
"""
---

title:
    "File watcher and loader stableflow-edict component."

description:
    "This component watches one or more
    directories for content and changes
    and then outputs the details of any
    changed files."

id:
    "438bf477-cf5a-427b-8652-f34a87c2257a"

type:
    dt004_python_stableflow_edict_component

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2022 William Payne"

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


import cl.design.watcher._impl


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    File system montior component coroutine.

    do_repeat_all takes precedence over do_terminate_when_done

    """
    signal = None

    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    iter_dirpath_root      = cfg.get('iter_dirpath_root',      list() )
    iter_pathincl          = cfg.get('iter_pathincl',          list() )
    iter_pathexcl          = cfg.get('iter_pathexcl',          list() )
    iter_direxcl           = cfg.get('iter_direxcl',           list() )
    iter_read_as_txt       = cfg.get('iter_read_as_txt',       list() )
    iter_read_as_bin       = cfg.get('iter_read_as_bin',       list() )
    size_batch             = cfg.get('size_batch',             None   )
    do_output_all          = cfg.get('do_output_all',          False  )
    do_repeat_all          = cfg.get('do_repeat_all',          False  )
    do_output_modified     = cfg.get('do_output_modified',     False  )
    do_terminate_when_done = cfg.get('do_terminate_when_done', False  )

    gen_list_fileinfo = cl.design.watcher._impl.gen_list_fileinfo(
                            iter_dirpath_root      = iter_dirpath_root,
                            iter_pathincl          = iter_pathincl,
                            iter_pathexcl          = iter_pathexcl,
                            iter_direxcl           = iter_direxcl,
                            iter_read_as_txt       = iter_read_as_txt,
                            iter_read_as_bin       = iter_read_as_bin,
                            size_batch             = size_batch,
                            do_output_all          = do_output_all,
                            do_repeat_all          = do_repeat_all,
                            do_output_modified     = do_output_modified,
                            do_terminate_when_done = do_terminate_when_done)

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # Work out if we have any
        # enabled inputs and grab
        # the timestamp for the
        # current simulation step
        # if so.
        #
        is_any_enabled = False
        map_ts         = None
        for input_dict in inputs.values():
            if input_dict['ena']:
                is_any_enabled = True
                map_ts = input_dict['ts']

        # Try to generate the next
        # batch of file information
        # and output it if we get
        # any.
        #
        if is_any_enabled:
            list_fileinfo = next(gen_list_fileinfo)
            if list_fileinfo:
                for id_out in outputs.keys():
                    outputs[id_out]['ena'] = True
                    outputs[id_out]['ts'].update(map_ts)
                    outputs[id_out]['list'][:] = list_fileinfo
