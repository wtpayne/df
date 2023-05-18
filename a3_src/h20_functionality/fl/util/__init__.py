# -*- coding: utf-8 -*-
"""
---

title:
    "Utility module."

description:
    "This module contains various bits of
    general purpose utility functionality."

id:
    "b34331cb-926d-4efa-aa88-0797b7067ed3"

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


import collections
import collections.abc
import contextlib
import functools
import importlib
import itertools
import os.path
import pprint
import string
import time
import typing


# Command used by Bureau and BureauEngine to mutate state.
#
Command = collections.namedtuple(
    typename    = 'Command',
    field_names = ('operation', 'idx', 'time_utc', 'path', 'value_new', 'value_old'),
    defaults    = ('edit',      0,     0.0,        '',     None,        None))


# Rule used by Bureau and BureauEngine to filter and modify commands.
#
Rule = collections.namedtuple(
    typename    = 'Rule',
    field_names = ('condition', 'action'))


# =============================================================================
class Bureau(collections.abc.MutableMapping):
    """
    Custom dictionary class intended to help manage application state.

    """

    # Instance private attributes
    # are given special handling
    # so they don't get treated
    # as regular keys.
    #
    _bureau_attributes = ('_bureau_attributes',
                          '_bureau_data',
                          '_bureau_engine',
                          '_bureau_path',
                          '_bureau_path_delimiter')

    # -------------------------------------------------------------------------
    def __init__(self, path = None, engine = None, path_delimiter = '.'):
        """
        Returns a new Bureau instance.

        The Bureau class defines a container
        that conforms to the standard library
        dictionary interface and whose instances
        are intended to be used as nodes in a
        larger tree structured hierarchical data
        store.

        The Bureau class supports both dict-like
        and attribute-like field access. Keys
        can be both atomic keys, dot-delimited
        string paths, or tuple paths. When keys
        are path-like in form, they are used to
        access data structures which are nested
        under the current instance.

        Each overall tree maintains unitary
        edit/undo histories and supports simple
        undo and redo functionality.

        Each tree also maintains unitary callback
        tables and supports callback registration
        for change listeners.

        TODO: Add path/filter/rules parameter for data savers/exporters.
        TODO: Save/Load (journal?/state?) to/from SQLITE

        TODO: Support for remote sync (Load/update from journal)
        TODO: Design mechanism for binding to other Bureau trees.
        TODO: Filters and rulesets.

        TODO: Reactive programming with RxPy ???
        TODO: Regex-based listening on paths. (jquery-like?) ???

        """

        # Bureau data is the underlying datastore
        # for this node in the overall tree.
        #
        self._bureau_data = dict()

        # The engine handles undo/redo and
        # callbacks. There is a single engine
        # for each tree. All nodes in the tree
        # have a reference to it.
        #
        if engine is None:
            self._bureau_engine = BureauEngine(bureau = self)
        else:
            self._bureau_engine = engine

        # The path is the path to the current
        # node in the tree. This is stored
        # internally as a tuple of strings.
        #
        if path is None:
            self._bureau_path = tuple()
        else:
            self._bureau_path = path

        # The path delimiter (normally '.'') is
        # used to delimit string paths.
        #
        self._bureau_path_delimiter = path_delimiter

    # -------------------------------------------------------------------------
    def to_tuple(self):
        """
        Return a representation of self as a key-value tuple.

        """

        return tuple(walkobj(obj      = self,
                             gen_leaf = True,
                             gen_path = True,
                             gen_obj  = True))

    # -------------------------------------------------------------------------
    def from_tuple(self, tup_kv, path_root = tuple()):
        """
        Update Bureau from a key-value tuple.

        """
        if path_root:
            tup_path_root = tuple(_iter_path(
                                        path  = path_root,
                                        delim = self._bureau_path_delimiter))
        else:
            tup_path_root = self._bureau_path

        for (tup_path, value) in tup_kv:
            self._bureau_engine.set_item(path      = tup_path_root + tup_path,
                                         value_new = value)

    # -------------------------------------------------------------------------
    def to_dict(self):
        """
        Return a representation of self as a nested dict.

        This function converts the current Bureau
        instance into a nested dictionary
        representation.

        This method traverses the object using
        the `walkobj` utility function (via the
        to_tuple method), which generates length
        two tuples where the first element is a
        path indicating a location in the Bureau
        and the second element is the value at
        that path location.

        The paths are sorted by their length as
        a (probably unnecessary) sanity check
        to ensure that parent dictionaries are
        created before their children.

        For each path-value pair, this method
        creates nested dictionaries within the
        output dictionary according to the path,
        and sets the innermost dictionary's value
        according to the value.

        The resulting dictionary has the same
        nested structure as the original object,
        and can be used for purposes like
        serialization.

        :returns:   A nested dictionary representation of the object. The
                    keys in the dictionary correspond to the paths in the
                    object, and the values in the dictionary correspond
                    to the values in the object.

        """

        output = dict()

        for (tup_path, value) in sorted(self.to_tuple(),
                                        key = lambda item: len(item[0])):

            cursor = output
            for name in tup_path[:-1]:
                if name not in cursor:
                    cursor[name] = dict()
                cursor = cursor[name]
            name = tup_path[-1]
            cursor[name] = value

        return output

    # -------------------------------------------------------------------------
    def from_dict(self, map_item, path_root = tuple()):
        """
        Load Bureau from a nested dict.

        """
        return self.from_tuple(path_root = path_root,
                               tup_kv    = walkobj(obj      = map_item,
                                                   gen_leaf = True,
                                                   gen_path = True,
                                                   gen_obj  = True))

    # -------------------------------------------------------------------------
    def from_db(self, connection, path_root = tuple()):
        """
        Load data into the Bureau from the specified database.

        """

        (map_data, map_error) = load_from_db(filepath, str_format)
        if map_error is None:
            self.from_dict(path_root = path_root,
                           map_item  = map_data)

    # -------------------------------------------------------------------------
    def to_db(self, connection):
        """
        Save data from the Bureau to the specified database.

        """

        save_to_db(self.to_dict(), connection)

    # -------------------------------------------------------------------------
    def from_file(self, filepath, str_format = None, path_root = tuple()):
        """
        Load data into the Bureau from the specified file.

        """

        (map_data, map_error) = load_from_filepath(filepath, str_format)
        if map_error is None:
            self.from_dict(path_root = path_root,
                           map_item  = map_data)

    # -------------------------------------------------------------------------
    def to_file(self, filepath, str_format = None):
        """
        Save data from the Bureau to the specified file.

        """

        save_to_filepath(self.to_dict(), filepath, str_format)

    # -------------------------------------------------------------------------
    def pprint(self):
        """
        Pretty print the bureau.

        """
        pprint.pprint(self.to_dict())

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Gets the value for the specified key.

        """

        return self._bureau_engine.get_item(path = self._tup_full_path(key))

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """
        Sets a key-value pair.

        """

        self._bureau_engine.set_item(path      = self._tup_full_path(key),
                                     value_new = value)

        return None

    # -------------------------------------------------------------------------
    def __delitem__(self, key):
        """
        Delete the specified key.

        """

        self._bureau_engine.del_item(path = self._tup_full_path(key))

        return None

    # -------------------------------------------------------------------------
    def __iter__(self):
        """
        Return an iterator over elements in the Bureau.

        """

        return self._bureau_data.__iter__()

    # -------------------------------------------------------------------------
    def __len__(self):
        """
        Return the number of elements in the Bureau.

        """

        return self._bureau_data.__len__()

    # -------------------------------------------------------------------------
    def __setattr__(self, key, value):
        """
        Sets a key-value pair.

        """

        if key in Bureau._bureau_attributes:
            super().__setattr__(key, value)
        else:
            self.__setitem__(key, value)

        return None

    # -------------------------------------------------------------------------
    def __getattr__(self, key):
        """
        Gets the value for the specified key.

        """

        return self.__getitem__(key)

    # -------------------------------------------------------------------------
    def __str__(self):
        """
        Return a string representation of the Bureau.

        """
        list_kv = list()
        for (key, value) in self._bureau_data.items():

            if isinstance(key, str):
                key = repr(key)
            else:
                key = str(key)

            if isinstance(value, str):
                value = repr(value)
            else:
                value = str(value)

            list_kv.append('{k}: {v}'.format(k = key, v = value))

        return '{' + ', '.join(list_kv) + '}'

    # -------------------------------------------------------------------------
    def undo(self):
        """
        Undo the last edit in the bureau engine edit history.

        """

        return self._bureau_engine.undo()

    # -------------------------------------------------------------------------
    def redo(self):
        """
        Redo the last undo in the bureau engine undo history.

        """

        return self._bureau_engine.redo()

    # -------------------------------------------------------------------------
    def add_rule(self,
                 rule      = None,
                 condition = None,
                 action    = None,
                 tup_path  = None):
        """
        Add a rule to the bureau engine.

        """

        if tup_path is None:
            tup_path = self._bureau_path

        return self._bureau_engine.add_rule(rule      = rule,
                                            condition = condition,
                                            action    = action,
                                            tup_path  = tup_path)

    # -------------------------------------------------------------------------
    def _tup_full_path(self, key):
        """
        Return the full path to the specified key as a tuple.

        """

        iter_branch = _iter_path(key, self._bureau_path_delimiter)

        return self._bureau_path + tuple(iter_branch)

    # -------------------------------------------------------------------------
    @contextlib.contextmanager
    def batch_context(self):
        """
        Context manager for processing updates as a batch.

        """
        self._bureau_engine._journal.clear()
        self._bureau_engine._do_keep_journal = True
        batch = list()

        try:

            yield batch

        except Exception as err:

            pass # We might want to rollback changes here if there is a need.

        finally:

            self._bureau_engine._do_keep_journal = False
            batch[:] = self._bureau_engine._journal

            self._bureau_engine._invoke_rules(batch)

            self._bureau_engine._journal.clear()

    # -------------------------------------------------------------------------
    def from_batch(self, batch):
        """
        Update the Bureau using the specified journal segment.

        """
        for tup_cmd in batch:
            cmd = Command._make(tup_cmd)
            self._bureau_engine.set_item(path      = cmd.path,
                                         value_new = cmd.value_new,
                                         operation = cmd.operation)

