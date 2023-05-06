# -*- coding: utf-8 -*-
"""
The notification_server module supports using the gtk event loop.

---
type:
    python_module

validation_level:
    v00_minimum

protection:
    k00_public

copyright:
    "Copyright 2023 William Payne"

license:
    "Licensed under the Apache License, Version 2.0 (the License);
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License."

requirements:
    "This design document may contain any number of requirements
    items embedded in comment blocks. Each requirements item
    that is present shall have one formal requirement statement
    with one modal verb. The modal verb shall be interpreted
    in accordance with iso29148:2011

    SHALL indicates a mandatory binding provision, the fulfillment
    of which must be proven through an appropriate test.

    WILL indicates a statement of fact; futurity; a declaration
    of purpose; or to establish a context or a limitation of use.
    These statements are not manadatory and not binding.

    SHOULD indicates a preference; a goal or an advantageous
    quality. These statements are not mandatory and not binding.

    MAY is used to grant permission or to make a suggestion.
    These statements are not mandatory and not binding."
...
"""


import signal
import sys

import da.monitor.desktop.ipc

import gi
gi.require_version('AppIndicator3', '0.1')
gi.require_version('Gtk',           '3.0')
gi.require_version('Notify',        '0.7')
import gi.repository.AppIndicator3                                       # noqa
import gi.repository.GLib                                                # noqa
import gi.repository.GObject                                             # noqa
import gi.repository.Gtk                                                 # noqa
import gi.repository.Notify                                              # noqa


# -----------------------------------------------------------------------------
def main(short_name):
    """
    Configure the notification_server application and enter the GTK main loop.

    """
    indicator = _app_indicator(short_name)
    _reconfigure(indicator, msg = None)
    _listen_to_stdin(indicator)

    # GTK Main loop.
    gi.repository.GObject.threads_init()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    return gi.repository.Gtk.main()


# -----------------------------------------------------------------------------
def _app_indicator(short_name):
    """
    Return the appindicator.

    """
    icon_name     = 'face-plain'
    app_indicator = gi.repository.AppIndicator3
    category      = app_indicator.IndicatorCategory.APPLICATION_STATUS
    indicator     = app_indicator.Indicator.new(short_name,
                                                icon_name,
                                                category)
    indicator.set_menu(gi.repository.Gtk.Menu())
    return indicator


# -----------------------------------------------------------------------------
def _listen_to_stdin(indicator):
    """
    Listen to stdin and update the indicator based on messages.

    """
    # -------------------------------------------------------------------------
    def _callback(stream, cb_condition, indicator):     # pylint: disable=W0613
        """
        Handle data received on standard input.

        """
        msg = da.monitor.desktop.ipc.read(stream)
        _reconfigure(indicator, msg)

    glib = gi.repository.GLib
    glib.io_add_watch(sys.stdin, glib.IO_IN | glib.IO_HUP, _callback,
                      indicator)


# -----------------------------------------------------------------------------
def _reconfigure(indicator, msg):
    """
    Reconfigure the specified indicator.

    """
    if msg is None:
        status   = '[WAIT]'
        build_id = 'pending...'
        icon     = 'face-smile-big'
    else:
        (status, build_id, icon) = _parse(msg)

    # -------------------------------------------------------------------------
    def _browse_current_log_files(_):
        """
        Closure to browse current log files.

        """
        pass
        # _browse_log_files(msg)

    # -------------------------------------------------------------------------
    def _open_current_html_log(_):
        """
        Closure to open current html log.

        """
        pass
        # _open_html_log(msg)

    gtk        = gi.repository.Gtk
    menu_root  = indicator.get_menu()

    menu_build = gtk.Menu()

    menu_file_browser = gtk.MenuItem("Browse log files")
    menu_file_browser.connect("activate", _browse_current_log_files)

    menu_html_log = gtk.MenuItem("Open HTML log")
    menu_html_log.connect("activate", _open_current_html_log)

    menu_build.append(menu_file_browser)
    menu_build.append(menu_html_log)
    menu_build.show_all()

    item_build = gtk.MenuItem(status + ' ' + build_id)
    item_build.set_submenu(menu_build)
    menu_root.append(item_build)
    menu_root.show_all()

    status_active = gi.repository.AppIndicator3.IndicatorStatus.ACTIVE
    indicator.set_status(status_active)
    indicator.set_icon(icon)


# -----------------------------------------------------------------------------
def _parse(msg):
    """
    Return a notification title, body and icon from the specified message data.

    """
    if msg['is_conforming']:
        status   = '[OK]'
        build_id = msg['build_id']
        icon     = 'face-smile-big'
    else:
        status   = '[ERR]'
        build_id = msg['build_id']
        icon     = 'face-sad'

    return (status, build_id, icon)
