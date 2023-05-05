# -*- coding: utf-8 -*-
"""
Fundamental types definition module.

This module defines a list of fundamental
types which are understood by the autodata
package.

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


import ctypes as ct
import collections
import functools

import numpy


# -----------------------------------------------------------------------------
@functools.lru_cache(maxsize = 1)
def _typeinfo_table():
    """
    Return a tuple of fundamental type parameter namedtuples.

    """
    type_info = collections.namedtuple('TypeInfo',
            ['name',     # numpy type name.
             'py',       # python type. (for conversion)
             'py_eq',    # True if python type is binary-compatible.
             'c',        # c type. (for conversion)
             'c_eq',     # True if c type is binary-compatible.
             'ctypes'])  # Ctypes type

    return tuple(type_info._make(tup) for tup in (
        ('bool_',      bool,    True,  None,             False,  None        ),
        ('bool8',      bool,    False, None,             False,  None        ),
        ('byte',       int,     False, 'char',           True, ct.c_byte     ),
        ('short',      int,     False, 'short',          True, ct.c_short    ),
        ('intc',       int,     False, 'int',            True, ct.c_int      ),
        ('int_',       int,     False, 'long',           True, ct.c_long     ),
        ('longlong',   int,     False, 'long long',      True, ct.c_longlong ),
        ('intp',       int,     False, 'void *',         True, None          ),
        ('int8',       int,     False, 'int8_t',         True, None          ),
        ('int16',      int,     False, 'int16_t',        True, None          ),
        ('int32',      int,     False, 'int32_t',        True, None          ),
        ('int64',      int,     False, 'int64_t',        True, None          ),
        ('ubyte',      int,     False, 'unsigned char',  True, ct.c_ubyte    ),
        ('ushort',     int,     False, 'unsigned short', True, ct.c_ushort   ),
        ('uintc',      int,     False, 'unsigned int',   True, ct.c_uint     ),
        ('uint',       int,     True,  None,             False,  None        ),
        ('ulonglong',  int,     False, 'long long',      True, ct.c_ulonglong),
        ('uintp',      int,     False, 'void *',         True, None          ),
        ('uint8',      int,     False, 'uint8_t',        True, None          ),
        ('uint16',     int,     False, 'uint16_t',       True, None          ),
        ('uint32',     int,     False, 'uint32_t',       True, None          ),
        ('uint64',     int,     False, 'uint64_t',       True, None          ),
        ('half',       float,   False, None,             False,  None        ),
        ('single',     float,   False, 'float',          True, ct.c_float    ),
        ('double',     float,   False, 'double',         True, ct.c_double   ),
        ('float_',     float,   True,  None,             False,  None        ),
        ('float',      float,   False, None,             False,  None        ),
        ('longfloat',  float,   False, 'long float',     True, None          ),
        ('float16',    float,   False, None,             False,  None        ),
        ('float32',    float,   False, None,             False,  None        ),
        ('float64',    float,   False, None,             False,  None        ),
        ('float128',   float,   False, None,             False,  None        ),
        ('csingle',    float,   False, None,             False,  None        ),
        ('complex_',   complex, True,  None,             False,  None        ),
        ('clongfloat', complex, False, None,             False,  None        ),
        ('complex64',  complex, False, None,             False,  None        ),
        ('complex128', complex, False, None,             False,  None        ),
        ('complex256', complex, False, None,             False,  None        )
    ))


# -----------------------------------------------------------------------------
@functools.lru_cache(maxsize = 1)
def _typeinfo_index():
    """
    Return a lookup table for all fundamental types.

    """
    lut = collections.defaultdict(list)
    for typeinfo in _typeinfo_table():
        dtype = numpy.dtype(typeinfo.name)
        lut[dtype].append(typeinfo)
    return dict(lut)


# -----------------------------------------------------------------------------
@functools.lru_cache(maxsize = 1)
def names():
    """
    Return a tuple containing all known fundamental type names.

    """
    name_set = set()
    for info in _typeinfo_table():
        dtype = numpy.dtype(info.name)
        name_set.add(dtype.char)
        name_set.add(info.name)
    unique_names = tuple(name_set)
    return unique_names


# -----------------------------------------------------------------------------
def lookup(key):
    """
    Return the type corresponding to the specified key.

    """
    return _typeinfo_index()[numpy.dtype(key)]


# -----------------------------------------------------------------------------
def is_fundamental(key):
    """
    Return True if key represents a fundamental type, False otherwise.

    """
    try:
        numpy.dtype(key)
    except TypeError:
        return False
    else:
        return True
