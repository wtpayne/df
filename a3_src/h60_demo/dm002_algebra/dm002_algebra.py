#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
"""


import sys

import flow_editor.cli


# -----------------------------------------------------------------------------
def main():
    """
    Run the flow_editor command line interface.

    """
    return flow_editor.cli.main()  # Uses sys.argv


# -----------------------------------------------------------------------------
if __name__ == '__main__':
    sys.exit(main())