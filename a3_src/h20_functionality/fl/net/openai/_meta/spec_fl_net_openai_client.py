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
    id_endpoint  = 'completions'
    uid_template = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant  = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params   = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model     = 'text-davinci-003'
    prompt_test  = 'completions_test_prompt_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint,
            'model':        id_model}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'model': id_model},
        'prompt':           prompt_test}

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'model':            id_model,
        'prompt':           prompt_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint   = 'chat_completions'
    uid_template  = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant   = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params    = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model      = 'text-davinci-003'
    messages_test = [{'role':    'system',
                      'content': 'chat_completions_test_msg_content'}]

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint,
            'model':        id_model}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'model': id_model},
        'messages':         messages_test }

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'model':            id_model,
        'messages':         messages_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint      = 'edits'
    uid_template     = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant      = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params       = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model         = 'text-davinci-edit-001'
    input_test       = 'edits_test_input_text'
    instruction_test = 'edits_test_instruction_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint,
            'model':        id_model}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'model': id_model},
        'input':            input_test,
        'instruction':      instruction_test }

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'model':            id_model,
        'input':            input_test,
        'instruction':      instruction_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint  = 'images_generations'
    uid_template = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant  = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params   = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    prompt_test  = 'images_generations_test_prompt_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {},
        'prompt':           prompt_test }

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'prompt':           prompt_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

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
    id_endpoint  = 'images_edits'
    uid_template = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant  = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params   = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    image_test   = 'images_edits_test_image_data'
    prompt_test  = 'images_edits_test_prompt_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'image': image_test},
        'prompt':           prompt_test}

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'image':            image_test,
        'prompt':           prompt_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint  = 'images_variations'
    uid_template = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant  = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params   = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    image_test   = 'images_variations_test_image_data'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'image':  image_test}}

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'image':            image_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint  = 'embeddings'
    uid_template = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant  = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params   = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model     = 'text-embedding-ada-002'
    input_test   = 'embeddings_test_input_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint,
            'model':        id_model}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'model': id_model},
        'input':            input_test}

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'model':            id_model,
        'input':            input_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint     = 'audio_transcriptions'
    uid_template    = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant     = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params      = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model        = 'whisper-1'
    audio_file_test = 'audio_transcriptions_test_audio_file_data'
    prompt_test     = 'audio_transcriptions_test_prompt_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint,
            'model':        id_model}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'file':  audio_file_test,
                             'model': id_model},
        'prompt':           prompt_test}

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'file':             audio_file_test,
        'model':            id_model,
        'prompt':           prompt_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

    error_valid = []

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
    id_endpoint     = 'audio_translations'
    uid_template    = 'e2cb431c-a709-4e7e-a9d1-dfb51d8dc4e2'
    uid_variant     = '5b8c0cfb-b4fb-4d9a-a839-4eef8bdd36d3'
    uid_params      = 'de678e1f-bc1b-402a-bfe8-d2705cb9a5ce'
    id_model        = 'whisper-1'
    audio_file_test = 'audio_translations_test_audio_file_data'
    prompt_test     = 'audio_translations_test_prompt_text'

    cfg_valid = {
        'is_bit':           True,
        'api_key':          'test_api_key',
        'secs_interval':    0.01,
        'default':          {
            'id_endpoint':  id_endpoint,
            'model':        id_model}}

    template_valid = {
        'id_endpoint':      id_endpoint,
        'type':             {'id': 'prompt_template', 'ver': '1.0'},
        'uid_template':     uid_template, # Process step.
        'uid_variant':      uid_variant,  # Improvement.
        'kwargs_req':       {'file':  audio_file_test,
                             'model': id_model},
        'prompt':           prompt_test}

    params_valid = {
        'type':             {'id': 'prompt_params', 'ver': '1.0'},
        'uid_params':       uid_params,
        'uid_template':     uid_template,
        'kwargs_tmpl':      dict(), # <-- Args for template
        'kwargs_req':       dict(), # <-- Args for OpenAI request
        'state':            dict()} # <-- Process state

    request_valid = {
        'file':             audio_file_test,
        'model':            id_model,
        'prompt':           prompt_test}

    result_valid = [{
        'error':            None,
        'request':          request_valid,
        'response':         fl.net.openai.client.built_in_test_response(
                                                                id_endpoint),
        'state':            {}}]

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
        list_tup_input_test = list()
        list_tup_input_test.append((list_template, list_param))

        client = fl.net.openai.client.coro_string_template_handler(cfg = cfg)
        for _ in range(maxiter):

            if list_tup_input_test:
                tup_input_test = list_tup_input_test.pop()
            else:
                tup_input_test = ([], [])

            (list_result, list_error) = client.send(tup_input_test)
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
