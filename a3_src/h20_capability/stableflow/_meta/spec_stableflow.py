# -*- coding: utf-8 -*-
"""
Functional specification for stableflow.

"""


import click.testing
import pytest


# =============================================================================
class SpecifyStableflow:
    """
    Spec for stableflow at a system level.

    """

    # -------------------------------------------------------------------------
    def it_supports_import_of_stableflow_proc_package(self):
        """
        stableflow.proc can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """
        import stableflow.proc

    # -------------------------------------------------------------------------
    def it_supports_import_of_stableflow_node_package(self):
        """
        stableflow.node can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """
        import stableflow.node

    # -------------------------------------------------------------------------
    def it_supports_import_of_stableflow_queue_package(self):
        """
        stableflow.queue can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """
        import stableflow.queue

    # -------------------------------------------------------------------------
    def it_supports_import_of_stableflow_signal_package(self):
        """
        stableflow.signal can be imported.

        Failure of this test usually indicates a
        problem with building native extensions.

        """
        import stableflow.signal

    # -------------------------------------------------------------------------
    def it_supports_single_process_execution(self):
        """
        stableflow.cli.command.grp_main supports single process execution.

        """
        import stableflow.test.util
        stableflow.test.util.run(
                env = stableflow.test.util.env(filepath = __file__),
                cfg = stableflow.test.util.simple_pipeline(
                            repr           = 'py_dill',
                            iface          = 'step',
                            is_closed_loop = False,
                            proc_a         = {'node_a': simple_counter,
                                              'node_b': simple_messager}),
                expected_output = {stableflow.test.util.TEST_PORT: 'TEST OK'},
                is_local        = True)

    # -------------------------------------------------------------------------
    def it_supports_multiprocess_execution(self):
        """
        stableflow.cli.command.grp_main supports multiprocess execution.

        """
        import stableflow.test.util
        stableflow.test.util.run(
                env = stableflow.test.util.env(filepath = __file__),
                cfg = stableflow.test.util.simple_pipeline(
                            repr           = 'py_dill',
                            iface          = 'step',
                            is_closed_loop = False,
                            proc_a         = {'node_a': simple_counter},
                            proc_b         = {'node_b': simple_messager}),
                expected_output = {stableflow.test.util.TEST_PORT: 'TEST OK'},
                is_local        = False)


    # -------------------------------------------------------------------------
    def it_supports_functions_specified_as_source_strings(self):
        """
        stableflow.cli.command.grp_main supports nodes specified as source strings.

        """
        import stableflow.test.util
        stableflow.test.util.run(
                env = stableflow.test.util.env(filepath = __file__),
                cfg = stableflow.test.util.simple_pipeline(
                            repr           = 'py_src',
                            iface          = 'step',
                            is_closed_loop = False,
                            proc_a         = {'node_a': simple_counter,
                                              'node_b': simple_messager}),
                expected_output = {stableflow.test.util.TEST_PORT: 'TEST OK'},
                is_local        = True)

    # -------------------------------------------------------------------------
    def it_supports_coroutines(self):
        """
        stableflow.cli.command.grp_main supports nodes specified as coroutines.

        """
        import stableflow.test.util
        stableflow.test.util.run(
                env = stableflow.test.util.env(filepath = __file__),
                cfg = stableflow.test.util.simple_pipeline(
                            repr           = 'py_dill',
                            iface          = 'coro',
                            is_closed_loop = False,
                            proc_a         = {'node_a': coro_counter,
                                              'node_b': coro_messager}),
                expected_output = {stableflow.test.util.TEST_PORT: 'TEST OK'},
                is_local        = True)


    # -------------------------------------------------------------------------
    def it_supports_feedback_loops(self):
        """
        stableflow.cli.command.grp_main supports nodes arranged in a feedback loop.

        """
        import stableflow.test.util
        stableflow.test.util.run(
                env = stableflow.test.util.env(filepath = __file__),
                cfg = stableflow.test.util.simple_pipeline(
                            repr           = 'py_dill',
                            iface          = 'coro',
                            is_closed_loop = True,
                            proc_a         = {'node_a': feedback_counter,
                                              'node_b': feedback_decisioner}),
                expected_output = {stableflow.test.util.TEST_PORT: 'TEST OK'},
                is_local        = True)


