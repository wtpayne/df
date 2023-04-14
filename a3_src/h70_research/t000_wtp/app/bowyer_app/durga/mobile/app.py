#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Durga mobile UI app.

"""

import sys

import kivy.app
import kivy.uix.gridlayout


# =============================================================================
class NavControl(kivy.uix.gridlayout.GridLayout):

    def nav(self, var):
        print('NAV PRESSED')
        print(var)


# =============================================================================
class DurgaApp(kivy.app.App):
    """
    Durga App class.

    """
    def build(self):
        return NavControl()


# -----------------------------------------------------------------------------
def main(cfg = None):
    """
    Main function for the durga mobile UI app.

    """
    DurgaApp().run()


# -----------------------------------------------------------------------------
if __name__ == "__main__":
    sys.exit(main())