# -*- coding: utf-8 -*-
"""
UI component for controlling a web based multi-feed video widget.

This is mainly intended for providing operator
situational awareness views in multi-camera
systems.

"""


import base64
import textwrap

import cv2

import bowyer.lib.ui.web.markup.html
import bowyer.lib.ui.web.util
import bowyer.lib.web.util
import bowyer.app.vrcam.aframe


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Image encoder coroutine.

    This will create a HTML canvas for each
    input video stream

    """
    signal                       = None
    outputs['resources']['ena']  = False
    outputs['uidata']['ena']     = False
    outputs['resources']['list'] = []
    outputs['uidata']['list']    = []

    # Lookup table mapping from configuration
    # format id to imencode format argument,
    # data url format specifier and resource
    # map format specific add function.
    #
    # https://www.iana.org/assignments/media-types/media-types.xhtml#image
    #
    map_res = bowyer.lib.web.util.ResMap()
    id_fmt  = cfg.get('format', 'jpeg')
    map_fmt = dict(
        bmp    = ('.bmp',  'image/bmp',  map_res.bmp),    # MS windows, OS/2 bitmap.
        jpeg   = ('.jpg',  'image/jpeg', map_res.jpeg),   # JPEG.
        jpeg2k = ('.jp2',  'image/jp2',  map_res.jpeg2k), # JPEG 2000.
        png    = ('.png',  'image/png',  map_res.png),    # Portable network graphics format.
        webp   = ('.webp', 'image/webp', map_res.webp),   # WebP image.
        tiff   = ('.tiff', 'image/tiff', map_res.tiff))   # Tagged image file format.
    (fmt_imencode, fmt_data_url, map_res_add_fcn) = map_fmt[id_fmt]

    while True:

        inputs = yield (outputs, signal)

        outputs['resources']['ena']  = False
        outputs['resources']['list'].clear()

        outputs['uidata']['ena'] = False
        outputs['uidata']['list'].clear()

        # We create one SSE topic for all
        # SSE events used by this widget.
        # The topic resource is created
        # once the list of SSE events has
        # been filled.
        #
        id_sse_topic   = 'vidfeed_updates'
        uri_sse_topic  = '/' + id_sse_topic
        list_sse_event = []

        uidata = dict()
        uidata['list_htm']    = list()
        uidata['list_uri_js'] = list()

        # Web-encode any images provided as input.
        #
        for key_in in inputs.keys():

            if not inputs[key_in]['ena']:
                continue

            (is_ok, buff_enc) = cv2.imencode(fmt_imencode,
                                             inputs[key_in]['buff'],
                                             [cv2.IMWRITE_WEBP_QUALITY, 30])
            if not is_ok:
                continue

            # Make the image avaiable as a binary resource.
            #
            encoded_bytes = buff_enc.tobytes()
            map_res_add_fcn(**{key_in: encoded_bytes})

            # Make the image available as a base64 encoded resource.
            #
            encoded_base64 = base64.standard_b64encode(encoded_bytes)
            key_base64     = key_in + '_base64'
            map_res_add_fcn(**{key_base64: encoded_base64})

            # Remember that we need to listen for
            # updates to the base64 image resource.
            #
            list_sse_event.append(key_base64)

            # Create a canvas for this video input.
            #
            id_element        = 'canvas_' + key_in
            html              = bowyer.lib.ui.web.markup.html
            html_video_player = html.canvas(id     = id_element,
                                            width  = '320',
                                            height = '200');
            uidata['list_htm'].append(html_video_player.render())

            # Create a javascript callback for
            # this video input.
            #
            id_event   = key_base64
            src_js     = textwrap.dedent("""
                document.addEventListener('DOMContentLoaded', function() {{
                    const evt_src = new EventSource("{uri_sse_topic}");
                    evt_src.addEventListener("{id_event}", function(evt) {{
                        var img = new Image();
                        img.src = "data:{fmt_data_url};base64," + evt.data.slice(2, -1);
                        img.onload = function(){{
                            var canvas = document.getElementById("{id_element}");
                            var ctx    = canvas.getContext("2d");
                            ctx.drawImage(img, 0, 0);
                        }};
                    }});
                }}, false);""".format(
                    uri_sse_topic = uri_sse_topic,
                    id_event      = id_event,
                    fmt_data_url  = fmt_data_url,
                    id_element    = id_element))

            id_res_js = 'vidfeed_{id_input}.js'.format(id_input = key_in)
            map_res.js(**{id_res_js: src_js})
            uidata['list_uri_js'].append(
                                '/{id_res_js}'.format(id_res_js = id_res_js))

        # SSE topic for all SSE events
        #
        map_res.topic(**{id_sse_topic: list_sse_event})

        outputs['resources']['ena']  = True
        outputs['resources']['list'] = [dict(map_res)]

        outputs['uidata']['ena']     = True
        outputs['uidata']['list']    = [uidata]
