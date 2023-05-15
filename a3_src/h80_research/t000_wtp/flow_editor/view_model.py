import collections
import collections.abc
import copy
import functools
import sys


# =============================================================================
class ViewModel():
    """
    DearPyGui view model.

    """

    # ------------------------------------------------------------------------
    def __init__(self, dpg, model = None):
        """
        """
        if model is None:
            model = LiveMap()
        self._dpg  = dpg
        self.model = model

    # ------------------------------------------------------------------------
    def bind(self,
             tag,                    # UI widget tag
             key            = None,  # Key in view model
             ui_property    = 'value',
             get_ui_changes = True,
             ui_callback    = 'callback'):
        """
        One directional, bidirectional, TODO: Single shot.

        """
        if key is None:
            key = tag

        # TODO: RESOLVE DOTTED PATHS GIVEN AS KEY

        if ui_property == 'value':
            def set_ui_fcn(value):
                self._dpg.set_value(item = tag, value = value)

        else:
            def set_ui_fcn(value):
                self._dpg.configure_item(item = tag, **{ui_property: val})

        self.model.add_callback(key = key, callback = set_ui_fcn)

        if get_ui_changes:

            def get_ui_fcn(sender, app_data, ctx):
                self.model[key] = app_data

            self._dpg.configure_item(item = tag,
                                     **{ui_callback: get_ui_fcn})


