# -*- coding: utf-8 -*-
"""
Memoization utility functions.

This function was originally from the ActiveState
recipe published at:

    http://code.activestate.com/recipes/578078/

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2013 Raymond Hettinger"

license:
    "Licensed under the MIT Expat license:

    Permission is hereby granted, free of charge, to any person
    obtaining a copy of this software and associated documentation
    files, (the Software), to deal in the Software without
    restriction, including without limitation the rights to use,
    copy, modify, merge, publish, distribute, sublicense, and or
    sell copies of the Software, and to permit persons to whom
    the Software is furnished to do so, subject to the following
    conditions:

    The above copyright notice and this permission notice shall be
    included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED AS IS, WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
    NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
    WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE."

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


import collections
import functools
import threading


_CacheInfo = collections.namedtuple(
                        "CacheInfo", ["hits", "misses", "maxsize", "currsize"])

# names for the stats fields
HITS   = 0
MISSES = 1

# names for the link fields
PREV   = 0
NEXT   = 1
KEY    = 2
RESULT = 3


# =============================================================================
class _HashedSeq(list):
    """
    Class used to generate a (key) hash from a sequence.

    """

    __slots__ = 'hashvalue'

    # -------------------------------------------------------------------------
    def __init__(self, tup, hash = hash):               # pylint: disable=W0231
        """
        Return an instantiated _HashedSeq object.

        """
        self[:] = tup
        self.hashvalue = hash(tup)

    # -------------------------------------------------------------------------
    def __hash__(self):
        """
        Return the hash value for the _HashedSeq object instance.

        ---
        type:   method
        ...

        """
        return self.hashvalue


# -----------------------------------------------------------------------------
def _make_key(                                    # pylint: disable=W0102,R0913
        args,
        kwds,
        typed,
        kwd_mark  = (object(),),
        fasttypes = {int, str, frozenset, type(None)},
        sorted    = sorted,
        tuple     = tuple,
        type      = type,
        len       = len):
    """
    Make a cache key from optionally typed positional and keyword arguments.

    ---
    type:   function
    ...

    """
    # The cache key is a hashed list of input
    # arguments and keyword arguments.
    #
    key = args

    if kwds:
        sorted_items = sorted(kwds.items())
        key += kwd_mark
        for item in sorted_items:
            key += item

    # Typenames can (optionally) be included
    # in the list also.
    #
    if typed:
        key += tuple(type(v) for v in args)
        if kwds:
            key += tuple(type(v) for k, v in sorted_items)

    # Don't bother computing a hash for the trivial
    # case where we have a single simple argument.
    #
    elif len(key) == 1 and type(key[0]) in fasttypes:
        return key[0]

    # The hashes are computed by the _HashedSeq
    # constructor.
    #
    return _HashedSeq(key)


# -----------------------------------------------------------------------------
def lru_cache(maxsize = 100, typed = False):
    """
    Least-recently-used cache decorator.

    If *maxsize* is set to None, the LRU features
    are disabled and the cache can grow without
    bound.

    If *typed* is True, arguments of different types
    will be cached separately. For example, f(3.0)
    and f(3) will be treated as distinct calls with
    distinct results.

    Arguments to the cached function must be hashable.

    View the cache statistics named tuple (hits,
    misses, maxsize, currsize) with f.cache_info().

    Clear the cache and statistics with f.cache_clear().
    Access the underlying function with f.__wrapped__.

    See:  http://en.wikipedia.org/wiki/Cache_algorithms#Least_Recently_Used

    Users should only access the lru_cache through
    its public API:

        * cache_info
        * cache_clear
        * f.__wrapped__

    The internals of the lru_cache are encapsulated
    for thread safety and to allow the implementation
    to change (including a possible C version).

    ---
    type:   function
    ...

    """
    # -------------------------------------------------------------------------
    def decorating_function(user_function):
        """
        Return a wrapped variant of the specified user_function.

        ---
        type:   function
        ...

        """
        cache = dict()

        # make statistics updateable non-locally
        stats     = [0, 0]
        make_key  = _make_key

        # bound method to lookup key or return None
        cache_get = cache.get

        # localize the global len() function
        _len      = len

        # because linkedlist updates aren't threadsafe
        lock      = threading.RLock()

        # root of the circular doubly linked list
        root      = []

        # initialize by pointing to self
        root[:]   = [root, root, None, None]

        # make updateable non-locally
        nonlocal_root = [root]

        if maxsize == 0:

            # -----------------------------------------------------------------
            def wrapper(*args, **kwds):
                """
                Call the wrapped function and return its result.

                No caching, just a statistics update
                after a successful call.

                ---
                type:   function
                ...

                """
                result = user_function(*args, **kwds)
                stats[MISSES] += 1
                return result

        elif maxsize is None:

            # -----------------------------------------------------------------
            def wrapper(*args, **kwds):
                """
                Call the wrapped function and return its result.

                Simple caching without ordering or
                size limit.

                ---
                type:   function
                ...

                """
                key = make_key(args, kwds, typed)

                # root used here as a unique not-found sentinel
                result = cache_get(key, root)
                if result is not root:
                    stats[HITS] += 1
                    return result
                result = user_function(*args, **kwds)
                cache[key] = result
                stats[MISSES] += 1
                return result

        else:

            # -----------------------------------------------------------------
            def wrapper(*args, **kwds):
                """
                Call the wrapped function and return its result.

                Size limited caching that tracks
                accesses by recency.

                ---
                type:   function
                ...

                """
                key = make_key(args, kwds, typed) if kwds or typed else args

                with lock:
                    link = cache_get(key)
                    if link is not None:

                        # Record recent use of the key
                        # by moving it to the front of
                        # the list
                        #
                        root,           = nonlocal_root
                        link_prev, link_next, key, result = link
                        link_prev[NEXT] = link_next
                        link_next[PREV] = link_prev
                        last            = root[PREV]
                        last[NEXT]      = root[PREV] = link
                        link[PREV]      = last
                        link[NEXT]      = root
                        stats[HITS] += 1
                        return result

                result = user_function(*args, **kwds)

                with lock:
                    root, = nonlocal_root
                    if key in cache:

                        # getting here means that this same key
                        # was added to the cache while the lock
                        # was released.  Since the link update
                        # is already done, we need only return
                        # the computed result and update the
                        # count of misses.
                        #
                        pass

                    elif _len(cache) >= maxsize:

                        # Use the old root to store
                        # the new key and result.
                        #
                        oldroot         = root
                        oldroot[KEY]    = key
                        oldroot[RESULT] = result

                        # Empty the oldest link and
                        # make it the new root.
                        #
                        root      = nonlocal_root[0] = oldroot[NEXT]
                        oldkey    = root[KEY]
                        root[KEY] = root[RESULT] = None

                        # Now update the cache
                        # dictionary for the new
                        # links.
                        #
                        del cache[oldkey]
                        cache[key] = oldroot

                    else:

                        # Put result in a new link
                        # at the front of the list.
                        #
                        last       = root[PREV]
                        link       = [last, root, key, result]
                        last[NEXT] = root[PREV] = cache[key] = link

                    stats[MISSES] += 1

                return result

        # ---------------------------------------------------------------------
        def cache_info():
            """
            Return a _CacheInfo named tuple containing cache statistics.

            ---
            type:   function
            ...

            """
            with lock:
                return _CacheInfo(
                            stats[HITS], stats[MISSES], maxsize, len(cache))

        # ---------------------------------------------------------------------
        def cache_clear():
            """
            Clear the cache and cache statistics.

            ---
            type:   function
            ...

            """
            with lock:
                cache.clear()
                root     = nonlocal_root[0]
                root[:]  = [root, root, None, None]
                stats[:] = [0, 0]

        wrapper.__wrapped__ = user_function
        wrapper.cache_info  = cache_info
        wrapper.cache_clear = cache_clear

        return functools.update_wrapper(wrapper, user_function)

    return decorating_function