# =============================================================================
class BureauEngine():
    """
    An engine to help run a tree of Bureau objects.

    """

    # -------------------------------------------------------------------------
    def __init__(self, bureau):
        """
        Returns a new BureauEngine instance.

        """

        self._bureau          = bureau
        self._do_keep_journal = False
        self._journal         = list()
        self._cmd_counter     = 0
        self._hist_edit       = list()
        self._hist_undo       = list()
        self._list_rule       = list()

    # -------------------------------------------------------------------------
    def get_item(self, path):
        """
        Getter implementation.

        """

        # Resolve path.
        #
        cursor      = self._bureau._bureau_data
        path_cursor = tuple()
        for name in _iter_path(path, self._bureau._bureau_path_delimiter):
            path_cursor = path_cursor + (name,)
            cursor      = self._ensure_exists(path_cursor, cursor, name)

        # Invalid path raise KeyError.
        #
        if cursor is self._bureau._bureau_data:
            raise KeyError(repr(path))

        return cursor

    # -------------------------------------------------------------------------
    def del_item(self, path):
        """
        Deleter implementation.

        """

        self.set_item(path = path, value_new = None, operation = 'del')
        return None

    # -------------------------------------------------------------------------
    def set_item(self, path, value_new, operation = 'edit'):
        """
        Setter implementation.

        """

        self._hist_edit.append(
                    self._do_update_and_bookkeeping(
                                    Command(operation = operation,
                                            path      = path,
                                            value_new = value_new,
                                            value_old = None)))
        return None

    # -------------------------------------------------------------------------
    def undo(self):
        """
        Get the last edit, reverse it, and store in the undo history.

        """

        if not self._hist_edit:
            return None

        cmd_edit = self._hist_edit.pop()
        self._hist_undo.append(
                    self._do_update_and_bookkeeping(
                                    Command(operation = 'undo',
                                            path      = cmd_edit.path,
                                            value_new = cmd_edit.value_old,
                                            value_old = cmd_edit.value_new)))
        return None

    # -------------------------------------------------------------------------
    def redo(self):
        """
        Get the last undo, reverse it, and store in the edit history.

        """

        if not self._hist_undo:
            return None

        cmd_undo = self._hist_undo.pop()
        self._hist_edit.append(
                    self._do_update_and_bookkeeping(
                                    Command(operation = 'redo',
                                            path      = cmd_undo.path,
                                            value_new = cmd_undo.value_old,
                                            value_old = cmd_undo.value_new)))
        return None

    # -------------------------------------------------------------------------
    def _do_update_and_bookkeeping(self, cmd):
        """
        Sets a new value in the specified bureau and returns the old value.

        Also performs book-keeping tasks such as
        updating the and journal command counter.

        """
        time_utc  = time.time()
        value_old = self._do_update(cmd.path, cmd.value_new)
        if cmd.operation == 'del':
            self._bureau_data.__delitem__(key)

        self._cmd_counter += 1
        idx_cmd = self._cmd_counter - 1

        cmd = Command(operation = cmd.operation,
                      idx       = idx_cmd,
                      time_utc  = time_utc,
                      path      = cmd.path,
                      value_new = cmd.value_new,
                      value_old = value_old)

        if self._do_keep_journal:
           self._journal.append(cmd)

        return cmd

    # -------------------------------------------------------------------------
    def _do_update(self, tup_path, value_new):
        """
        Sets a new value in the specified bureau and returns the old value.

        This function implements the functionality
        of setting a new value at a specified path
        in the data structure.

        This method updates the value at the
        specified path in the bureau's data
        structure with a new value.

        The old value at the specified path is
        returned. If there is no old value (the
        path was not previously in the data
        structure), then None is returned.

        If there are any callbacks associated
        with the specified path, they are invoked
        with the old and new values as arguments.

        :param tup_path:    A tuple representing the path in the bureau's
                            data structure where the new value is to be set.
                            Each item in the tuple is a key in the data
                            structure, and the sequence of keys represents
                            the path to  the value.

        :param value_new:   The new value to be set at the specified path
                            in the bureau's data structure.

        :returns:           The old value at the specified path, or None
                            if there was no old value.

        :raises KeyError:   If the specified path is not valid (it is an
                            empty tuple).

        :note:              The method uses the _ensure_exists method to
                            get or create the bureau at each step along the
                            specified path. It uses the _accessor_functions
                            function to get the getter and setter methods
                            for the bureau's data structure.

        """

        # Resolve path-like keys.
        #
        cursor      = self._bureau._bureau_data
        path_cursor = tuple()
        for name in tup_path[:-1]:
            path_cursor += (name,)
            cursor      = self._ensure_exists(path_cursor, cursor, name)

        # Invalid keys raise KeyError.
        #
        try:
            name = tup_path[-1]
        except IndexError:
            raise KeyError(repr(tup_path))

        # Resolve the final element of a path-like
        # key (or the whole key if it is atomic).
        #
        path_cursor += (name,)

        # Avoid recursion and get the old value.
        #
        (get_item, set_item) = _accessor_functions(cursor)
        if name in tuple(cursor.keys()):  # NUST BE tuple(cursor.keys())
            value_old    = get_item(name)
            is_recursive = (value_old is value_new)
            if is_recursive:
                return value_old
        else:
            value_old = None

        # Apply the change.
        #
        set_item(name, value_new)
        return value_old

    # -------------------------------------------------------------------------
    def _ensure_exists(self, tup_path_cursor, cursor, name):
        """
        Return the named item in cursor, or create as a Bureau if not present.

        This function tries to return a named
        item in a given cursor. If the item does
        not exist, it creates a new Bureau object
        and assigns it to the specified name in
        the cursor.

        The function uses the _accessor_functions
        function to get the getter and setter
        methods for the current cursor, and uses
        these methods to get and set items in the
        cursor.

        """

        (get_item, set_item) = _accessor_functions(cursor)
        try:
            cursor = get_item(name)
        except KeyError:
            bureau_new = Bureau(engine = self,
                                path   = tup_path_cursor)
            set_item(name, bureau_new)
            cursor = bureau_new

        return cursor

    # -------------------------------------------------------------------------
    def add_rule(self,
                 rule      = None,
                 condition = None,
                 action    = None,
                 tup_path  = None):
        """
        Add a rule.

        """
        has_rule      = rule      is not None
        has_condition = condition is not None
        has_action    = action    is not None
        has_tup_path  = tup_path  is not None

        if has_rule:

            if (has_condition) or (has_action):
                raise ValueError((
                    'If a rule is specified, then'
                    'no additional condition or'
                    'action may be specified.'))

        else:

            if (not has_condition) or (not has_action):
                raise ValueError((
                    'If no rule is specified, then'
                    'a condition and an action must'
                    'be specified instead.'))

            # Ensure condition wrapped in tuple
            if callable(condition):
                condition = (condition,)

            rule = Rule(condition = condition,
                        action    = action)

        # Add an indicator function to the rule's
        # conditions to select only commands that
        # affect the specified path.
        #
        if has_tup_path:

            indicator = functools.partial(_is_match_path,
                                          tup_path = tup_path)
            rule = Rule(condition = (indicator,) + rule.condition,
                        action    = rule.action)

        self._list_rule.append(rule)

        return None

    # -------------------------------------------------------------------------
    def _invoke_rules(self, batch):
        """
        Invoke rules for the specified batch of commands.

        """
        list_cmd = list()
        for rule in self._list_rule:

            # If one or more commands in the
            # batch meet all of the current
            # rule's conditions, then the rule's
            # action is invoked.
            #
            list_cmd.clear()
            list_cmd[:] = batch

            for indicator in rule.condition:
                if not list_cmd:
                    break
                list_cmd[:] = (cmd for cmd in list_cmd if indicator(cmd = cmd))

            if not list_cmd:
                continue

            rule.action(self._bureau, list_cmd)

        return None

