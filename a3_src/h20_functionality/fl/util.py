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


import collections.abc


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
def walkobj(obj,                                  # pylint: disable=R0912,R0913
            gen_leaf    = False,
            gen_nonleaf = False,
            gen_path    = False,
            gen_obj     = False,
            path        = (),
            memo        = None):
    """
    Generate a walk over a treelike structure of mappings and other iterables.

    Adapted from:
    http:/code.activestate.com/recipes/577982-recursively-walk-python-objects/

    This function performs a (depth-first left to
    right recursive) traversal over the provided
    data structure, which we assume to consist of
    a finite; treelike arrangement of nested
    collections.Mapping and collections.Iterable
    types.

    This function can be configured to yield
    information about nodes in the tree: leaf
    nodes; non-leaf (internal) nodes or both.

    The information that is yielded may also be
    configured: the path to the node can be
    delivered as can the object at the node
    itself.

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
        return getattr(mapping, 'iteritems', mapping.items)()
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