# =============================================================================
class SpecifyGrpMain:
    """
    Spec for the stableflow.cli.command.grp_main command group.

    """

    # -------------------------------------------------------------------------
    def it_displays_help_text_when_called_with_no_args(
                                                self, expected_help_text_main):
        """
        stableflow.cli.command.grp_main prints help text when called with no args.

        """
        import stableflow.cli.command  # pylint: disable=C0415

        runner        = click.testing.CliRunner()
        response      = runner.invoke(stableflow.cli.command.grp_main)
        response_text = ' '.join(line.strip() for line in
                                        response.output.splitlines())
        expected_text = ' '.join(line.strip() for line in
                                        expected_help_text_main.splitlines())

        assert response.exit_code == 0
        assert response_text.startswith(expected_text)

    # -------------------------------------------------------------------------
    def it_displays_help_text_when_called_with_help_arg(
                                                self, expected_help_text_main):
        """
        stableflow.cli.command.grp_main prints help text when called with a help arg.

        """
        import stableflow.cli.command  # pylint: disable=C0415

        runner        = click.testing.CliRunner()
        response      = runner.invoke(stableflow.cli.command.grp_main, ['--help'])
        response_text = ' '.join(line.strip() for line in
                                        response.output.splitlines())
        expected_text = ' '.join(line.strip() for line in
                                        expected_help_text_main.splitlines())

        assert response.exit_code == 0
        assert response_text.startswith(expected_text)


# -----------------------------------------------------------------------------
@pytest.fixture
def expected_help_text_main():
    """
    Return the expected help text for stableflow.cli.command.grp_main.

    """
    return (
        'Usage: main [OPTIONS] COMMAND [ARGS]...\n\n'
        '  Stableflow command line interface.\n\n'
        '  The stableflow command line interface provides the\n'
        '  user with the ability to start, stop, pause\n'
        '  and step a stableflow system.\n\n'
        '  A stableflow system is composed of one or more\n'
        '  process-hosts, each of which contains one or\n'
        '  more processes, each of which contains one or\n'
        '  more compute nodes.\n\n'
        'Options:\n'
        '  --version  Show the version and exit.\n'
        '  --help     Show this message and exit.\n\n'
        'Commands:\n'
        '  system  Control the system as a whole.\n'
        '  host    Control a single process host.\n'

    )


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
        return (stableflow.signal.exit_ok_controlled,)


# -----------------------------------------------------------------------------
def simple_messager(inputs, state, outputs):  # pylint: disable=W0613
    """
    Step function for a test node that prints a message after ten steps.

    """
    import stableflow.test.util
    if inputs['input']['count'] >= 10:
        stableflow.test.util.send(message = 'TEST OK')
        import stableflow.exception  # pylint: disable=C0415
        return (stableflow.signal.exit_ok_controlled,)


# -----------------------------------------------------------------------------
def coro_counter(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine for a simple test node that counts to ten.

    """
    import stableflow.signal
    count  = -1
    signal = (None,)
    while True:
        inputs = yield (outputs, signal)
        count += 1
        outputs['output']['count'] = count
        if count >= 10:
            signal = (stableflow.signal.exit_ok_controlled,)


# -----------------------------------------------------------------------------
def coro_messager(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine for a test node that prints a message after ten steps.

    """
    import stableflow.signal
    import stableflow.test.util
    signal = (None,)
    while True:
        inputs = yield (outputs, signal)
        if inputs['input']['count'] >= 10:
            stableflow.test.util.send(message = 'TEST OK')
            signal = (stableflow.signal.exit_ok_controlled,)


# -----------------------------------------------------------------------------
def feedback_counter(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine for a simple test node that counts to ten.

    """
    import stableflow.signal
    import stableflow.test.util
    count = 0
    while True:
        outputs['output']['count'] = count
        inputs = yield (outputs, None)
        count += 1
        if inputs['input']['do_halt']:
            stableflow.test.util.send(message = 'TEST OK')
            signal = (stableflow.signal.exit_ok_controlled,)
            yield (outputs, signal)


# -----------------------------------------------------------------------------
def feedback_decisioner(runtime, cfg, inputs, state, outputs):  # pylint: disable=W0613
    """
    Coroutine for a test node that decides to halt after ten steps.

    """
    outputs['output']['do_halt'] = False
    signal = (None,)
    while True:
        inputs = yield (outputs, signal)
        if inputs['input']['count'] >= 10:
            outputs['output']['do_halt'] = True
