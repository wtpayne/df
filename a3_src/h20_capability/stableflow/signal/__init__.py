# -*- coding: utf-8 -*-
"""
Package of stableflow control signals.

These signals are understood by the runtime.

---
type:
    python_extension

name_extension:
    stableflow.signal
...

"""


import cython
import signal


continue_ok:        cython.int = 100
exit_ex_immediate:  cython.int = int(signal.SIGKILL)  # Immediate exceptional shutdown (e.g. fatal nonrecoverable error).
exit_ex_controlled: cython.int = 101                  # Controlled exceptional shutdown.
exit_ok_controlled: cython.int = int(signal.SIGTERM)  # Controlled nominal shutdown.
control_reset:      cython.int = 102                  # Reset and retry
control_pause:      cython.int = int(signal.SIGUSR1)  #
control_step:       cython.int = int(signal.SIGUSR2)

exit = (
    exit_ex_immediate,
    exit_ex_controlled,
    exit_ok_controlled)

reset = (
    control_reset,)

immediate = (
    exit_ex_immediate,)

controlled = (
    exit_ex_controlled,
    exit_ok_controlled,
    control_reset,
    control_pause,
    control_step)