# -----------------------------------------------------------------------------
def _is_match_path(tup_path, cmd):
    """
    """
    return cmd.path[:len(tup_path)] == tup_path

# -----------------------------------------------------------------------------
def _accessor_functions(item):
    """
    Return getter and setter methods for the specified object.

    This function returns the getter and setter
    methods for a specified object. If the object
    is an instance of Bureau, it uses the getter
    and setter methods of the _bureau_data
    attribute.

    If the object is not an instance of Bureau,
    it uses the built-in getter and setter
    methods.

    """

    if isinstance(item, Bureau):

        get_item = item._bureau_data.__getitem__
        set_item = item._bureau_data.__setitem__

    else:

        get_item = item.__getitem__
        set_item = item.__setitem__

    return (get_item, set_item)


# -----------------------------------------------------------------------------
def _iter_path(path, delim):
    """
    Yield each item in path.

    This function returns a generator that yields
    each item in a given path. The path can be a
    string, an iterable, or an atomic (non-string,
    non-iterable) value.

    If the path is a string, it is split by a
    specified delimiter, and each item is yielded.

    If the item can be converted to an integer,
    it is yielded as an integer; otherwise, it
    is yielded as a string.

    If the path is an iterable (but not a string),
    each item in the iterable is yielded.

    If the path is an atomic value (neither a
    string nor an iterable), it is yielded as is.

    """

    # If the path is a string, split by the
    # delimiter and yield each item in turn.
    #
    try:
        for item in path.split(delim):
            try:
                yield int(item)  # Support for indices into lists.
            except ValueError:
                yield item

    # If the path is not a string (it doesn't
    # have the split method), it treats it as
    # an iterable.
    #
    except AttributeError:
        try:
            for item in path:
                yield item

        # If the path is not an iterable either,
        # it treats it as an atomic value and
        # yields it as-is.
        #
        except TypeError:
            yield path


