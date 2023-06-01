# -*- coding: utf-8 -*-
"""
---

title:
    "Light theme for FlowForge."

description:
    "This python module defines the light
    theme for the FlowForge system."

id:
    "7a3a84d9-061b-4ebb-9e51-dcd7f51f404f"

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


import fl.util

from .. import brand
from .. import font
from .. import icon


# -----------------------------------------------------------------------------
def theme():
    """
    Return the light theme.

    """

    theme   = fl.util.Bureau()
    palette = brand.palette()

    theme.FILEPATH_FONT_PRIMARY = font.path(id_theme = 'light',
                                            id_font  = 'primary')
    theme.ICON_PLAY_16X16       = icon.load(id_theme = 'light',
                                            id_icon  = 'play')
    theme.ICON_PAUSE_16X16      = icon.load(id_theme = 'light',
                                            id_icon  = 'pause')
    theme.ICON_STOP_16X16       = icon.load(id_theme = 'light',
                                            id_icon  = 'stop')

    # Core style
    #
    theme.ALPHA_X                         = 1.0
    theme.ALPHA_Y                         = 1.0

    theme.WINDOW_PADDING_X                = None
    theme.WINDOW_PADDING_Y                = None
    theme.WINDOW_ROUNDING_X               = 3
    theme.WINDOW_ROUNDING_Y               = 3
    theme.WINDOW_BORDER_SIZE_X            = 1
    theme.WINDOW_BORDER_SIZE_Y            = 1
    theme.WINDOW_MIN_SIZE_X               = 1
    theme.WINDOW_MIN_SIZE_Y               = 1
    theme.WINDOW_TITLE_ALIGN_X            = 1
    theme.WINDOW_TITLE_ALIGN_Y            = 1

    theme.CHILD_ROUNDING_X                = 1
    theme.CHILD_ROUNDING_Y                = 1
    theme.CHILD_BORDER_SIZE_X             = 1
    theme.CHILD_BORDER_SIZE_Y             = 1

    theme.POPUP_ROUNDING_X                = 1
    theme.POPUP_ROUNDING_Y                = 1
    theme.POPUP_BORDER_SIZE_X             = 1
    theme.POPUP_BORDER_SIZE_Y             = 1

    theme.FRAME_PADDING_X                 = 0
    theme.FRAME_PADDING_Y                 = 0
    theme.FRAME_ROUNDING_X                = 3
    theme.FRAME_ROUNDING_Y                = 3
    theme.FRAME_BORDER_SIZE_X             = 0
    theme.FRAME_BORDER_SIZE_Y             = 0

    theme.ITEM_SPACING_X                  = 2
    theme.ITEM_SPACING_Y                  = 2
    theme.ITEM_INNER_SPACING_X            = 0
    theme.ITEM_INNER_SPACING_Y            = 0

    theme.INDENT_SPACING_X                = 1
    theme.INDENT_SPACING_Y                = 1
    theme.CELL_PADDING_X                  = 1
    theme.CELL_PADDING_Y                  = 1
    theme.SCROLLBAR_SIZE_X                = 10
    theme.SCROLLBAR_SIZE_Y                = 10
    theme.SCROLLBAR_ROUNDING_X            = 3
    theme.SCROLLBAR_ROUNDING_Y            = 3
    theme.GRAB_MIN_SIZE_X                 = 1
    theme.GRAB_MIN_SIZE_Y                 = 1
    theme.GRAB_ROUNDING_X                 = 1
    theme.GRAB_ROUNDING_Y                 = 1
    theme.TAB_ROUNDING_X                  = 1
    theme.TAB_ROUNDING_Y                  = 1

    theme.BUTTON_TEXT_ALIGN_X             = 1
    theme.BUTTON_TEXT_ALIGN_Y             = 1
    theme.SELECTABLE_TEXT_ALIGN_X         = 1
    theme.SELECTABLE_TEXT_ALIGN_Y         = 1

    # Node style
    #
    theme.GRID_SPACING_X                  = 8
    theme.GRID_SPACING_Y                  = 8

    theme.NODE_CORNER_ROUNDING_X          = 5
    theme.NODE_CORNER_ROUNDING_Y          = 5
    theme.NODE_PADDING_HORIZONTAL_X       = 5
    theme.NODE_PADDING_HORIZONTAL_Y       = 5
    theme.NODE_PADDING_VERTICAL_X         = 5
    theme.NODE_PADDING_VERTICAL_Y         = 5
    theme.NODE_BORDER_THICKNESS_X         = 1
    theme.NODE_BORDER_THICKNESS_Y         = 1

    theme.LINK_THICKNESS_X                = 1
    theme.LINK_THICKNESS_Y                = 1
    theme.LINK_LINE_SEGMENTS_PER_LENGTH_X = 1
    theme.LINK_LINE_SEGMENTS_PER_LENGTH_Y = 1
    theme.LINK_HOVER_DISTANCE_X           = 10
    theme.LINK_HOVER_DISTANCE_Y           = 10

    theme.PIN_CIRCLE_RADIUS_X             = 3
    theme.PIN_CIRCLE_RADIUS_Y             = 3
    theme.PIN_QUAD_SIDE_LENGTH_X          = 3
    theme.PIN_QUAD_SIDE_LENGTH_Y          = 3
    theme.PIN_TRIANGLE_SIDE_LENGTH_X      = 3
    theme.PIN_TRIANGLE_SIDE_LENGTH_Y      = 3
    theme.PIN_LINE_THICKNESS_X            = 1
    theme.PIN_LINE_THICKNESS_Y            = 1
    theme.PIN_HOVER_RADIUS_X              = 10
    theme.PIN_HOVER_RADIUS_Y              = 10
    theme.PIN_OFFSET_X                    = 0
    theme.PIN_OFFSET_Y                    = 0

    # Plot style
    #
    theme.LINE_WEIGHT_X                   = 1
    theme.LINE_WEIGHT_Y                   = 1
    theme.MARKER_X                        = 1
    theme.MARKER_Y                        = 1
    theme.MARKER_SIZE_X                   = 1
    theme.MARKER_SIZE_Y                   = 1
    theme.MARKER_WEIGHT_X                 = 1
    theme.MARKER_WEIGHT_Y                 = 1
    theme.FILL_ALPHA_X                    = 1
    theme.FILL_ALPHA_Y                    = 1
    theme.ERROR_BAR_SIZE_X                = 1
    theme.ERROR_BAR_SIZE_Y                = 1
    theme.ERROR_BAR_WEIGHT_X              = 1
    theme.ERROR_BAR_WEIGHT_Y              = 1
    theme.DIGITAL_BIT_HEIGHT_X            = 1
    theme.DIGITAL_BIT_HEIGHT_Y            = 1
    theme.DIGITAL_BIT_GAP_X               = 1
    theme.DIGITAL_BIT_GAP_Y               = 1
    theme.PLOT_BORDER_SIZE_X              = 1
    theme.PLOT_BORDER_SIZE_Y              = 1
    theme.MINOR_ALPHA_X                   = 1
    theme.MINOR_ALPHA_Y                   = 1
    theme.MAJOR_TICK_LEN_X                = 1
    theme.MAJOR_TICK_LEN_Y                = 1
    theme.MINOR_TICK_LEN_X                = 1
    theme.MINOR_TICK_LEN_Y                = 1
    theme.MAJOR_TICK_SIZE_X               = 1
    theme.MAJOR_TICK_SIZE_Y               = 1
    theme.MINOR_TICK_SIZE_X               = 1
    theme.MINOR_TICK_SIZE_Y               = 1
    theme.MAJOR_GRID_SIZE_X               = 1
    theme.MAJOR_GRID_SIZE_Y               = 1
    theme.MINOR_GRID_SIZE_X               = 1
    theme.MINOR_GRID_SIZE_Y               = 1
    theme.PLOT_PADDING_X                  = 1
    theme.PLOT_PADDING_Y                  = 1
    theme.LABEL_PADDING_X                 = 1
    theme.LABEL_PADDING_Y                 = 1
    theme.LEGEND_PADDING_X                = 1
    theme.LEGEND_PADDING_Y                = 1
    theme.LEGEND_INNER_PADDING_X          = 1
    theme.LEGEND_INNER_PADDING_Y          = 1
    theme.LEGEND_SPACING_X                = 1
    theme.LEGEND_SPACING_Y                = 1
    theme.MOUSE_POS_PADDING_X             = 1
    theme.MOUSE_POS_PADDING_Y             = 1
    theme.ANNOTATION_PADDING_X            = 1
    theme.ANNOTATION_PADDING_Y            = 1
    theme.FIT_PADDING_X                   = 1
    theme.FIT_PADDING_Y                   = 1
    theme.PLOT_DEFAULT_SIZE_X             = 1
    theme.PLOT_DEFAULT_SIZE_Y             = 1
    theme.PLOT_MIN_SIZE_X                 = 1
    theme.PLOT_MIN_SIZE_Y                 = 1

    # Core colors
    #

    theme.TEXT                            = palette.DARK_GREY_MID
    theme.TEXT_DISABLED                   = palette.LIGHT_GREY_SHADE_5
    theme.TEXT_SELECTED_BG                = palette.LIGHT_GREY_MID

    theme.WINDOW_BG                       = palette.LIGHT_GREY_TINT_4
    theme.CHILD_BG                        = palette.LIGHT_GREY_TINT_4
    theme.POPUP_BG                        = palette.LIGHT_GREY_TINT_4
    theme.MODAL_WINDOW_DIM_BG             = palette.LIGHT_GREY_TINT_4

    theme.NAV_HIGHLIGHT                   = palette.LIGHT_GREY_TINT_4
    theme.NAV_WINDOWING_DIM_BG            = palette.LIGHT_GREY_TINT_4
    theme.NAV_WINDOWING_HIGHLIGHT         = palette.LIGHT_GREY_TINT_4

    theme.DOCKING_EMPTY_BG                = palette.LIGHT_GREY_TINT_4
    theme.DOCKING_PREVIEW                 = palette.LIGHT_GREY_TINT_4

    theme.DRAG_DROP_TARGET                = palette.LIGHT_GREY_TINT_4

    theme.TITLE_BG                        = palette.DARK_GREY_MID
    theme.TITLE_BG_ACTIVE                 = palette.DARK_GREY_MID
    theme.TITLE_BG_COLLAPSED              = palette.DARK_GREY_MID

    theme.MENU_BAR_BG                     = palette.LIGHT_GREY_TINT_4

    theme.FRAME_BG                        = palette.LIGHT_GREY_TINT_4
    theme.FRAME_BG_ACTIVE                 = palette.BACKGROUND_WHITE
    theme.FRAME_BG_HOVERED                = palette.BACKGROUND_WHITE

    theme.BORDER                          = palette.LIGHT_GREY_TINT_4
    theme.BORDER_SHADOW                   = palette.LIGHT_GREY_TINT_3

    theme.SCROLLBAR_BG                    = palette.LIGHT_GREY_TINT_4
    theme.SCROLLBAR_GRAB                  = palette.LIGHT_GREY_TINT_3
    theme.SCROLLBAR_GRAB_ACTIVE           = palette.LIGHT_GREY_TINT_2
    theme.SCROLLBAR_GRAB_HOVERED          = palette.LIGHT_GREY_TINT_1

    theme.RESIZE_GRIP                     = palette.LIGHT_GREY_TINT_2
    theme.RESIZE_GRIP_ACTIVE              = palette.LIGHT_GREY_TINT_1
    theme.RESIZE_GRIP_HOVERED             = palette.LIGHT_GREY_TINT_2

    theme.HEADER                          = palette.LIGHT_GREY_TINT_4
    theme.HEADER_ACTIVE                   = palette.LIGHT_GREY_TINT_4
    theme.HEADER_HOVERED                  = palette.LIGHT_GREY_TINT_4

    theme.CHECK_MARK                      = palette.LIGHT_GREY_TINT_4

    theme.BUTTON                          = palette.LIGHT_GREY_TINT_4
    theme.BUTTON_ACTIVE                   = palette.LIGHT_GREY_TINT_4
    theme.BUTTON_HOVERED                  = palette.LIGHT_GREY_TINT_4

    theme.SEPARATOR                       = palette.LIGHT_GREY_TINT_2
    theme.SEPARATOR_ACTIVE                = palette.LIGHT_GREY_TINT_2
    theme.SEPARATOR_HOVERED               = palette.LIGHT_GREY_TINT_2

    theme.SLIDER_GRAB                     = palette.LIGHT_GREY_TINT_1
    theme.SLIDER_GRAB_ACTIVE              = palette.LIGHT_GREY_TINT_1

    theme.TAB                             = palette.LIGHT_GREY_TINT_4
    theme.TAB_ACTIVE                      = palette.LIGHT_GREY_TINT_4
    theme.TAB_HOVERED                     = palette.LIGHT_GREY_TINT_4
    theme.TAB_UNFOCUSED                   = palette.LIGHT_GREY_TINT_4
    theme.TAB_UNFOCUSED_ACTIVE            = palette.LIGHT_GREY_TINT_4

    theme.TABLE_BORDER_LIGHT              = palette.LIGHT_GREY_TINT_4
    theme.TABLE_BORDER_STRONG             = palette.LIGHT_GREY_TINT_4
    theme.TABLE_HEADER_BG                 = palette.LIGHT_GREY_TINT_4
    theme.TABLE_ROW_BG                    = palette.LIGHT_GREY_TINT_4
    theme.TABLE_ROW_BG_ALT                = palette.LIGHT_GREY_TINT_4

    theme.PLOT_HISTOGRAM                  = palette.LIGHT_GREY_TINT_4
    theme.PLOT_HISTOGRAM_HOVERED          = palette.LIGHT_GREY_TINT_4
    theme.PLOT_LINES                      = palette.LIGHT_GREY_TINT_4
    theme.PLOT_LINES_HOVERED              = palette.LIGHT_GREY_TINT_4


    # Node colors
    #

    theme.GRID_BACKGROUND                 = palette.BACKGROUND_WHITE
    theme.GRID_LINE                       = palette.LIGHT_GREY_TINT_4

    theme.NODE_OUTLINE                    = palette.LIGHT_GREY_TINT_3
    theme.NODE_BACKGROUND                 = palette.LIGHT_GREY_TINT_4
    theme.NODE_BACKGROUND_HOVERED         = palette.LIGHT_GREY_TINT_3
    theme.NODE_BACKGROUND_SELECTED        = palette.LIGHT_GREY_TINT_3

    theme.TITLE_BAR                       = palette.LIGHT_GREY_TINT_3
    theme.TITLE_BAR_HOVERED               = palette.LIGHT_GREY_TINT_2
    theme.TITLE_BAR_SELECTED              = palette.ACCENT_A

    theme.PIN                             = palette.LIGHT_GREY_MID
    theme.PIN_HOVERED                     = palette.ACCENT_A

    theme.LINK                            = palette.LIGHT_GREY_TINT_1
    theme.LINK_HOVERED                    = palette.LIGHT_GREY_MID
    theme.LINK_SELECTED                   = palette.ACCENT_A

    theme.BOX_SELECTOR                    = palette.ACCENT_A
    theme.BOX_SELECTOR_OUTLINE            = palette.ACCENT_A


    # Plot colors
    #

    theme.LINE                            = palette.BACKGROUND_WHITE
    theme.FILL                            = palette.BACKGROUND_WHITE
    theme.MARKEROUTLINE                   = palette.BACKGROUND_WHITE
    theme.MARKERFILL                      = palette.BACKGROUND_WHITE
    theme.ERRORBAR                        = palette.BACKGROUND_WHITE

    theme.FRAMEBG                         = palette.BACKGROUND_WHITE
    theme.PLOTBG                          = palette.BACKGROUND_WHITE
    theme.PLOTBORDER                      = palette.BACKGROUND_WHITE

    theme.LEGENDBG                        = palette.BACKGROUND_WHITE
    theme.LEGENDBORDER                    = palette.BACKGROUND_WHITE
    theme.LEGENDTEXT                      = palette.BACKGROUND_WHITE

    theme.TITLETEXT                       = palette.BACKGROUND_WHITE
    theme.INLAYTEXT                       = palette.BACKGROUND_WHITE

    theme.XAXIS                           = palette.BACKGROUND_WHITE
    theme.XAXISGRID                       = palette.BACKGROUND_WHITE

    theme.YAXIS                           = palette.BACKGROUND_WHITE
    theme.YAXISGRID                       = palette.BACKGROUND_WHITE
    theme.YAXIS2                          = palette.BACKGROUND_WHITE
    theme.YAXISGRID2                      = palette.BACKGROUND_WHITE
    theme.YAXIS3                          = palette.BACKGROUND_WHITE
    theme.YAXISGRID3                      = palette.BACKGROUND_WHITE

    theme.SELECTION                       = palette.BACKGROUND_WHITE
    theme.QUERY                           = palette.BACKGROUND_WHITE
    theme.CROSSHAIRS                      = palette.BACKGROUND_WHITE

    return theme