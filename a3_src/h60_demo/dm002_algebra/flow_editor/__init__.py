# -*- coding: utf-8 -*-
"""
"""


import importlib.metadata


try:
    __version__ = importlib.metadata.version('flow_editor')
except importlib.metadata.PackageNotFoundError:
    __version__ = '0.0.1'