# =============================================================================
class DotDict(dict):
    """
    Custom dictionary with dot notation attribute access.

    """

    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


# -----------------------------------------------------------------------------
def coroutine(fun):
    """
    Return a decorator function that primes communications with a coroutine.

    ---
    type:   function
    ...

    """

    def primed(*args, **kwargs):
        """
        Wrapper for coroutines that 'primes' it by sending the first message.

        ---
        type:   function
        ...

        """
        coro = fun(*args, **kwargs)
        coro.send(None)
        return coro

    return primed


# -----------------------------------------------------------------------------
def walkobj(obj:         typing.Any,              # pylint: disable=R0912,R0913
            gen_leaf:    bool                 = False,
            gen_nonleaf: bool                 = False,
            gen_path:    bool                 = False,
            gen_obj:     bool                 = False,
            path:        typing.Tuple         = (),
            memo:        typing.Optional[set] = None) -> typing.Iterator[
                                                            typing.Union[
                                                                typing.Tuple,
                                                                typing.Any]]:
    """
    Generate depth-first traversal over tree of mappings and other iterables.

    This function performs a depth-first,
    left-to-right recursive traversal over
    the provided data structure, which is
    assumed to consist of a finite, treelike
    arrangement of nested collections.Mapping
    and collections.Iterable types.

    The function can be configured to yield
    information about nodes in the tree:
    leaf nodes, non-leaf (internal) nodes,
    or both. Additionally, the information
    yielded can be configured to include
    the path to the node and/or the object
    at the node itself.

    Adapted from:

        {http://code.activestate.com/recipes/577982-recursively-walk-python-objects/}

    Parameters:

        obj (object):                   The object to be traversed.

        gen_leaf (bool, optional):      If True, leaf nodes will be generated.
                                        Default is False.

        gen_nonleaf (bool, optional):   If True, non-leaf nodes will be
                                        generated. Default is False.

        gen_path (bool, optional):      If True, the path to the node will be
                                        generated. Default is False.

        gen_obj (bool, optional):       If True, the object at the node will
                                        be generated. Default is False.

        path (tuple, optional):         A tuple representing the path to the
                                        current node. Default is an empty tuple.

        memo (set, optional):           A set used to track visited objects to
                                        avoid infinite recursion.

    Yields:

        tuple or object:                The configured information for each
                                        node in the traversal.

    Examples:

        >>> data = {'a': 1, 'b': {'c': 2, 'd': [3, 4]}}
        >>> list(walkobj(data, gen_leaf=True, gen_path=True))
        [(('a',), 1), (('b', 'c'), 2), (('b', 'd', 0), 3), (('b', 'd', 1), 4)]

    ---
    type:   generator
    ...

    """
    # If the object is elemental, it cannot be
    # decomposed, so we must bottom out the
    # recursion and yield the object and its'
    # path before returning control back up
    # the stack.
    #
    is_itable    = isinstance(obj, collections.abc.Iterable)
    is_leaf      = (not is_itable) or is_string(obj)

    if is_leaf:
        if gen_leaf:
            if gen_path and gen_obj:
                yield (path, obj)
            elif gen_path:
                yield path
            elif gen_obj:
                yield obj
        return

    # Since this is a recursive function, we need
    # to be on our guard against any references
    # to objects back up the call stack (closer
    # to the root of the tree). Any such
    # references would be circular, leading to
    # an infinite tree, and causing us to blow
    # our stack in a fit of unbounded recursion.
    #
    # If we detect that we've already visited
    # this object (using identity not equality),
    # then the safe thing to do is to halt the
    # recursive descent and return control back
    # up the stack.
    #
    _id = id(obj)
    if memo is None:
        memo = set()
    if _id in memo:
        return
    memo.add(_id)

    # If the object is not elemental (i.e. it is
    # an Iterable), then it may be decomposed, so
    # we should recurse down into each component,
    # yielding the results as we go. Of course,
    # we need different iteration functions for
    # mappings vs. other iterables.
    #
    def mapiter(mapping):
        """
        Return an iterator over the specified mapping or other iterable.

        This function selects the appropriate
        iteration function to use.

        """
        return getattr(mapping, 'items', mapping.items)()
    itfcn = mapiter if isinstance(obj, collections.abc.Mapping) else enumerate

    for pathpart, component in itfcn(obj):

        childpath = path + (pathpart,)
        if gen_nonleaf:
            if gen_path and gen_obj:
                yield (childpath, component)
            elif gen_path:
                yield childpath
            elif gen_obj:
                yield component

        for result in walkobj(obj         = component,
                              gen_leaf    = gen_leaf,
                              gen_nonleaf = gen_nonleaf,
                              gen_path    = gen_path,
                              gen_obj     = gen_obj,
                              path        = childpath,
                              memo        = memo):
            yield result

    # We only need to guard against infinite
    # recursion within a branch of the call-tree.
    # There is no danger in visiting the same item
    # instance in sibling branches, so we can
    # forget about objects once we are done
    # with them and about to pop the stack.
    #
    memo.remove(_id)

    return


