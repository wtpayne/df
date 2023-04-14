# -*- coding: utf-8 -*-
"""
PDF renderer component.

Read PDF files and output a list of images.

"""


import os
import itertools

import pdf2image
import pdf2image.exceptions
import pytesseract

import xact.util


# -----------------------------------------------------------------------------
def reset(runtime, cfg, inputs, state, outputs):
    """
    Reset the PDF renderer component.

    """
    pass


# -----------------------------------------------------------------------------
def step(inputs, state, outputs):
    """
    Step the pdf renderer component.

    """
    xact.util.clear_outputs(
                    outputs             = outputs,
                    iter_name_output    = ('image',),
                    iter_field_to_clear = ('list', ))

    if not inputs['hexdigest']['ena']:
        return

    for map_item in inputs['hexdigest']['list']:
        try:
            iter_page = pdf2image.convert_from_path(map_item['filepath'])
        except (pdf2image.exceptions.PopplerNotInstalledError,
                pdf2image.exceptions.PDFInfoNotInstalledError,
                pdf2image.exceptions.PDFPageCountError,
                pdf2image.exceptions.PDFSyntaxError,
                pdf2image.exceptions.PDFPopplerTimeoutError):
            continue
        else:
            for (idx_image, image) in enumerate(iter_page):
                outputs['image']['list'].append({
                                            'filepath':  map_item['filepath'],
                                            'hexdigest': map_item['hexdigest'],
                                            'idx_image': idx_image,
                                            'image':     image})

    if outputs['image']['list']:
        outputs['image']['ena'] = True
