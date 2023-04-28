# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.openai.client

"""


import inspect
import time

import pytest


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_completions_valid_bit():
    """
    Return a valid template data structure for the completions endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'completions'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-davinci-003'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'text-davinci-003'},
        'prompt':       'test_prompt'}

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'model':  'text-davinci-003',
                      'prompt': 'test_prompt'},
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_chat_completions_valid_bit():
    """
    Return a valid template data structure for the chat completions endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'chat_completions'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'gpt-3.5-turbo-0301'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'gpt-3.5-turbo-0301'},
        'messages':     [{'role':    'system',
                          'content': 'test_content'}] }

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'model':      'gpt-3.5-turbo-0301',
                      'messages':   [{'role':    'system',
                                      'content': 'test_content'}]},
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_edits_valid_bit():
    """
    Return a valid template data structure for the edits endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'edits'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-davinci-edit-001'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'text-davinci-edit-001'},
        'input':        'test_input',
        'instruction':  'test_instruction' }

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'model':        'text-davinci-edit-001',
                      'input':        'test_input',
                      'instruction':  'test_instruction' },
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_images_generations_valid_bit():
    """
    Return a valid template data structure for the images_generations endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'images_generations'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {},
        'prompt':       'prompt' }

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'prompt': 'prompt' },
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_images_edits_valid_bit():
    """
    Return a valid template data structure for the images_edits endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'images_edits'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-davinci-003'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'image':  'test_image'},
        'prompt':       'test_prompt'}

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'image':  'test_image',
                      'prompt': 'test_prompt' },
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_images_variations_valid_bit():
    """
    Return a valid template data structure for the images_variations endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'images_variations'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-davinci-003'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'image':  'test_image'}}

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'image': 'test_image'},
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_embeddings_valid_bit():
    """
    Return a valid template data structure for the embeddings endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'embeddings'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-embedding-ada-002'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'model': 'text-embedding-ada-002'},
        'input':        'test_input'}

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'model': 'text-embedding-ada-002',
                      'input': 'test_input'},
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_audio_transcriptions_valid_bit():
    """
    Return valid template data structure for the audio_transcriptions endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'audio_transcriptions'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-davinci-003'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'file':  'test_audio_file',
                         'model': 'whisper-1'},
        'prompt':       'test_prompt'}

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'file':   'test_audio_file',
                      'model':  'whisper-1',
                      'prompt': 'test_prompt'},
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testvector_audio_translations_valid_bit():
    """
    Return a valid template data structure for the audio_translations endpoint.

    Sets the built-in-test flag to true so no
    actual call to the OpenAI server is made.

    """
    import fl.net.openai.client
    id_endpoint = 'audio_translations'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint': id_endpoint,
            'model':       'text-davinci-003'}}

    template_valid = {
        'id_endpoint':  id_endpoint,
        'type':         {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2', # Process step.
        'uid_variant':  '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3', # Improvement.
        'kwargs_req':   {'file':  'test_audio_file',
                         'model': 'whisper-1'},
        'prompt':       'test_prompt'}

    params_valid = {
        'type':         {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':   'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce',
        'uid_template': 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2',
        'kwargs_tmpl':  dict(), # <-- Args for template
        'kwargs_req':   dict(), # <-- Args for OpenAI request
        'state':        dict()} # <-- Process state

    result_valid = [{
        'error':     None,
        'request':   {'file':   'test_audio_file',
                      'model':  'whisper-1',
                      'prompt': 'test_prompt'},
        'response':  fl.net.openai.client.built_in_test_response(id_endpoint),
        'state':     {}}]

    error_valid  = []

    return (cfg_valid, template_valid, params_valid, result_valid, error_valid)


# -----------------------------------------------------------------------------
@pytest.fixture
def testrunner_coro_string_template_handler_singleshot():
    """
    Return a single-shot test runner fixture for the coro couroutine.

    """
    # -------------------------------------------------------------------------
    def _get_result_singleshot(cfg,
                               list_template,
                               list_param,
                               maxiter     = 100,
                               delay_secs  = 0.001):
        """
        Run the openAI client and wait for the first set of responses.

        """
        import fl.net.openai.client
        list_test_input = list()
        list_test_input.append((list_template, list_param))

        client = fl.net.openai.client.coro_string_template_handler(cfg = cfg)
        for _ in range(maxiter):

            if list_test_input:
                (list_result, list_error) = client.send(list_test_input.pop())
            else:
                (list_result, list_error) = client.send(([], []))

            if (len(list_result) > 0) or (len(list_error) > 0):
                return (list_result, list_error)

            time.sleep(delay_secs)

    return _get_result_singleshot


# =============================================================================
class SpecifyFlNetOpenAiClient:
    """
    Spec for the fl.net.openai.client package.

    """

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_import_of_fl_net_openai_client(self):
        """
        fl.net.openai.client can be imported.

        """
        import fl.net.openai.client

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_supports_creation_of_the_main_coroutine(
                                            self,
                                            testvector_completions_valid_bit):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        (cfg_valid, _, _, _, _) = testvector_completions_valid_bit
        client = fl.net.openai.client.coro_string_template_handler(
                                                            cfg = cfg_valid)
        assert inspect.isgenerator(client)

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_validates_provided_configuration(self,
                                            testvector_completions_valid_bit):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        (cfg_valid, _, _, _, _) = testvector_completions_valid_bit
        cfg_invalid = cfg_valid
        with pytest.raises(AssertionError):
            fl.net.openai.client.coro_string_template_handler(cfg = {})

    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_completions_input(
                        self,
                        testvector_completions_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid completions input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_completions_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_chat_completions_input(
                        self,
                        testvector_chat_completions_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid chat_completions input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_chat_completions_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_edits_input(
                        self,
                        testvector_edits_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid edits input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_edits_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_images_generations_input(
                        self,
                        testvector_images_generations_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid images_generations input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_images_generations_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_images_edits_input(
                        self,
                        testvector_images_edits_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid images_edits input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_images_edits_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])

        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_images_variations_input(
                        self,
                        testvector_images_variations_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid images_variations input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_images_variations_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_embeddings_input(
                        self,
                        testvector_embeddings_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid embeddings input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_embeddings_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_audio_transcriptions_input(
                        self,
                        testvector_audio_transcriptions_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid audio_transcriptions input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_audio_transcriptions_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected


    # -------------------------------------------------------------------------
    @pytest.mark.e002_general_research
    def it_yields_expected_bit_response_for_valid_audio_translations_input(
                        self,
                        testvector_audio_translations_valid_bit,
                        testrunner_coro_string_template_handler_singleshot):
        """
        When valid audio_translations input sent, valid bit output yielded.

        """
        (cfg_valid,
         template_valid,
         params_valid,
         list_result_expected,
         list_error_expected) = testvector_audio_translations_valid_bit
        (list_result,
         list_error) = testrunner_coro_string_template_handler_singleshot(
                                                            cfg_valid,
                                                            [template_valid],
                                                            [params_valid])
        assert list_result == list_result_expected
        assert list_error  == list_error_expected
