# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.openai.client

"""


import inspect
import time

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture
def cfg_valid_bit_enabled():
    """
    Return some valid configuration.

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
            'user':              'test_user',
            'metadata':          dict()}}


# -----------------------------------------------------------------------------
@pytest.fixture
def cfg_invalid():
    """
    Return some invalid configuration.

    """
    return {}


# -----------------------------------------------------------------------------
@pytest.fixture
def expected_bit_response():
    """
    """
    import fl.net.openai.client
    return {'request':   {},  # Needs to be filled in the test case.
            'response':  fl.net.openai.client.built_in_test_response(),
            'error':     None,
            'metadata':  {}}


# =============================================================================
class SpecifyFlNetOpenAiClient:
    """
    Spec for the fl.net.openai.client package.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_openai_client(self):
        """
        fl.net.openai.client can be imported.

        """
        import fl.net.openai.client

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_creation_of_the_main_coroutine(self,
                                                   cfg_valid_bit_enabled):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        client = fl.net.openai.client.coro(cfg = cfg_valid_bit_enabled)
        assert inspect.isgenerator(client)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response(self,
                                        cfg_valid_bit_enabled,
                                        expected_bit_response):
        """
        fl.net.openai.client coro() yields the expected BIT response.

        """
        import fl.net.openai.client
        client = fl.net.openai.client.coro(cfg = cfg_valid_bit_enabled)

        test_list_messages       = ['test_request']
        item_request             = {'messages': test_list_messages}
        list_item_request        = [item_request]
        list_item_result         = list()
        max_iterations           = 500
        delay_per_iteration_secs = 0.01
        for _ in range(max_iterations):
            (list_item_result, list_item_error) = client.send(list_item_request)
            list_item_request.clear()
            if len(list_item_result) == 0:
                time.sleep(delay_per_iteration_secs)
                continue
            else:
                break

        expected_bit_response['request'] = cfg_valid_bit_enabled['default']
        expected_bit_response['request'].pop('metadata', None)
        expected_bit_response['request']['messages'] = test_list_messages

        assert len(list_item_result) == 1
        assert list_item_result[0] == expected_bit_response


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_validates_provided_configuration(self, cfg_invalid):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        with pytest.raises(AssertionError):
            fl.net.openai.client.coro(cfg = cfg_invalid)

