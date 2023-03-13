# -*- coding: utf-8 -*-
"""
Functional specification for the stableflow.test.util module.

"""


# =============================================================================
class SpecifySimplePipeline:
    """
    Spec for the simple_pipeline function.

    """

    # -------------------------------------------------------------------------
    def it_returns_valid_configuration(self):
        """
        simple_pipeline returns a valid configuration dict.

        """
        import stableflow.test.util
        import stableflow.cfg.validate
        cfg = stableflow.test.util.simple_pipeline(
                            repr           = 'py_dill',
                            iface          = 'step',
                            is_closed_loop = False,
                            proc_a         = {'node_a': simple_counter,
                                              'node_b': simple_messager})
        stableflow.cfg.validate.normalized(cfg)


# -----------------------------------------------------------------------------
def simple_counter(inputs, state, outputs):  # pylint: disable=W0613
    """
    Step function for a simple test node that counts to ten.

    """
    if 'count' not in state:
        state['count'] = 0
    else:
        state['count'] += 1
    outputs['output']['count'] = state['count']
    if state['count'] >= 10:
        import stableflow.exception  # pylint: disable=C0415
        return stableflow.exception.GracefulHalt(0)


# -----------------------------------------------------------------------------
def simple_messager(inputs, state, outputs):  # pylint: disable=W0613
    """
    Step function for a test node that prints a message after ten steps.

    """
    import stableflow.test.util
    if inputs['input']['count'] >= 10:
        stableflow.test.util.send(message = 'TEST OK')
        import stableflow.exception  # pylint: disable=C0415
        raise stableflow.exception.GracefulHalt(0)
