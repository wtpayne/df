# -*- coding: utf-8 -*-
"""
Durga UI.

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

    outputs['resources']['ena']  = False
    outputs['resources']['list'] = []

    while True:

        inputs = yield (outputs, signal)

        outputs['resources']['ena'] = False
        outputs['resources']['list'].clear()

        # Aggregate uidata from inputs.
        #
        list_uri_js = []
        list_htm    = []
        for (id_input, item_input) in inputs.items():
            if not item_input['ena']:
                continue
            for uidata in item_input['list']:
                list_uri_js.extend(uidata['list_uri_js'])
                list_htm.extend(uidata['list_htm'])

        map_res.htm(
            durga = _page(title       = 'durga',
                          list_htm    = list_htm,
                          list_uri_js = list_uri_js))

        outputs['resources']['ena']  = True
        outputs['resources']['list'] = [dict(map_res)]


# -----------------------------------------------------------------------------
def _js

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


# -----------------------------------------------------------------------------
def _page(title, list_htm = None, list_uri_js = None):
    """
    Return a default VRUI HTML page.

    """
    if list_htm is None:
        list_htm = list()

    if list_uri_js is None:
        list_uri_js = list()

    html   = bowyer.lib.ui.web.markup.html
    page   = html.document(title = title)
    with page.head:

        html.meta(charset = 'utf-8')

        html.meta(name    = 'viewport',
                  content = 'width=device-width, initial-scale=1.0')

        html.link(rel     = 'stylesheet',
                  href    = ('https://fonts.googleapis.com/css2'
                             '?family=Roboto:wght@100;300;900&display=swap'))

        html.link(rel  = 'stylesheet',
                  href = ('https://unpkg.com/tailwindcss'
                          '@^2/dist/tailwind.min.css'))

        for uri_js in list_uri_js:
            html.script(type = 'text/javascript', src = uri_js)

    with page:
        with html.div():
            for htm_fragment in list_htm:
                html.raw(htm_fragment)

    return page