# -----------------------------------------------------------------------------
def save_to_filepath(map_data, filepath, str_format = None):
    """
    Write the specified dict to the specified file in the specified format.

    """

    if str_format is None:
        (_, str_ext) = os.path.splitext(filepath)
        str_format   = str_ext[1:]

    if str_format == 'pickle':
        filemode = 'wb'
    else:
        filemode = 'wt'

    (serial_data, map_error) = serialize(map_data, str_format)

    if serial_data is not None:
        with open(filepath, filemode) as file:
            file.write(serial_data)

    return map_error


# -----------------------------------------------------------------------------
def load_from_filepath(filepath, str_format = None):
    """
    Return data loaded from the specified file as a dict.

    """

    if str_format is None:
        (_, str_ext) = os.path.splitext(filepath)
        str_format   = str_ext[1:]

    if str_format == 'pickle':
        filemode = 'rb'
    else:
        filemode = 'rt'

    with open(filepath, filemode) as file:
        serial_data = file.read()

    (map_data, map_error) = deserialize(serial_data, str_format)

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize(map_data, str_format):
    """
    Return the specified data as a serialised string in the specified format.

    """

    lut = dict(pickle = serialize_to_pickle_bytes,
               pkl    = serialize_to_pickle_bytes,
               xml    = serialize_to_xml_string,
               json   = serialize_to_json_string,
               toml   = serialize_to_toml_string,
               yaml   = serialize_to_yaml_string,
               yml    = serialize_to_yaml_string)
    return lut[str_format](map_data)


