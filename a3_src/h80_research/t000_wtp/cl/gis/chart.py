# -*- coding: utf-8 -*-
"""
Imgui chart component using GDAL.

"""

import imgui
import osgeo.gdal

import stableflow.lib.ui.imgui.util


# -----------------------------------------------------------------------------
def coro_frontend(inputs, outputs):
    """
    Chart component.

    """
    osgeo.gdal.UseExceptions()
    kap   = osgeo.gdal.Open('/media/wtp/Data/charts/L8-80-120-8-16_8.kap')
    band  = kap.GetRasterBand(1)
    array = band.ReadAsArray()
    img_cv2 = array

    # filepath_img = '/home/wtp/Desktop/img.png'
    # img_cv2      = cv2.imread(filepath_img)
    texture_id   = stableflow.lib.ui.imgui.util.gen_opengl_texture(img_cv2)

    while True:

        (inputs, context)   = yield (outputs)
        (ctx_ui, ctx_frame) = context

        with stableflow.lib.ui.imgui.util.background_context(ctx_ui, name = 'background'):
            size = imgui.get_content_region_available()
            imgui.image(texture_id, size.x, size.y);

            if imgui.begin_popup_context_window(mouse_button = 1):
                imgui.menu_item('New',  'Ctrl+N', False, True)

                # submenu
                if imgui.begin_menu('Feed', True):
                    # Label, shortcut, selected, enabled
                    is_selected = False
                    is_enabled  = True
                    imgui.menu_item('Moving map',  None, is_selected, is_enabled)
                    imgui.menu_item('Video',       None, is_selected, is_enabled)
                    imgui.menu_item('Diagnostics', None, is_selected, is_enabled)
                    imgui.end_menu()


                if imgui.begin_menu('Send to', True):
                    imgui.menu_item('Display 1', None, is_selected, is_enabled)
                    imgui.menu_item('Display 2', None, is_selected, is_enabled)
                    imgui.end_menu()

                imgui.end_popup()


