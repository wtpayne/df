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
import functools
import itertools
import string
import typing


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

        TODO: Consider removing callbacks from _do_update. OR MOVE JOURNAL IN THERE?
        TODO: Design mechanism for binding to other Bureau trees.
        TODO: Support for remote sync (Load/update from journal)
        TODO: Handle clearing down the journal.

        TODO: Save/Load to/from JSON/YAML/XML/SQLITE
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
    def add_callback(self, key, callback):
        """
        Add a callback function for the specified key.

        """

        return self._bureau_engine.add_callback(
                                        tup_path = self._tup_full_path(key),
                                        callback = callback)

    # -------------------------------------------------------------------------
    def as_key_value_tuple(self):
        """
        Return a representation of self as a key-value tuple.

        """

        return tuple(walkobj(obj      = self,
                             gen_leaf = True,
                             gen_path = True,
                             gen_obj  = True))

    # -------------------------------------------------------------------------
    def as_nested_dict(self):
        """
        Return a representation of self as a nested dict.

        This function converts the current Bureau
        instance into a nested dictionary
        representation.

        This method traverses the object using
        the `walkobj` utility function (via the
        as_key_value_tuple method), which
        generates length-2 tuples where the
        first element is a path indicating a
        location in the Bureau and the second
        element is the value at that path.

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

        for (tup_path, value) in sorted(self.as_key_value_tuple(),
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
    def journal(self):
        """
        Return the journal.

        """

        return self._bureau_engine._journal


    # -------------------------------------------------------------------------
    def _tup_full_path(self, key):
        """
        Return the full path to the specified key as a tuple.

        """

        iter_branch = _iter_path(key, self._bureau_path_delimiter)

        return self._bureau_path + tuple(iter_branch)


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

        self._bureau         = bureau
        self._journal        = list()
        self._hist_edit      = list()
        self._hist_undo      = list()
        self._list_callback  = list()  # Global callbacks.
        self._map_callback   = dict()  # Callbacks specific to a key.

    # -------------------------------------------------------------------------
    def add_callback(self, tup_path, callback):
        """
        Add a callback function for the specified key.

        """

        if tup_path not in self._map_callback:
            self._map_callback[tup_path] = list()
        self._map_callback[tup_path].append(callback)

        return None

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
                            BureauEngineCommand(operation = operation,
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
                                    BureauEngineCommand(
                                            operation = 'undo',
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
                                    BureauEngineCommand(
                                            operation = 'redo',
                                            path      = cmd_undo.path,
                                            value_new = cmd_undo.value_old,
                                            value_old = cmd_undo.value_new)))
        return None

    # -------------------------------------------------------------------------
    def _do_update_and_bookkeeping(self, cmd):
        """
        Sets a new value in the specified bureau and returns the old value.

        Also performs book-keeping tasks such as
        invoking related callbacks, updating
        the journal etc...

        """
        value_old = self._do_update(cmd.path, cmd.value_new)
        if cmd.operation == 'del':
            self._bureau_data.__delitem__(key)
        cmd = BureauEngineCommand(operation = cmd.operation,
                                  path      = cmd.path,
                                  value_new = cmd.value_new,
                                  value_old = value_old)
        self._invoke_callbacks(cmd)
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
    def _invoke_callbacks(self, cmd):
        """
        Invoke callbacks.

        """
        list_callback = list()
        list_callback.extend(self._list_callback)

        # Extend the calback list with
        # key-specific callbacks.
        #
        tup_path_part = tuple()
        for item in cmd.path:
            tup_path_part += (item,)
            if tup_path_part in self._map_callback:
                list_callback.extend(self._map_callback[tup_path_part])

        for callback in list_callback:
            callback(cmd)

        return None


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
BureauEngineCommand = collections.namedtuple(
        typename    = 'BureauEngineCommand',
        field_names = ('operation', 'path', 'value_new', 'value_old'),
        defaults    = ('edit',      '',     None,        None))


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
