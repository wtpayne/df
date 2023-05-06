# -*- coding: utf-8 -*-
"""
The ipc module supports inter-process comms with the notification server.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2023 William Payne"

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


import base64
import json


# -----------------------------------------------------------------------------
def write(stream, msg):
    """
    Serialise and encode msg data and write it to the specified stream.

    """
    string_base64 = _encode(msg)
    try:
        num_bytes = stream.write(string_base64 + '\n')
    except BrokenPipeError as err:
        print('BrokenPipeError: ' + str(err) + ' - ' + str(msg))
        num_bytes = 0
    return num_bytes


# -----------------------------------------------------------------------------
def read(stream):
    """
    Read and decode data from the specified stream.

    """
    try:
        string_base64 = stream.readline()
        if not string_base64:
            return None
    except ConnectionError:
        return None

    msg = _decode(string_base64)

    return msg


# -----------------------------------------------------------------------------
def _encode(msg):
    """
    Serialise and encode the specified message data.

    We use JSON as a serialisation format because
    it is more secure than pickle or YAML.

    The serialised data is then base-64 encoded
    so that we can use newline-delimited messages
    to send it over the pipe.

    """
    string_json   = json.dumps(msg, sort_keys = True)
    bytes_json    = string_json.encode('utf-8')
    bytes_base64  = base64.b64encode(bytes_json)
    string_base64 = bytes_base64.decode('utf-8')
    return string_base64


# -----------------------------------------------------------------------------
def _decode(string_base64):
    """
    Return a message structure decoded from the specified string.

    """
    bytes_base64 = string_base64.encode('utf-8')
    bytes_json   = base64.b64decode(bytes_base64)
    string_json  = bytes_json.decode('utf-8')
    msg          = json.loads(string_json)
    return msg
