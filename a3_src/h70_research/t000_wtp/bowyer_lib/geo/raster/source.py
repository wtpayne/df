# -*- coding: utf-8 -*-
"""
Bowyer component for generating raster data for charts and maps.

"""

import cartopy.io.img_tiles
import cartopy.crs  # Note we need Shapely <= 1.7.1 as 1.8 causes crash.
import matplotlib
import numpy
import PIL

# Use the antigrain geometry backend
# for rendering, removing the need to
# have an x server running and allowing
# us to use this component on headless
# computers.
#
matplotlib.use('Agg')
import matplotlib.pyplot


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Raster data generator coroutine.

    """
    signal = None


    # stamen_terrain = cartopy.io.img_tiles.Stamen('terrain-background')
    stamen_terrain = cartopy.io.img_tiles.Stamen('terrain')

    axes   = matplotlib.pyplot.axes(projection = stamen_terrain.crs)
    figure = axes.get_figure()


    # Limit the extent of the map to a small longitude/latitude range.
    axes.set_extent([-1.3, -1, 50.7, 50.85], crs = cartopy.crs.Geodetic())

    # Add the Stamen data at zoom level 8.
    axes.add_image(stamen_terrain, 11)

    while True:

        inputs = yield (outputs, signal)

        # TODO: Update axes.

        array_bgr = _draw_to_bgr(figure)

        for id_out in outputs.keys():
            outputs[id_out]['ena']  = True
            outputs[id_out]['buff'] = array_bgr


# -----------------------------------------------------------------------------
def _draw_to_bgr(figure):
    """
    Return a numpy BGR array containing an image of the specified figure.

    """
    canvas = figure.canvas
    canvas.draw()

    buffer          = canvas.tostring_rgb()
    (width, height) = canvas.get_width_height()
    shape_array     = (height, width, 3)

    rgb = numpy.frombuffer(buffer, dtype = numpy.uint8)
    rgb = rgb.reshape(shape_array)
    bgr = rgb[...,::-1].copy()

    return bgr
