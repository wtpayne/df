# -*- coding: utf-8 -*-
"""
Decompress bytes

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
    map_ctx         = dict()

    # Initialize outputs.
    #
    for id_out in outputs.keys():
        outputs[id_out]['ena'] = False
        outputs[id_out]['ts']  = dict()
        outputs[id_out]['map'] = dict()

    while True:

        inputs = yield (outputs, signal)

        # Reset outputs.
        #
        for id_out in outputs.keys():
            outputs[id_out]['ena'] = False
            outputs[id_out]['ts'].clear()
            outputs[id_out]['map'].clear()

        if not inputs['raw_samples']['ena']:
            continue

        # Update sample buffer.
        #
        deq_samples.extend(inputs['raw_samples']['list'])

        idx = inputs['raw_samples']['ts']['idx']
        do_update_dict = (idx % interval_update) == 0
        if not deq_dict or do_update_dict:

            list_samples = list(deq_samples)
            zdict        = zstandard.train_dictionary(sz_dict, list_samples)
            id_zdict     = zstandard.dictionary_id(zdict)
            deq_dict.append((id_zdict,zdict))

        ctx = zstandard.ZstdCompressor(dict_data = deq_dict[0])

        for sample in inputs['raw_samples']['list']:
            compressed = cctx.compress(sample)


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _update_dict():



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
