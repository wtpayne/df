# -*- coding: utf-8 -*-
"""
VRCAM UI.

"""

import bowyer.lib.ui.web.markup.html
import bowyer.lib.ui.web.util
import bowyer.lib.web.util
import bowyer.app.vrcam.aframe


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Image encoder coroutine.

    """
    signal  = None
    map_res = bowyer.lib.web.util.ResMap()
    html    = bowyer.lib.ui.web.markup.html

    outputs['ui']['ena']  = False
    outputs['ui']['list'] = [dict(map_res)]

    while True:

        inputs = yield (outputs, signal)

        outputs['ui']['ena'] = False
        outputs['ui']['list'].clear()

        if not inputs['control']['ena']:
            continue

        # List of resource-id of dynamic resources.
        list_id_res_dynamic = ['img_base64',
                               'seg_base64']

        # SSE topic.
        id_app   = 'vrui'
        id_topic = id_app + '_updates'
        map_res.topic(**{id_topic: list_id_res_dynamic})

        map_res.htm(
            vrui = _page(
                title       = 'vrui',
                id_topic    = id_topic,
                list_id_ui  = [],
                list_uri_js = ['/aframe.min.js',
                               '/aframe_extras.min.js',
                               # '/aframe_extras.misc.min.js',
                               '/super_hands.js',
                               '/_hyperscript_web.min.js',
                               '/htmx.js',
                               '/sse.js',
                               '/vrcam.js']))

        outputs['ui']['ena']  = True
        outputs['ui']['list'] = [dict(map_res)]


# -----------------------------------------------------------------------------
def _page(title, id_topic, list_id_ui, list_uri_js = list()):
    """
    Return a default VRUI HTML page.

    """
    html   = bowyer.lib.ui.web.markup.html
    aframe = bowyer.app.vrcam.aframe
    page   = html.document(title = title)
    with page.head:

        html.meta(charset = 'utf-8')

        html.meta(name    = 'viewport',
                  content = 'width=device-width, initial-scale=1.0')

        html.link(rel     = 'stylesheet',
                  href    = ('https://fonts.googleapis.com/css2'
                             '?family=Roboto:wght@100;300;900&display=swap'))

        # TAILWIND
        html.link(rel  = 'stylesheet',
                  href = ('https://unpkg.com/tailwindcss'
                          '@^2/dist/tailwind.min.css'))

        # Javascript
        for uri_js in list_uri_js:
            html.script(type = 'text/javascript', src = uri_js)

    with page:

        with aframe.a_scene():

            with aframe.a_assets():
                html.canvas(
                    id     = 'canvas_img',
                    width  = '640',
                    height = '480');

                html.canvas(
                    id     = 'canvas_seg',
                    width  = '160',
                    height = '120');

            with aframe.a_entity():
                aframe.a_camera()
                aframe.a_entity(
                    **{'super-hands':     '',
                       'sphere-collider': 'objects: a-box',
                       'hand-controls':   'hand: left'})
                aframe.a_entity(
                    **{'super-hands':     '',
                       'sphere-collider': 'objects: a-box',
                       'hand-controls':   'hand: right'})

            aframe.a_box(
                hoverable   = '',
                grabbable   = '',
                stretchable = '',
                draggable   = '',
                dropppable  = '',

                sseimg      = 'topic: /vrui_updates; resource: img_base64; id_canvas: canvas_img',
                material    = 'src:#canvas_img',
                src         = '/seg',

                height      = 0.4,
                width       = 0.5,
                depth       = 0.01,
                position    = '0 1.2 -0.65')

            aframe.a_box(

                sseimg      = 'topic: /vrui_updates; resource: seg_base64; id_canvas: canvas_seg',
                material    = 'src:#canvas_seg',
                src         = '/seg',

                height      = 0.4,
                width       = 0.5,
                depth       = 0.01,
                position    = '-0.6 1.2 -0.65',
                rotation    = '0, 30, 0')

            aframe.a_sky(
                color    = '#FFFFFF')

# <a-ocean color="aqua" depth="100" width="100"></a-ocean>

                # # id       = 'grid',
                # # material = 'color: #B0B0BF',
                # scale    = '1.0 1.0 1.0',
                # position = '0.0 0.0 0.0')

            # aframe.a_hexgrid(
            #     id       = 'grid',
            #     src      = '/hexgrid.json',
            #     material = 'color: #FFFFFF',
            #     scale    = '0.2 0.2 0.2',
            #     position = '0 0 0')

            # backgroundEl.setAttribute('material', {
            #   shader: 'background-gradient',
            #   colorTop: '#37383c',
            #   colorBottom: '#757575',
            #   side: 'back'
            # });

            aframe.a_entity(**{'oculus-touch-controls': 'hand: left'})
            aframe.a_entity(**{'oculus-touch-controls': 'hand: right'})

    return page

