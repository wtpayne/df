


# =============================================================================
class PathDict(collections.UserDict):  # pylint: disable=R0901
    """
    Custom dictionary class supporting path-tuple based access.

    """

    # -------------------------------------------------------------------------
    def __init__(self, *args, **kwargs):
        """
        Return a PathDict instance.

        """
        self.delim = '.'
        super().__init__(*args, **kwargs)

    # -------------------------------------------------------------------------
    def __getitem__(self, key):
        """
        Return a reference to the specified item in data.

        """
        reference = self.data
        for name in _ensure_list(key, delim = self.delim):
            reference = reference[name]
        return reference

    # -------------------------------------------------------------------------
    def __setitem__(self, key, value):
        """
        Return a reference to the specified item in data.

        """
        reference = self.data

        # If we want to disable string
        # to list conversion, we can
        # set delim to None.
        #
        if self.delim is not None:
            key = _ensure_list(key, delim = self.delim)

        reference = self.data
        for name in key[:-1]:
            if name not in reference:
                reference[name] = dict()
            reference = reference[name]
        if key:
            reference[key[-1]] = value
        else:
            reference = value




# =============================================================================
# class LiveMap(collections.abc.MutableMapping):
#     """
#     A dict-like class that can invokes callbacks when values are changed.

#     This class can be used to implement data
#     binding between UI views and view models,
#     or between any set of data models in the
#     applicaiton.

#     """

#     # Instance private attributes
#     # are given special handling
#     # so they don't get treated
#     # as regular keys.
#     #
#     _lm_attributes = ('_lm_path',
#                       '_lm_journal',
#                       '_lm_data',
#                       '_lm_map_key_callback',
#                       '_lm_list_global_callback')

#     # ------------------------------------------------------------------------
#     def __init__(self, path = None, journal = None):
#         """
#         Returns a new LiveMap instance.

#         """
#         if journal is None:
#             journal = CommandJournal()

#         # The underlying datastore.
#         self._lm_data = dict()

#         # Dot delimited path to self.
#         self._lm_path = path

#         # Stores commands to support undo,
#         # redo functionality as well as
#         # remote synchronization.
#         #
#         self._lm_journal = journal

#         # List of callbacks to be invoked when
#         # a specific key is mutated.
#         #
#         self._lm_map_key_callback = collections.defaultdict(list)

#         # List of callbacks to be invoked on
#         # every change.
#         #
#         self._lm_list_global_callback = list()

#     # ------------------------------------------------------------------------
#     def _set(self, key, value):
#         """
#         Setter implemnetation.

#         Calls self._invoke() if the value changes.

#         """
#         # TODO: ADD COMMAND TO JOURNAL

#         has_key = (key in self._lm_data.keys())
#         if has_key:
#             is_same_value = (self._lm_data[key] == value)
#             if is_same_value:
#                 return  # Avoid recursion

#         # If we are adding a LiveMap, ensure
#         # that we get invoked if it changes.
#         #
#         # TODO: BUILD PATH AND SET IT IN VALUE
#         #
#         if isinstance(value, LiveMap):
#             value.add_callback(
#                     callback = functools.partial(self._invoke, key = key))

#         # TODO: USE COMMAND TO CHANGE VALUE
#         self._lm_data[key] = value
#         self._invoke(value = value, key = key)

#     # ------------------------------------------------------------------------
#     def _get(self, key):
#         """
#         """
#         try:
#             return self._lm_data[key]
#         except KeyError:

#             # Create a new LiveMap, making sure
#             # that callback invocations bubble back
#             # up to the root.
#             #
#             new_dict = LiveMap(is_root = False)
#             new_dict.add_callback(
#                         lambda value: self._invoke(value = value, key = key))
#             self._set(key = key, value = new_dict)
#             return new_dict

#     # ------------------------------------------------------------------------
#     def __str__(self):
#         """
#         Return a string representation of the LiveMap.

#         """
#         str_kv = ', '.join(('{0}: {1}'.format(str(k), str(v))
#                                         for (k, v) in self._lm_data.items()))
#         return '{' + str_kv + '}'

#     # ------------------------------------------------------------------------
#     def __getitem__(self, key):
#         """
#         Gets the value for the specified key.

#         """
#         self._get(key)

#     # ------------------------------------------------------------------------
#     def __setitem__(self, key, value):
#         """
#         Sets a key-value pair and invokes relevant callbacks.

#         """
#         self._set(key, value)

#     # ------------------------------------------------------------------------
#     def __delitem__(self, key):
#         """
#         Delete the specified key.

#         """
#         return self._lm_data.__delitem__(key)

#     # ------------------------------------------------------------------------
#     def __iter__(self):
#         """
#         Return an iterator over elements in the LiveMap.

#         """
#         return self._lm_data.__iter__()

#     # ------------------------------------------------------------------------
#     def __len__(self):
#         """
#         Return the number of elements in the LiveMap.

#         """
#         return self._lm_data.__len__()

#     # ------------------------------------------------------------------------
#     def __setattr__(self, key, value):
#         """
#         Sets a key-value pair and invokes relevant callbacks.

#         """
#         if key in LiveMap._lm_attributes:
#             super().__setattr__(key, value)
#         else:
#             self._set(key, value)

#     # ------------------------------------------------------------------------
#     def __getattr__(self, key):
#         """
#         Gets the value for the specified key.

#         """
#         return self._get(key)

#     # ------------------------------------------------------------------------
#     def add_callback(self, callback, key = None):
#         """
#         Add a callback to be invoked when something changes.

#         If a key is specified, then the callback
#         will only be invoked when the corresponding
#         data item changes.

#         """
#         if not callable(callback):
#             raise ValueError("Callback must be a callable")

#         if key is None:
#             self._add_global_callback(callback)
#         else:
#             self._add_callback_for_key(key, callback)

#     # ------------------------------------------------------------------------
#     def _add_callback_for_key(self, key, callback):
#         """
#         Add a callback to be invoked each time dict[key] changes.

#         """
#         self._lm_map_key_callback[key].append(callback)

#     # ------------------------------------------------------------------------
#     def _add_global_callback(self, callback):
#         """
#         Add a callback to be invoked each time anything in the dict changes.

#         """
#         self._lm_list_global_callback.append(callback)

#     # ------------------------------------------------------------------------
#     def _invoke(self, value, key = None):
#         """
#         Invoke callbacks.

#         If key is not specified or is None then only
#         the global callbacks will be invoked.

#         Otherwise both the global callbacks and those
#         for key will be invoked.

#         """
#         try:
#             for callback in self._lm_map_key_callback[key]:
#                 callback(value)
#         except KeyError:
#             pass
#         for callback in self._lm_list_global_callback:
#             callback(self)


# # =============================================================================
# class Command:
#     """
#     """

#     # ------------------------------------------------------------------------
#     def __init__(self, key, value_old, value_new):
#         """
#         """
#         self._key       = key
#         self._value_old = value_old
#         self._value_new = value_new

#     # ------------------------------------------------------------------------
#     def exec():
#         """
#         """
#         self.obj[self._key] = self._value_new

#     # ------------------------------------------------------------------------
#     def undo():
#         """
#         """
#         self.obj[self._key] = self._value_old


# # =============================================================================
# class CommandJournal:
#     """
#     Stores, routes and executes commands.

#     """

#     # ------------------------------------------------------------------------
#     def __init__(self):
#         """
#         """
#         self._list_commands = list()