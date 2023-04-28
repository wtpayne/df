# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.openai.client

"""


import inspect
import time

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture
def template_completions_valid():
    """
    Return a valid template data structure for the completions endpoint.

    """
    return {
        'id_endpoint':  'completions',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'text-davinci-003'},
        'prompt':       'test_prompt'}


# -----------------------------------------------------------------------------
@pytest.fixture
def template_chat_completions_valid():
    """
    Return a valid template data structure for the chat completions endpoint.

    """
    return {
        'id_endpoint':  'chat_completions',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'gpt-3.5-turbo-0301'},
        'messages':     [{'role':    'system',
                          'content': 'test_content'}] }


# -----------------------------------------------------------------------------
@pytest.fixture
def template_edits_valid():
    """
    Return a valid template data structure for the edits endpoint.

    """
    return {
        'id_endpoint':  'edits',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'text-davinci-edit-001'},
        'input':        'test_input',
        'instruction':  'test_instruction' }


# -----------------------------------------------------------------------------
@pytest.fixture
def template_images_generations_valid():
    """
    Return a valid template data structure for the images_generations endpoint.

    """
    return {
        'id_endpoint':  'images_generations',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {},
        'prompt':       'prompt' }


# -----------------------------------------------------------------------------
@pytest.fixture
def template_images_edits_valid():
    """
    Return a valid template data structure for the images_edits endpoint.

    """
    return {
        'id_endpoint':  'images_edits',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'image':  'test_image'},
        'prompt':       'test_prompt'}


# -----------------------------------------------------------------------------
@pytest.fixture
def template_images_variations_valid():
    """
    Return a valid template data structure for the images_variations endpoint.

    """
    return {
        'id_endpoint':  'images_variations',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'image':  'test_image'}}


# -----------------------------------------------------------------------------
@pytest.fixture
def template_embeddings_valid():
    """
    Return a valid template data structure for the embeddings endpoint.

    """
    return {
        'id_endpoint':  'embeddings',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'text-embedding-ada-002'},
        'input':        'test_input'}


# -----------------------------------------------------------------------------
@pytest.fixture
def template_audio_transcriptions_valid():
    """
    Return valid template data structure for the audio_transcriptions endpoint.

    """
    return {
        'id_endpoint':  'audio_transcriptions',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'file':  'test_audio_file',
                         'model': 'whisper-1'},
        'prompt':       'test_prompt'}


# -----------------------------------------------------------------------------
@pytest.fixture
def template_audio_translations_valid():
    """
    Return a valid template data structure for the audio_translations endpoint.

    """
    return {
        'id_endpoint':  'audio_translations',
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'file':  'test_audio_file',
                         'model': 'whisper-1'},
        'prompt':       'test_prompt'}


# -----------------------------------------------------------------------------
@pytest.fixture
def param_valid():
    """
    Return a valid parameter data structure.

    """
    return {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Things for template
        'kwargs_req':   dict(), # <-- Things for OpenAI request
        'metadata':     dict()} # <-- Tracking metadata


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
            'id_endpoint':        'chat_completions',
            'model':              'gpt-3.5-turbo',
            'temperature':        0.7,
            'n':                  1,
            'stream':             False,
            'presence_penalty':   0.0,
            'frequency_penalty':  0.0,
            'user':               'test_user',
            'metadata':           dict()}}


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
    Return an expected response to a built-in-test request.

    """
    id_endpoint = 'chat_completions'
    import fl.net.openai.client
    return {
        'request':   {},  # Needs to be filled in the test case.
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'error':     None,
        'metadata':  {}}


# -----------------------------------------------------------------------------
@pytest.fixture
def testrunner_singleshot_ipc():
    """
    Return a single-shot test runner fixture.

    """
    # -------------------------------------------------------------------------
    def _get_one_result(cfg,
                        list_request,
                        maxiter     = 50,
                        delay_secs  = 0.01):
        """
        Run the openAI client and wait for the first set of responses.

        """
        import fl.net.openai.client

        ipc_handler = fl.net.openai.client._coro_daemon_ipc_handler(cfg = cfg)

        for _ in range(maxiter):
            (list_result, list_error) = ipc_handler.send(list_request)
            if (len(list_result) > 0) or (len(list_error) > 0):
                return (list_result, list_error)
            time.sleep(delay_secs)

    return _get_one_result


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
                                        testrunner_singleshot_ipc,
                                        expected_bit_response):
        """
        fl.net.openai.client coro() yields the expected BIT response.

        When configured with built-in-test enabled,
        the system shall return the expected
        prepopulated built-in-test response.

        """
        test_list_messages = ['test_request']
        request            = {'messages': test_list_messages}
        (list_result, list_error)  = testrunner_singleshot_ipc(
                                        cfg          = cfg_valid_bit_enabled,
                                        list_request = [request])
        assert len(list_result) == 1
        assert len(list_error)  == 0

        expected_bit_response['request'] = cfg_valid_bit_enabled['default']
        expected_bit_response['request'].pop('id_endpoint', None)
        expected_bit_response['request'].pop('metadata',    None)
        expected_bit_response['request']['messages'] = test_list_messages

        assert list_result[0] == expected_bit_response

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_validates_provided_configuration(self, cfg_invalid):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        with pytest.raises(AssertionError):
            fl.net.openai.client.coro(cfg = cfg_invalid)
