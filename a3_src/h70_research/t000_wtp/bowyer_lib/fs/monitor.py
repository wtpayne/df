# -*- coding: utf-8 -*-
"""
Filesystem monitor component for bowyer.

Monitor one or more directories for content and changes.

"""


import collections
import itertools
import multiprocessing
import os
import queue
import re
import sys
import time

import watchdog.events
import watchdog.observers

import bowyer.signal


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    File system montior component coroutine.

    """
    signal = None

    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    gen_filepath = _batch_filepath_generator(
                            iter_dirpath_root = cfg.get('dirpath_root'),
                            iter_pathincl     = cfg.get('pathincl',      None),
                            iter_pathexcl     = cfg.get('pathexcl',      None),
                            iter_direxcl      = cfg.get('direxcl',       None),
                            size_batch        = cfg.get('batch_size',    50),
                            do_changes        = cfg.get('changes',       False),
                            do_static_files   = cfg.get('static_files',  True),
                            do_repeat_static  = cfg.get('repeat_static', False),
                            do_halt_after     = cfg.get('halt_after',    True))

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        id_in = 'control'
        if not inputs[id_in]['ena']:
            continue

        list_filepath = next(gen_filepath)

        # If any filepaths are ready for
        # processing, then output them.
        #
        if list_filepath:
            map_ts = inputs[id_in]['ts']
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_filepath


# -----------------------------------------------------------------------------
def _batch_filepath_generator(iter_dirpath_root,
                              iter_pathincl,
                              iter_pathexcl,
                              iter_direxcl,
                              size_batch,
                              do_changes,
                              do_static_files,
                              do_repeat_static,
                              do_halt_after):
    """
    Yield filepaths from the specified search criteria.

    """
    gen_filepath_mod = iter(tuple())
    if do_changes:
        gen_filepath_mod = _gen_list_filepath_modified(
                                    iter_dirpath_root = iter_dirpath_root,
                                    iter_pathincl     = iter_pathincl,
                                    iter_pathexcl     = iter_pathexcl,
                                    iter_direxcl      = iter_direxcl)

    # For each repeat pass over
    # the filesystem tree.
    #
    while True:

        gen_filepath_static = iter(tuple())
        if do_static_files:
            gen_filepath_static = _generate_all_static_files(
                                        iter_dirpath_root = iter_dirpath_root,
                                        iter_pathincl     = iter_pathincl,
                                        iter_pathexcl     = iter_pathexcl,
                                        iter_direxcl      = iter_direxcl)

        # For each batch of filepaths to be
        # returned (simulation step).
        #
        while True:

            batch = list()

            # Start by adding any recently
            # modified files.
            #
            if do_changes:
                batch.extend(next(gen_filepath_mod))

            if not do_static_files:
                yield batch
                continue

            # Now fill the rest of the batch up
            # with static files.
            #
            try:
                while len(batch) < size_batch:
                    batch.append(next(gen_filepath_static))
                yield batch

            except StopIteration:
                if batch:
                    yield batch
                break

        if not do_repeat_static:
            do_static_files = False

        if do_halt_after:
            break


# -----------------------------------------------------------------------------
def _generate_all_static_files(iter_dirpath_root,
                               iter_pathincl,
                               iter_pathexcl,
                               iter_direxcl):
    """
    Yield filepaths of matching files from the list of roots.

    """
    list_generator = list()
    for dirpath_root in iter_dirpath_root:
        list_generator.append(
            _filtered_filepath_generator(dirpath_root,
                                         iter_pathincl = iter_pathincl,
                                         iter_pathexcl = iter_pathexcl,
                                         iter_direxcl  = iter_direxcl))
    return itertools.chain.from_iterable(list_generator)


# --------------------------------------------------------------------------
def _filtered_filepath_generator(dirpath_root,
                                 iter_pathincl,
                                 iter_pathexcl,
                                 iter_direxcl):

    """
    Yield each matching file in the directory tree under dirpath_src.

    """

    re_pathincl = _combine_regex(iter_regex = iter_pathincl, op = '|')
    re_pathexcl = _combine_regex(iter_regex = iter_pathexcl, op = '|')
    re_direxcl  = _combine_regex(iter_regex = iter_direxcl,  op = '|')
    os_walk     = os.walk(dirpath_root,
                          topdown     = True,
                          onerror     = None,
                          followlinks = False)

    for (dirpath, list_dirname, iter_filename) in os_walk:

        # Keep for further consideration only
        # those directories which do not match
        # the directory-exclusion regex.
        #
        list_dirname_ok = []
        for dirname in list_dirname:
            is_included = re_direxcl.match(dirname) is None
            if is_included:
                list_dirname_ok.append(dirname)
        list_dirname[:] = sorted(list_dirname_ok)

        for filename in iter_filename:
            filepath = os.path.join(dirpath, filename)

            is_excluded = re_pathexcl.match(filepath) is not None
            if is_excluded:
                continue

            is_included = re_pathincl.match(filepath) is not None
            if is_included:
                yield filepath


# --------------------------------------------------------------------------
def _combine_regex(iter_regex, op = '|'):
    """
    Combine and then compile an iterable of regular expression strings.

    """
    if iter_regex is None:
        return re.compile('(?!x)x')  # Will never match anything

    str_delim = '){op}('.format(op = op)
    str_inner = str_delim.join(iter_regex)
    str_regex = '({inner})'.format(inner = str_inner)
    obj_regex = re.compile(str_regex)
    return obj_regex


#-----------------------------------------------------------------------------
def _gen_list_filepath_modified(iter_dirpath_root,
                                iter_pathincl,
                                iter_pathexcl,
                                iter_direxcl):
    """
    Yield a list of filepaths of recently modified matching files.

    """
    re_pathincl = _combine_regex(iter_regex = iter_pathincl, op = '|')
    re_pathexcl = _combine_regex(iter_regex = iter_pathexcl, op = '|')
    re_direxcl  = _combine_regex(iter_regex = iter_direxcl,  op = '|')

    list_tup_observer_handler = _list_tup_observer_handler(iter_dirpath_root)

    while True:
        list_path = list()
        for (observer, handler) in list_tup_observer_handler:
            for filepath in _modified_files(handler):

                # Check to see if the modified
                # filepath is excluded (or not
                # included) according to the
                # two whole-path filters.
                #
                is_path_excluded = re_pathexcl.match(filepath) is not None
                is_path_included = re_pathincl.match(filepath) is not None
                if is_path_excluded or (not is_path_included):
                    continue

                # Check to see if any of the
                # directory names in the
                # filepath are excluded by
                # the directory-name filter.
                #
                dirpath             = os.path.dirname(filepath)
                iter_dirname        = dirpath.split(os.sep)
                is_dirname_excluded = False
                for dirname in iter_dirname:
                    is_dirname_excluded = re_direxcl.match(dirname) is not None
                    if is_dirname_excluded:
                        break
                if is_dirname_excluded:
                    continue

                list_path.append(filepath)

        yield sorted(list_path)


# -----------------------------------------------------------------------------
def _list_tup_observer_handler(iter_dirpath_root):
    """
    Return a list of change-observer, change-handler tuple pairs.

    """
    list_tup_observer_handler = list()
    for dirpath_root in iter_dirpath_root:
        observer  = watchdog.observers.Observer()
        handler   = EventEnqueueingHandler()
        observer.schedule(event_handler = handler,
                          path          = dirpath_root,
                          recursive     = True)
        observer.start()
        list_tup_observer_handler.append((observer, handler))
    return list_tup_observer_handler


# -----------------------------------------------------------------------------
def _modified_files(handler):
    """
    Return a list of modified files from the specified event handler.

    """
    list_filepath  = list()
    list_tup_event = handler.get()
    for tup_event in list_tup_event:

        if tup_event.is_dir:
            continue

        if tup_event.path_dst is not None:
            list_filepath.append(tup_event.path_dst)
            continue

        if tup_event.path_src is not None:
            list_filepath.append(tup_event.path_src)
            continue

    return list_filepath


# =============================================================================
TupEvent = collections.namedtuple(
                        'TupEvent', ['type', 'path_src', 'path_dst', 'is_dir'])


# =============================================================================
class EventEnqueueingHandler(watchdog.events.FileSystemEventHandler):
    """
    Enqueues watchdog filesystem events for bowyer to pick up.

    """

    # -------------------------------------------------------------------------
    def __init__(self):
        """
        Construct a EventEnqueueingHandler instance.

        """
        super(EventEnqueueingHandler, self).__init__()
        self.queue = multiprocessing.Queue()


    # -------------------------------------------------------------------------
    def on_moved(self, event):
        """
        Dispatch watchdog.events.FileMovedEvent events.

        """
        super(EventEnqueueingHandler, self).on_moved(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def on_created(self, event):
        """
        Dispatch watchdog.events.FileCreatedEvent events.

        """
        super(EventEnqueueingHandler, self).on_created(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def on_deleted(self, event):
        """
        Dispatch watchdog.events.FileDeletedEvent events.

        """
        super(EventEnqueueingHandler, self).on_deleted(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def on_modified(self, event):
        """
        Dispatch watchdog.events.FileModifiedEvent events.

        """
        super(EventEnqueueingHandler, self).on_modified(event)
        self._enqueue(event)

    # -------------------------------------------------------------------------
    def _enqueue(self, event):
        """
        Add the specified event to the queue.

        """
        path_src   = None
        path_dst   = None
        is_dir     = False

        if hasattr(event, 'src_path'):
            if event.src_path:
                path_src = event.src_path

        if hasattr(event, 'dest_path'):
            if event.dest_path:
                path_dst = event.dest_path

        if hasattr(event, 'is_directory'):
            if event.is_directory:
                is_dir = event.is_directory

        tup_event = TupEvent(type     = event.event_type,
                             path_src = path_src,
                             path_dst = path_dst,
                             is_dir   = is_dir)
        self.queue.put(tup_event, block = False)

    # -------------------------------------------------------------------------
    def get(self):
        """
        Get all events currently on the queue.

        """
        set_tup_event = set()
        while True:
            try:
                set_tup_event.add(self.queue.get(block = False))
            except queue.Empty:
                break
        list_tup_event = list(set_tup_event)
        return(list_tup_event)