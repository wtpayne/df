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
    "Copyright 2022-2023 William Payne"

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