# -----------------------------------------------------------------------------
def deserialize(str_data, str_format):
    """
    Return the data encoded in the the specified string as a dict.

    """

    lut = dict(pickle = deserialize_from_pickle_bytes,
               pkl    = deserialize_from_pickle_bytes,
               xml    = deserialize_from_xml_string,
               json   = deserialize_from_json_string,
               toml   = deserialize_from_toml_string,
               yaml   = deserialize_from_yaml_string,
               yml    = deserialize_from_yaml_string)
    return lut[str_format](str_data)


# -----------------------------------------------------------------------------
def serialize_to_pickle_bytes(map_data):
    """
    Return the specified data as pickled bytes.

    """

    import pickle # pylint: disable=C0415

    bytes_pickle = None
    map_error    = None

    try:

        bytes_pickle = pickle.dumps(obj             = map_data,
                                    protocol        = pickle.DEFAULT_PROTOCOL,
                                    fix_imports     = False,
                                    buffer_callback = None)

    except pickle.PicklingError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    return (bytes_pickle, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_pickle_bytes(bytes_pickle):
    """
    Return the data encoded in the the specified pickled bytes as a dict.

    """

    import pickle # pylint: disable=C0415

    map_data  = None
    map_error = None

    try:

        map_data = pickle.loads(bytes_pickle,
                                fix_imports = False)

    except pickle.UnpicklingError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    return (map_data, map_error)



# -----------------------------------------------------------------------------
def serialize_to_xml_string(map_data):
    """
    Return the specified data as an XML string.

    """

    import xmltodict # pylint: disable=C0415

    str_xml   = None
    map_error = None

    if len(map_data) > 1:
        map_data = dict(root = map_data)

    try:

        str_xml = xmltodict.unparse(input_dict = map_data,
                                    encoding = 'utf-8',
                                    pretty     = True,
                                    newl       = '\n'.format(),
                                    indent     = '  ')

    except TypeError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_xml = str_xml.strip()

    return (str_xml, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_xml_string(str_xml):
    """
    Return the data encoded in the the specified XML string as a dict.

    """

    import xmltodict          # pylint: disable=C0415
    import xml.parsers.expat  # pylint: disable=C0415

    map_data  = None
    map_error = None

    str_xml = str_xml.strip()

    # -------------------------------------------------------------------------
    def _postproc(path, key, value):
        """
        """
        tup_ctor_type = (int, float)
        for ctor_type in tup_ctor_type:
            try:
                value = ctor_type(value)
            except (ValueError, TypeError):
                continue
            else:
                break
        return (key, value)

    try:

        map_data = xmltodict.parse(str_xml,
                                   encoding      = 'utf-8',
                                   xml_attribs   = False,
                                   postprocessor = _postproc)

    except xml.parsers.expat.ExpatError as err:

        map_error = dict(exception = err,
                         message   = str(err),
                         idx_line  = err.lineno - 1,
                         idx_col   = err.offset)

    else:

        if tuple(map_data.keys()) == ('root',):
            map_data = map_data['root']

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize_to_json_string(map_data):
    """
    Return the specified data as a JSON string.

    """

    import json  # pylint: disable=C0415

    str_json  = None
    map_error = None

    try:

        str_json = json.dumps(map_data, indent = 2)

    except TypeError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_json = str_json.strip()

    return (str_json, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_json_string(str_json):
    """
    Return the data encoded in the the specified JSON string.

    """

    import json  # pylint: disable=C0415

    map_data  = None
    map_error = None

    # Remove comment lines.
    #
    list_str_line = []
    for str_line in str_json.strip().splitlines():
        str_line_naked = str_line.strip()
        if str_line_naked.startswith('//') or str_line_naked.startswith('#'):
            continue
        list_str_line.append(str_line)
    str_json = ''.join(list_str_line)

    try:

        map_data = json.loads(str_json)

    except json.JSONDecodeError as err:

        map_error = dict(exception      = err,
                         message        = str(err),
                         idx_char_start = err.pos)

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize_to_toml_string(map_data):
    """
    Return the specified data as a TOML string.

    """

    import toml  # pylint: disable=C0415

    str_toml  = None
    map_error = None

    try:

        str_toml = toml.dumps(map_data)

    except TypeError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_toml = str_toml.strip()

    return (str_toml, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_toml_string(str_toml):
    """
    Return the data encoded in the specified TOML string.

    """

    import toml  # pylint: disable=C0415

    map_data  = None
    map_error = None

    str_toml  = str_toml.strip()

    try:

        map_data = toml.loads(str_toml)

    except toml.TomlDecodeError as err:

        map_error = dict(exception      = err,
                         message        = err.msg,
                         idx_char_start = err.pos,
                         idx_line       = err.lineno - 1,
                         idx_col        = err.colno)

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def serialize_to_yaml_string(map_data):
    """
    Return the specified data as a YAML string.

    """

    import yaml  # pylint: disable=C0415

    str_yaml  = None
    map_error = None

    try:

        str_yaml = yaml.dump(map_data, default_flow_style = False)

    except yaml.YAMLError as err:

        map_error = dict(exception = err,
                         message   = str(err))

    else:

        str_yaml = str_yaml.strip()
        #str_yaml = _reindent_yaml(str_yaml)

    return (str_yaml, map_error)


# -----------------------------------------------------------------------------
def deserialize_from_yaml_string(str_yaml):
    """
    Return the data encoded in the specified YAML string.

    """

    import yaml  # pylint: disable=C0415

    map_data  = None
    map_error = None

    loader = yaml.SafeLoader
    yaml.add_constructor('!regex',
                         lambda l, n: str(n.value),
                         Loader = loader)

    str_yaml = str_yaml.strip()

    try:

        map_data = yaml.load(str_yaml, Loader = loader)

    except yaml.YAMLError as err:

        map_error = dict(exception = err,
                         message   = str(err))

        if hasattr(err, 'problem_mark'):
            mark = err.problem_mark
            map_error['idx_line'] = mark.line
            map_error['idx_col']  = mark.column

    return (map_data, map_error)


# -----------------------------------------------------------------------------
def resolve(value):
    """
    Ensure that the provided value is fully resolved.

    If the provided value is a string starting
    with the prefix '_spec::' then resolve it
    to the actual value.

    """
    if not is_string(value):
        return value

    prefix = '_spec::'
    if not value.startswith(prefix):
        return value

    (name_module, name_attrib) = value[len(prefix):].rsplit('.', 1)
    return getattr(importlib.import_module(name_module), name_attrib)


# -----------------------------------------------------------------------------
def is_string(obj):
    """
    Return true if obj is a string. Works in Python 2 and Python 3.

    """

    return isinstance(obj, string_types())


# -----------------------------------------------------------------------------
def string_types():
    """
    Return the string types for the current Python version.

    """

    is_python_2 = str is bytes
    if is_python_2:  # pylint: disable=R1705

        return (str, unicode)  # pylint: disable=E0602

    else:

        return (str, bytes)