# -*- coding: utf-8 -*-
"""
---

title:
    "Design index extract and transform stableflow-edict component."

description:
    "Prepares design information to be stored
    in the design index."

id:
    "f94d59d0-d11e-473c-81d9-8c55edf4fd45"

type:
    dt004_python_stableflow_edict_component

dependencies:
    - pycozo[embedded,pandas]
    - pandas

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2015-2022 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WIT HOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""

import os
import os.path
import pprint

import pycozo.client
import uuid

import cl.core.design.index.db.trace as trace


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Design index component coroutine.

    """

    signal = None

    for id_out in outputs.keys():
        outputs[id_out]['ena']  = False
        outputs[id_out]['ts']   = dict()
        outputs[id_out]['list'] = list()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['list'].clear()

        # For each fileinfo data structure
        # that is input, derive a set
        # of indexable items. Each
        # indexable item represents
        # some piece of indexable design
        # data or metadata. This includes
        # traceability information, test
        # results, coverage, performance
        # metrics etc...
        #
        map_ts = dict()
        list_trace = list()
        if inputs['fileinfo']['ena']:
            map_ts = inputs['fileinfo']['ts']
            for fileinfo in inputs['fileinfo']['list']:
                list_trace.extend(
                    (item for item in _iter_trace(fileinfo)))

        # If any designdata items are
        # ready to be stored in the
        # design index
        #
        if list_trace:
            for id_out in outputs.keys():
                outputs[id_out]['ena'] = True
                outputs[id_out]['ts'].update(map_ts)
                outputs[id_out]['list'][:] = list_trace


# -----------------------------------------------------------------------------
def _iter_trace(fileinfo):
    """
    Yield all trace items that can be derived from fileinfo.

    """
    list_embed    = fileinfo['embed']['list_embed']
    filepath_doc  = fileinfo['filepath']
    tup_embed_doc = _get_tup_embed_doc(list_embed)
    id_doc        = _get_id_doc(filepath_doc  = filepath_doc,
                                tup_embed_doc = tup_embed_doc)

    for trace in _iter_natural_filesystem_hierarchy_traces(
                                id_doc       = id_doc,
                                filepath_doc = filepath_doc):
        yield trace

    for trace in _iter_design_document_metadata_traces(
                                id_doc        = id_doc,
                                tup_embed_doc = tup_embed_doc):
        yield trace

    list_nonconformity = fileinfo['list_nonconformity']
    for trace in _iter_nonconformity_report_traces(
                                id_doc             = id_doc,
                                list_nonconformity = list_nonconformity):
        yield trace


# -----------------------------------------------------------------------------
def _iter_nonconformity_report_traces(id_doc, list_nonconformity):
    """
    Yield all trace items from the nonconformity list.

    """
    if not list_nonconformity:
        return

    id_nc_packet = '.'.join((id_doc, 'nonconformity'))
    yield trace.ensure_valid(
                        id_src    = id_doc,
                        rel_type  = 'nonconformity.packet',
                        id_dst    = id_nc_packet,
                        label_src = '',
                        label_dst = 'nonconformity',
                        metadata  = '')

    for nc in list_nonconformity:
        id_nc_type = str(nc['id_nc'])
        yield trace.ensure_valid(
                            id_src    = 'reports',
                            rel_type  = 'nonconformity.type',
                            id_dst    = id_nc_type,
                            label_src = '',
                            label_dst = id_nc_type,
                            metadata  = '')

        # Trace under type
        id_nc_item = '.'.join((id_nc_packet, id_nc_type))
        yield trace.ensure_valid(
                            id_src    = id_nc_type,
                            rel_type  = 'nonconformity.item',
                            id_dst    = id_nc_item,
                            label_src = '',
                            label_dst = nc['filepath'],
                            metadata  = nc['str_msg'])

        # Trace under document
        id_nc_item = '.'.join((id_nc_packet, id_nc_type))
        yield trace.ensure_valid(
                            id_src    = id_nc_packet,
                            rel_type  = 'nonconformity.item',
                            id_dst    = id_nc_item,
                            label_src = '',
                            label_dst = str(nc['id_nc']),
                            metadata  = nc['str_msg'])


# -----------------------------------------------------------------------------
def _get_tup_embed_doc(list_embed):
    """
    Return the top level embedded data for the design document.

    """
    tup_embed_doc = None
    for tup_embed in list_embed:
        name_type = type(tup_embed.meta.node).__name__
        if name_type == 'Module':
            tup_embed_doc = tup_embed
    return tup_embed_doc


# -----------------------------------------------------------------------------
def _get_id_doc(filepath_doc, tup_embed_doc):
    """
    Return the document ID from the design document top level embedded data.

    This is the 'id' field from the top level
    embedded data if present, otherwise we use
    the filepath as a fallback. We need to have
    this fallback so error messages about missing
    id fields can be associated with the correct
    design document in the local filesystem.

    """
    try:
        return tup_embed_doc.dat['id']
    except (AttributeError, KeyError):
        return filepath_doc


# -----------------------------------------------------------------------------
def _iter_natural_filesystem_hierarchy_traces(id_doc, filepath_doc):
    """
    Yield all natural filesystem hierarchy traces.

    """
    list_tup_backwards = list(_iter_tup_path_parts(filepath_doc))
    list_tup_parts     = list(reversed(list_tup_backwards))
    list_tup_src_dst   = list(zip(list_tup_parts, list_tup_parts[1:]))
    count_tup_src_dst  = len(list_tup_src_dst)
    idx_last           = count_tup_src_dst - 1

    for (idx, tup_src_dst) in enumerate(list_tup_src_dst):
        (tup_src, tup_dst)  = tup_src_dst
        (id_src, label_src) = tup_src
        (id_dst, label_dst) = tup_dst
        metadata            = ''
        rel_type            = 'natural.filesystem_hierarchy'

        if idx == idx_last:
            id_dst = id_doc

        yield trace.ensure_valid(id_src    = id_src,
                                 rel_type  = rel_type,
                                 id_dst    = id_dst,
                                 label_src = label_src,
                                 label_dst = label_dst,
                                 metadata  = metadata)


# -----------------------------------------------------------------------------
def _iter_tup_path_parts(filepath):
    """
    Yield (path, name) tuples for all parts of the specified filepath.

    i.e. (dirpath, dirname) for all containing
    directories in the path, and (filepath, filename)
    for the actual file itself.

    """
    path = os.path.normpath(filepath)
    while True:
        (path_next, name) = os.path.split(path)
        if not name:
            return
        yield (path, name)
        path = path_next


# -----------------------------------------------------------------------------
def _iter_design_document_metadata_traces(id_doc, tup_embed_doc):
    """
    Yield all metadata traces.

    """
    if not tup_embed_doc:
        return

    id_doc_metadata = '.'.join((id_doc, 'metadata'))
    yield trace.ensure_valid(
                        id_src    = id_doc,
                        rel_type  = 'metadata.packet',
                        id_dst    = id_doc_metadata,
                        label_src = '',
                        label_dst = 'metadata',
                        metadata  = pprint.pformat(tup_embed_doc.dat))

    for (key, value) in tup_embed_doc.dat.items():
        yield trace.ensure_valid(
                            id_src    = id_doc_metadata,
                            rel_type  = 'metadata.item',
                            id_dst    = '.'.join((id_doc_metadata, str(key))),
                            label_src = '',
                            label_dst = str(key),
                            metadata  = str(value))
