# -*- coding: utf-8 -*-
"""
---

title:
    "OpenAI workflow engine module."

description:
    "This python module is designed to automate
    and continuously improve workflows for
    OpenAI ChatGPT agents."

id:
    "2fdd7113-1e2d-40df-81dc-7c4511f8e627"

type:
    dt003_python_module

validation_level:
    v00_minimum

protection:
    k00_general

copyright:
    "Copyright 2022-2023 William Payne"

license:
    "Licensed under the Apache License, Version
    2.0 (the License); you may not use this file
    except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed
    to in writing, software distributed under
    the License is distributed on an AS IS BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
    either express or implied. See the License
    for the specific language governing
    permissions and limitations under the
    License."

...
"""

# Load initial prompt templates.
#
template = textwrap.dedent("""
    Generate a list of 3-5 characters for a story based on the following description:

          "A {style} story about {theme} suitable for an {age}-year old
          inspired by {inspiration} that teaches {teaching}"

          The story should have five characters, each with a unique
          personality, backstory, and motivation.

          The character list should look like this:
          [
              {{
                  "name": "Character Name",
                  "role": "Character Role (Protagonist, Antagonist, Supporting)",
                  "age": "Character Age",
                  "physical_description": "Physical Description",
                  "personality": "Character Personality",
                  "backstory": "Character Backstory",
                  "motivation": "Character Motivation"
                  "arc": "Character Arc"
              }},
              {{
                  "name": "Character Name",
                  "role": "Character Role",
                  "age": "Character Age",
                  "physical_description": "Physical Description",
                  "personality": "Character Personality",
                  "backstory": "Character Backstory",
                  "motivation": "Character Motivation"
                  "arc": "Character Arc"
              }},
              ...
          ]
          character_list =
    """)



# =============================================================================
class Engine():
    """
    OpenAI workflow engine class.

    """

    # -------------------------------------------------------------------------
    def __init__(self, cfg):
        """
        """
        self.cfg = cfg

    # -------------------------------------------------------------------------
    def update(self, result, param):
        """
        Here is an example of a result data structure:

        {'error':       None,
         'request':     {'engine':      '<OPENAI_MODEL_ID>',
                         'max_tokens':  100,
                         'n':           1,
                         'prompt':      '<PROMPT_TEXT>.',
                         'stop':        None,
                         'temperature': 0.5},
         'response':    {'choices':     [{'finish_reason':  'stop',
                                          'index':          0,
                                          'logprobs':       None,
                                          'text':           '<RESPONSE_TEXT>'}],
                         'created':    1682122855,
                         'id':         'cmpl-77vHj30k0S1k8pqz2lHUueiQDMSZj',
                         'model':      '<OPENAI_MODEL_ID>',
                         'object':     'text_completion',
                         'usage':      {'completion_tokens':   57,
                                        'prompt_tokens':       9,
                                        'total_tokens':        66}}}"

        """
        pass

        # 1. check param - What do we do with it?

        # 2. check result - What do we do with it?





    # id_prompt     = 'test_prompt'
    # list_template = list()
    # list_param    = list()

    # def _add_param(id_prompt, **kwargs):
    #     list_param.append({id_prompt: kwargs})


    # def _add_template(id_prompt, str_template):
    #     list_template.append({id_prompt: {'guid':      'test_guid_string',
    #                                       'version':   'test_version_string',
    #                                       'template':  str_template}})


    # _add_template(id_prompt    = id_prompt,
    #               str_template = 'Please tell me some facts about {topic}.')

    # _add_param(id_prompt = id_prompt,
    #            topic     = 'Cars',
    #            _options  = { 'engine': 'text-curie-001' })
    # _add_param(id_prompt = id_prompt, topic = 'Lorries')


# -----------------------------------------------------------------------------
def _next_state(result):
    """
    """
    pass
#     print('#' * 80)
#     import pprint
#     pprint.pprint(inputs['result'])
#     print('#' * 80)
