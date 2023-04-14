# -*- coding: utf-8 -*-
"""
Video capture node.

"""


import cv2


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Video capture coroutine.

    """
    signal = None
    try:
        connection = int(cfg['connection'])
    except ValueError:
        connection = cfg['connection']

    if connection == 'nvarguscamerasrc':
        state['cap'] = cv2.VideoCapture(
                                gstreamer_pipeline(
                                        capture_width  = cfg['cam_width'],
                                        capture_height = cfg['cam_height'],
                                        display_width  = cfg['out_width'],
                                        display_height = cfg['out_height'],
                                        framerate      = cfg['framerate'],
                                        flip_method    = cfg['flip_method']),
                                cv2.CAP_GSTREAMER)
    else:
        cap_params   = [cv2.CAP_PROP_FRAME_WIDTH,  cfg['out_width'],
                        cv2.CAP_PROP_FRAME_HEIGHT, cfg['out_height']]
        state['cap'] = cv2.VideoCapture(connection,
                                        apiPreference = cv2.CAP_ANY,
                                        params        = cap_params)

    while True:

        inputs = yield (outputs, signal)

        if not inputs['control']['ena']:
            continue

        (is_ok, buffer) = state['cap'].read()   # OpenCV |- BGR

        for id_out in outputs.keys():
            outputs[id_out]['buff']      = buffer
            outputs[id_out]['ena']       = is_ok
            outputs[id_out]['ts_rel_us'] = inputs['control']['ts_rel_us']


# -----------------------------------------------------------------------------
def gstreamer_pipeline(capture_width  = 1280,
                       capture_height = 720,
                       display_width  = 1280,
                       display_height = 720,
                       framerate      = 60,
                       flip_method    = 0):

    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (capture_width,
           capture_height,
           framerate,
           flip_method,
           display_width,
           display_height))


# -----------------------------------------------------------------------------
def finalize(runtime, config, inputs, state, outputs):
    """
    Clean up resources.

    """
    try:
        state['cap'].release()
    except cv2.error as err:
        pass
