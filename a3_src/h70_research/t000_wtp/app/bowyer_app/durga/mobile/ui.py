# -*- coding: utf-8 -*-
"""
Mobile UI component.

"""


import kivy.app
import kivy.uix.widget
import multiprocessing


# -----------------------------------------------------------------------------
def coro(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Screen control UI component coroutine.

    """
    signal                       = None

    # outputs['uidata']['ena']     = False
    # outputs['uidata']['list']    = []

    # outputs['resources']['ena']  = False
    # outputs['resources']['list'] = []

    map_queues = dict(
        queue_updates = multiprocessing.Queue(), # From backend to frontend UI
        queue_events  = multiprocessing.Queue(), # From frontend UI to backend
    )

    process_app = multiprocessing.Process(
                                    target = _kivi_app,
                                    args   = (cfg, map_queues),
                                    name   = 'durga-mobile-app',
                                    daemon = True)
    process_app.start()

    while True:

        inputs = yield (outputs, signal)

        if not inputs['control']['ena']:
            continue

        # outputs['uidata']['ena']     = False
        # outputs['uidata']['list']    = []

        # outputs['resources']['ena']  = False
        # outputs['resources']['list'] = []


# -----------------------------------------------------------------------------
def _kivi_app(cfg, map_queues):

    import bowyer.app.durga.mobile.app
    bowyer.app.durga.mobile.app.main(cfg)