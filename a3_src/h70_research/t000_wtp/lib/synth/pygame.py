# -*- coding: utf-8 -*-
"""
Xact pygame component.

"""


import os
import sys

import pygame


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the pygame component.

    """
    state['headless'] = cfg.get('headless', False)
    state['width']    = cfg.get('width',    512)
    state['height']   = cfg.get('height',   512)
    state['size']     = (state['width'], state['height'])

    if state['headless']:
        os.environ['SDL_VIDEODRIVER'] = 'dummy'
        pygame.init()
        pygame.display.set_mode((1,1))
        state['screen'] = pygame.Surface(state['size'], pygame.SRCALPHA, 32)
        pygame.draw.rect(state['screen'],
                         (0,0,0), (0, 0, state['width'], state['height']), 0)

    else:
        pygame.init()
        state['screen'] = pygame.display.set_mode(state['size'])


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the pygame component.

    """
    black = 0, 0, 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    state['screen'].fill((0,0,0))
    pygame.display.flip()

