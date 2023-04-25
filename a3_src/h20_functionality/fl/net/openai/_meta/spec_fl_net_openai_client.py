# -*- coding: utf-8 -*-
"""
Functional specification for fl.net.openai.client

"""


import pytest


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
    def it_supports_creation_of_the_main_coroutine(self):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        client = fl.net.openai.client.coro(cfg = {})

    # -------------------------------------------------------------------------
    def it_validates_provided_configuration(self):
        """
        fl.net.openai.client coro() can be created.

        """
        import fl.net.openai.client
        client = fl.net.openai.client.coro(cfg = {})


# {
#    "id":       "chatcmpl-abc123",
#    "object":   "chat.completion",
#    "created":  1677858242,
#    "model":    "gpt-3.5-turbo-0301",
#    "usage": {
#       "prompt_tokens":13,
#       "completion_tokens":7,
#       "total_tokens":20
#    },
#    "choices":[
#       {
#          "message":{
#             "role":"assistant",
#             "content":"\n\nThis is a test!"
#          },
#          "finish_reason":"stop",
#          "index":0
#       }
#    ]
# }