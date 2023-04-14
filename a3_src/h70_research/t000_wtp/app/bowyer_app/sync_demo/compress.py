# -*- coding: utf-8 -*-
"""
Compress bytes

"""


import collections

import zstandard


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Generate key-value data

    """
    signal = None

    # State.
    #
    interval_update = 1024    # Update dictionary every 1024 simulation steps.
    size_dict       = 131072  # Size of dict in bytes
    deq_samples     = collections.deque(maxlen = 1024)
    deq_dict        = collections.deque(maxlen = 256)



    compressor   = None
    list_backlog = list()

    # Initialize outputs.
    #
    outputs['zdict']['ena']      = False
    outputs['zdict']['id_zdict'] = None
    outputs['zdict']['bytes'].clear()
    outputs['compressed']['ena']      = False
    outputs['compressed']['id_zdict'] = None
    outputs['compressed']['list'].clear()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        outputs['zdict']['ena']     = False
        outputs['zdict']['id_dict'] = None
        outputs['zdict']['bytes'].clear()
        outputs['compressed']['ena']     = False
        outputs['compressed']['id_dict'] = None
        outputs['compressed']['list'].clear()

        # Update the active compressor.
        #
        if inputs['id_zdict']['ena']:
            compressor = zstandard.ZstdCompressor(
                                dict_data = map_dict(inputs['id_zdict']['id']))

        # Compress samples using the
        # active compressor.
        #
        has_new_samples = inputs['raw_samples']['ena']
        list_compressed = list()
        if has_new_samples:
            map_ts   = inputs['raw_samples']['ts']
            list_raw = inputs['raw_samples']['list']
            list_backlog.extend(list_raw)

            has_compressor = compressor is not None
            if has_compressor:
                list_compressed.extend(
                                    compressor.compress(it) for it in list_backlog)
            else:


        id_zdict_new = None
        zdict_new    = None
        if has_new_samples:
            deq_samples.extend(list_raw)
            zdict = _maybe_new_dict(
                            idx            = map_ts['idx'],
                            deq_samples    = deq_samples,
                            deq_compressor = deq_compressor)


        if (zdict_new is not None) and (id_zdict_new is not None):
            outputs['zdict']['ena']     = True
            outputs['zdict']['id_dict'] = id_zdict_new
            outputs['zdict']['bytes']   = zdict_new
        if list_compressed:
            outputs['compressed']['ena']      = True
            outputs['compressed']['id_zdict'] = id_zdict
            outputs['compressed']['list'].extend(list_comp)

# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _maybe_new_dict(idx, deq_samples, deq_compressor):
    """
    Decide if it's time to propose a new dictionary to use.

    """
    do_propose_new = (idx % interval_update) == 0
    if not deq_dict or do_propose_new:

        list_samples = list(deq_samples)
        zdict        = zstandard.train_dictionary(sz_dict, list_samples)
        id_zdict     = zstandard.dictionary_id(zdict)
        compressor   = zstandard.ZstdCompressor(dict_data = zdict)
        deq_compressor.append((id_zdict, zdict, compressor))
        return zdict

    return None



# >>> for source_data in input_data:
# ...     compressed = cctx.compress(source_data)
# ...     # Do something with compressed data.
# ...
# >>> dctx = zstandard.ZstdDecompressor(dict_data=dict_data)
# >>> for compressed_data in input_data:
# ...     buffer = io.BytesIO()
# ...     with dctx.stream_writer(buffer) as decompressor:
# ...         decompressor.write(compressed_data)
# ...         # Do something with raw data in ``buffer``.
