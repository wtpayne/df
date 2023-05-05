# -*- coding: utf-8 -*-
"""
Utility functions for building IMGUI user interfaces.

"""


import collections
import contextlib
import ctypes
import functools
import sys
import re

import cv2
import imgui
import imgui.integrations.sdl2
import numpy
import OpenGL.GL
import sdl2

import xact.signal


# -----------------------------------------------------------------------------
def route(iter_msg, iter_keys):
    """
    Return a mapping from a key to a list of matching messages.

    """

    map_msg = collections.defaultdict(list)
    for msg in iter_msg:
        pattern = msg['dst'][0]
        for key in iter_keys:
            if re.match(pattern, key[0]) is not None:
                map_msg[key].append(msg)
    return map_msg


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def background_context(ctx_ui, name):
    """
    Context manager for drawing a background image.

    """

    (width, height) = get_sdl_window_size(sdl_window = ctx_ui.window)
    imgui.set_next_window_position(0, 0)
    imgui.set_next_window_size(width, height)
    imgui.begin(name, False,
                  imgui.WINDOW_NO_TITLE_BAR
                | imgui.WINDOW_NO_RESIZE
                | imgui.WINDOW_NO_MOVE
                | imgui.WINDOW_NO_SCROLLBAR
                | imgui.WINDOW_NO_SCROLL_WITH_MOUSE
                | imgui.WINDOW_NO_COLLAPSE
                | imgui.WINDOW_ALWAYS_AUTO_RESIZE
                | imgui.WINDOW_NO_SAVED_SETTINGS
                | imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS)

    (yield)

    imgui.end()


# -----------------------------------------------------------------------------
def get_sdl_window_size(sdl_window):
    """
    Return the (width, height) of the SDL window.

    Note that the SDL window is the
    window in which the entire App
    resides, not one of the imgui
    "windows" that are rendered
    within it.

    """
    width  = ctypes.c_int()
    height = ctypes.c_int()
    sdl2.SDL_GetWindowSize(sdl_window, width, height)
    return (width.value, height.value)


# -----------------------------------------------------------------------------
def gen_opengl_texture(img_cv2):
    """
    Load the specified image into a texture.

    """
    img_bgr    = _convert_cv2_to_bgr(img_cv2)
    img_width  = img_bgr.shape[1]
    img_height = img_bgr.shape[0]
    texture_id = OpenGL.GL.glGenTextures(1)

    OpenGL.GL.glPixelStorei(OpenGL.GL.GL_UNPACK_ALIGNMENT, 1)
    OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D,       texture_id)
    OpenGL.GL.glPixelStorei(OpenGL.GL.GL_UNPACK_ALIGNMENT, 1)
    OpenGL.GL.glTexParameteri(
            OpenGL.GL.GL_TEXTURE_2D,
            OpenGL.GL.GL_TEXTURE_MAG_FILTER,
            OpenGL.GL.GL_LINEAR)
    OpenGL.GL.glTexParameteri(
            OpenGL.GL.GL_TEXTURE_2D,
            OpenGL.GL.GL_TEXTURE_MIN_FILTER,
            OpenGL.GL.GL_LINEAR)
    OpenGL.GL.glTexImage2D(
            OpenGL.GL.GL_TEXTURE_2D,
            0,
            OpenGL.GL.GL_RGB,
            img_width,
            img_height,
            0,
            OpenGL.GL.GL_BGR,
            OpenGL.GL.GL_UNSIGNED_BYTE,
            img_bgr)
    OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D, 0)
    return texture_id


# -----------------------------------------------------------------------------
def _convert_cv2_to_bgr(img_cv2):
    """
    Convert a generic OpenCV image to BGR.

    Auto-detect a small handful
    of common source formats.

    """
    is_uint8      = img_cv2.dtype == numpy.uint8
    is_float      = img_cv2.dtype in [numpy.float32, numpy.float64]
    array_shape   = img_cv2.shape
    num_dims      = len(array_shape)

    is_bgr        = is_uint8 and num_dims == 3 and array_shape[2] == 3
    is_bgra       = is_uint8 and num_dims == 3 and array_shape[2] == 4
    is_8bit_mono  = is_uint8 and num_dims == 2
    is_float_mono = is_float and num_dims == 2

    if is_bgr:
        return img_cv2

    elif is_bgra:
        return cv2.cvtColor(img_cv2, cv2.COLOR_BGRA2BGR)

    elif is_8bit_mono:
        return cv2.cvtColor(img_cv2, cv2.COLOR_GRAY2BGR)

    elif is_float_mono:
        return cv2.cvtColor(numpy.uint8(img_cv2 * 255.0), cv2.COLOR_GRAY2BGR)

    else:
        raise ValueError('Unrecognized image data type and/or array shape.')


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def ui_context(
        id_node, id_screen, name, width, height, filepath_ttf, font_size):
    """
    Context manager for IMGUI UI setup and teardown.

    """
    window     = _configure_sdl2_window(width, height, name);
    gl_context = _configure_gl_context(window)
    imgui.create_context()
    renderer   = imgui.integrations.sdl2.SDL2Renderer(window)
    font       = _render_scaled_font_texture(renderer     = renderer,
                                             id_screen    = id_screen,
                                             filepath_ttf = filepath_ttf,
                                             font_size    = font_size)
    event_data = sdl2.SDL_Event()
    UIContext  = collections.namedtuple(
                                'UIContext', ['id_node',
                                              'window',
                                              'gl_context',
                                              'renderer',
                                              'event_data',
                                              'ui_state',
                                              'event_handlers',
                                              'frame_context'])


    try:

        ui_state       = dict()
        event_handlers = dict()

        yield UIContext(id_node        = id_node,
                        window         = window,
                        gl_context     = gl_context,
                        renderer       = renderer,
                        event_data     = event_data,
                        ui_state       = ui_state,
                        event_handlers = event_handlers,
                        frame_context  = functools.partial(
                                                _frame_context,
                                                window,
                                                renderer,
                                                event_data,
                                                ui_state,
                                                event_handlers,
                                                font))

    except xact.signal.ControlSignal:
        _clean_shutdown(window, gl_context, renderer)
        raise

    else:
        _clean_shutdown(window, gl_context, renderer)


