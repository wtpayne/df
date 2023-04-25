# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.openai.client

"""


import inspect

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture
def cfg_valid():
    """
    """
    return {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'model':             'gpt-3.5-turbo',
            'temperature':       0.7,
            'n':                 1,
            'stream':            'test_stream',
            'presence_penalty':  'test_presence_penalty',
            'frequency_penalty': 'test_frequency_penalty',
            'user':              'test_user'}}

# -----------------------------------------------------------------------------
@pytest.fixture
def cfg_invalid():
    """
    """
    return {}



# =============================================================================
class SpecifyOpenAiClient:
    """
    Spec for openai client functionality.

    """

    # -------------------------------------------------------------------------
    def it_supports_import_of_openai_client(self):
        """
        fl.net.openai.client can be imported.

        """
        import fl.net.openai.client

    # -------------------------------------------------------------------------
    def it_supports_creation_of_the_main_coroutine(self, cfg_valid):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        client = fl.net.openai.client.coro(cfg = cfg_valid)
        assert inspect.isgenerator(client)

    # -------------------------------------------------------------------------
    def it_validates_provided_configuration(self, cfg_invalid):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        with pytest.raises(AssertionError):
            fl.net.openai.client.coro(cfg = cfg_invalid)

