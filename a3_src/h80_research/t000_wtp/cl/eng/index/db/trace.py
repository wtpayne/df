# -*- coding: utf-8 -*-
"""
---

title:
    "Trace relation module."

description:
    "This module contains constants to
    help with using the trace relation
    in cozodb."

id:
    "165d06bb-c131-4782-8700-36e67ed51410"

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


import pycozo.client



# ?[is, id] := *trace[is, r, id, s, d, m]
# ?[r, id] := *trace["/media/wtp/Data/dev/df/ws00_pri/a3_src", r, id, s, d, m]


_ID_SRC        = 'is'
_LABEL_SRC     = 's'
_REL_TYPE      = 'r'
_ID_DST        = 'id'
_LABEL_DST     = 'd'
_METADATA_DST  = 'm'

_REL_TRACE     = 'trace'
_HDR_TRACE     = [_ID_SRC, _REL_TYPE, _ID_DST, _LABEL_SRC, _LABEL_DST, _METADATA_DST]


_SCRIPT_CREATE_RELATIONS = f"""
        {{
            :timeout 2
            :create {_REL_TRACE}
            {{
                {_ID_SRC}:        String,
                {_REL_TYPE}:      String,
                {_ID_DST}:        String
                =>
                {_LABEL_SRC}:     String,
                {_LABEL_DST}:     String,
                {_METADATA_DST}:  String
            }}
        }}

        """
_SCRIPT_PUT_DATA = f"""
        {{
            :timeout 2
            ?[{_ID_SRC},
              {_REL_TYPE},
              {_ID_DST},
              {_LABEL_SRC},
              {_LABEL_DST},
              {_METADATA_DST}] <- [[${_ID_SRC},
                                    ${_REL_TYPE},
                                    ${_ID_DST},
                                    ${_LABEL_SRC},
                                    ${_LABEL_DST},
                                    ${_METADATA_DST}]]
            :put {_REL_TRACE}
            {{
                {_ID_SRC}:        String,
                {_REL_TYPE}:      String,
                {_ID_DST}:        String
                =>
                {_LABEL_SRC}:     String,
                {_LABEL_DST}:     String,
                {_METADATA_DST}:  String
            }}
        }}

        """
_SCRIPT_QUERY_BY_SRC  = f"""
        {{
            ?[{_REL_TYPE},
              {_ID_DST},
              {_LABEL_SRC},
              {_LABEL_DST},
              {_METADATA_DST}] := *{_REL_TRACE}[${_ID_SRC},
                                                 {_REL_TYPE},
                                                 {_ID_DST},
                                                 {_LABEL_SRC},
                                                 {_LABEL_DST},
                                                 {_METADATA_DST}]
        }}"""


# -----------------------------------------------------------------------------
def ensure_valid(
                *, id_src, rel_type, id_dst, label_src, label_dst, metadata):
    """
    Return a tuple with validated trace table row data

    """
    assert isinstance(id_src,    str)
    assert isinstance(rel_type,  str)
    assert isinstance(id_dst,    str)
    assert isinstance(label_src, str)
    assert isinstance(label_dst, str)
    assert isinstance(metadata,  str)
    return (id_src, rel_type, id_dst, label_src, label_dst, metadata)


# =============================================================================
class DataBase():
    """
    Design index traceability database.

    """

    # -------------------------------------------------------------------------
    def __init__(self, filepath_db, str_engine  = 'sqlite'):
        """
        Construct a trace DataBase instance.

        """
        self._client =  pycozo.client.Client(engine    = str_engine,
                                             path      = filepath_db,
                                             options   = None,
                                             dataframe = False)
        try:
            self._client.run(script = _SCRIPT_CREATE_RELATIONS)
        except Exception as err:
            print(err)
            pass  # An exception will always be thrown after the first run.

    # -------------------------------------------------------------------------
    def bulk_upsert(self, iter_tup_trace):
        """
        Bulk upsert the specified trace data.

        """
        map_importdata = {
            _REL_TRACE: {
                'headers': _HDR_TRACE,
                'rows':    iter_tup_trace
            }
        }
        self._client.import_relations(map_importdata)

    # -------------------------------------------------------------------------
    def iter_trace(self, id_from):
        """
        Yield traces from the specified origin.

        """
        try:
            result = self._client.run(script = _SCRIPT_QUERY_BY_SRC,
                                      params = {_ID_SRC: id_from})
            for trace in result['rows']:
                yield trace
        except:
            pass
