# -*- coding: utf-8 -*-
"""
Web image encoder.

"""


import cv2
import base64


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Image encoder coroutine.

    """
    signal = None

    outputs['encoded']['ena']  = False
    outputs['encoded']['list'] = list()

    id_fmt  = cfg.get('format', 'jpeg')
    map_fmt = dict(
        bmp      = ('.bmp',  'image/bmp'),                # MS windows, OS/2 bitmap.
        dib      = ('.dib',  'image/dib'),                # Device independent bitmap.
        jpeg     = ('.jpg',  'image/jpeg'),               # JPEG.
        jpeg2000 = ('.jp2',  'image/jpm'),                # JPEG 2000.
        png      = ('.png',  'image/png'),                # Portable network graphics format.
        webp     = ('.webp', 'image/webp'),               # WebP image.
        pbm      = ('.pbm',  'image/x-portable-bitmap'),  # Portable bit map.
        tiff     = ('.tiff', 'image/tiff'),               # Tagged image file format.
        hdr      = ('.hdr',  'image/vnd.radiance'))       # Radiance HDR files.
        # TODO: GDAL for geospatial imagery.

    (fmt_imencode, fmt_mimetype) = map_fmt[id_fmt]

    while True:

        inputs = yield (outputs, signal)

        outputs['encoded']['ena'] = False
        outputs['encoded']['list'].clear()

        for key in inputs.keys():

            if not inputs[key]['ena']:
                continue

            (is_ok, buff_enc) = cv2.imencode(fmt_imencode, inputs[key]['buff'])
            if not is_ok:
                continue

            encoded_bytes  = buff_enc.tobytes()
            encoded_base64 = base64.standard_b64encode(encoded_bytes)
            key_base64     = key + '_base64'

            for id_out in outputs.keys():
                outputs[id_out]['ena']  = True
                outputs[id_out]['list'].append({
                    key:        (fmt_mimetype, encoded_bytes),
                    key_base64: (fmt_mimetype, encoded_base64)})