# -----------------------------------------------------------------------------
def _render_scaled_font_texture(renderer, id_screen, filepath_ttf, font_size):
    """
    Render a font scaled appropriate to the resolution of the display.

    """
    dpi          = _get_display_dpi(screen = id_screen)
    scale        = dpi / 72.0
    size_scaled  = font_size * scale
    io           = imgui.get_io()
    glyph_range  = io.fonts.get_glyph_ranges_latin()
    font         = io.fonts.add_font_from_file_ttf(filepath_ttf,
                                                   size_scaled,
                                                   glyph_range)
    renderer.refresh_font_texture()
    io.font_global_scale = 1 / scale

    return font


# -----------------------------------------------------------------------------
def _get_display_dpi(screen):
    """
    Return the DPI value for the specified screen.

    """
    ddpi = ctypes.c_float()
    hdpi = ctypes.c_float()
    vdpi = ctypes.c_float()
    if sdl2.SDL_GetDisplayDPI(screen,
                              ctypes.byref(ddpi),
                              ctypes.byref(hdpi),
                              ctypes.byref(vdpi)):
        raise RuntimeError(
                'SDL could not get display DPI. SDL Error: {err}'.format(
                                err = sdl2.SDL_GetError().decode("utf-8")))

    return ddpi.value


# -----------------------------------------------------------------------------
def _configure_sdl2_window(width, height, name):
    """
    Configure and return the SDL2 Window.

    """

    if sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING) < 0:
        raise RuntimeError(
                'SDL could not initialize. SDL Error: {err}'.format(
                                err = sdl2.SDL_GetError().decode("utf-8")))

    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER,       1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE,         24)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_STENCIL_SIZE,       8)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_ACCELERATED_VISUAL, 1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES, 4)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_FLAGS,
                             sdl2.SDL_GL_CONTEXT_FORWARD_COMPATIBLE_FLAG)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_MINOR_VERSION, 1)
    sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONTEXT_PROFILE_MASK,
                             sdl2.SDL_GL_CONTEXT_PROFILE_CORE)

    sdl2.SDL_SetHint(sdl2.SDL_HINT_MAC_CTRL_CLICK_EMULATE_RIGHT_CLICK, b"1")
    sdl2.SDL_SetHint(sdl2.SDL_HINT_VIDEO_HIGHDPI_DISABLED,             b"1")

    window = sdl2.SDL_CreateWindow(
                            name.encode('utf-8'),
                            sdl2.SDL_WINDOWPOS_CENTERED,
                            sdl2.SDL_WINDOWPOS_CENTERED,
                            width,
                            height,
                            sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE)

    if window is None:
        raise RuntimeError(
                'Error: Window could not be created! SDL Error: {err}'.format(
                                err = sdl2.SDL_GetError().decode("utf-8")))

    return window


# -----------------------------------------------------------------------------
def _configure_gl_context(window):
    """
    Configure the GL context and return it.

    """

    gl_context = sdl2.SDL_GL_CreateContext(window)

    if gl_context is None:
        raise RuntimeError(
                'Cannot create OpenGL Context. SDL Error: {err}'.format(
                                err = sdl2.SDL_GetError().decode("utf-8")))

    sdl2.SDL_GL_MakeCurrent(window, gl_context)
    if sdl2.SDL_GL_SetSwapInterval(1) < 0:
        raise RuntimeError(
                'Unable to set VSync. SDL Error: {err}'.format(
                                err = sdl2.SDL_GetError().decode("utf-8")))

    return gl_context


# -----------------------------------------------------------------------------
@contextlib.contextmanager
def _frame_context(
                window, renderer, event_data, ui_state, event_handlers, font):
    """
    Context manager for frame setup, event handling and teardown.

    """
    _handle_events(renderer, event_data, ui_state, event_handlers)
    imgui.new_frame()
    OpenGL.GL.glClearColor(1.0, 1.0, 1.0, 1.0)
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT)

    imgui.push_font(font)

    (yield)  # Application populates PyImGui draw data during this yield.

    imgui.pop_font()

    _draw_window(window, renderer)


# -----------------------------------------------------------------------------
def _handle_events(renderer, event_data, ui_state, event_handlers):
    """
    Dispatch events to the relevant handler.

    PyImGui internal event handling is implemented
    in the renderer.process_inputs function.

    This processes input events which have been
    added using the renderer.process_event()
    function. (Data is stored internally in
    renderer.io).

    """
    while sdl2.SDL_PollEvent(ctypes.byref(event_data)) != 0:
        try:
            event_handlers[event_data.type](event_data, ui_state)
        except KeyError:
            pass

        renderer.process_event(event_data)  # Add event to renderer.io
    renderer.process_inputs()               # Process renderer.io


# -----------------------------------------------------------------------------
def _draw_window(window, renderer):
    """
    Draw the UI window to video memory.

    """
    imgui.render()
    renderer.render(imgui.get_draw_data())
    sdl2.SDL_GL_SwapWindow(window)


# -----------------------------------------------------------------------------
def _clean_shutdown(window, gl_context, renderer):
    """
    Close the window and clean up resources.

    """
    renderer.shutdown()
    sdl2.SDL_GL_DeleteContext(gl_context)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()
