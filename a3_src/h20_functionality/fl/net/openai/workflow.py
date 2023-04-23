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

import copy
import pprint
import textwrap


# Load initial prompt templates.
#
template_characters = textwrap.dedent("""
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
          character_list = """)

template_outline = textwrap.dedent("""

    Generate a JSON that includes a chapter outline
    for a story based on the following description
    and the Hero's Journey:

        "A {style} story about {theme} suitable for an {age}-year old
        inspired by {inspiration} that teaches {teaching}"

        The following characters take part in the story:

        {story_characters}

        The chapter structure JSON should look like this:
        {{
         "Act 1: Act Title": [
          Scene 1: Scene description - Introduce the protagonist and setting
          Scene 2: Scene description - Establish the conflict and introduce the antagonist
          Scene 3: Scene description - Raise the stakes and create a point of no return for the protagonist
          Scene 4: Scene description - Develop the conflict further and increase the tension
          Scene 5: Scene description - End Act 1 with a cliffhanger or a major turning point
         ],
         "Act 2: Act Title": [
          Scene 1: Scene description - Show the protagonist reacting to the events of Act 1 and establishing a plan
          Scene 2: Scene description - Introduce complications and obstacles that make the protagonist's goal more difficult to achieve
          Scene 3: Scene description - Increase the stakes and create more tension
          Scene 4: Scene description - Show the protagonist facing their lowest point, with seemingly insurmountable obstacles
          Scene 5: Scene description - End Act 2 with a twist or a new complication that sets up the climax
         ],
         "Act 3: Act Title": [
          Scene 1: Scene description - Show the protagonist preparing for the final confrontation
          Scene 2: Scene description - Introduce the final obstacle or antagonist
          Scene 3: Scene description - The final confrontation, with the protagonist using everything they've learned to overcome the obstacle or defeat the antagonist
          Scene 4: Scene description - Show the aftermath of the confrontation and tie up any loose ends
          Scene 5: Scene description - End the story with a satisfying resolution or a hint at a new beginning
         ]
        }}
        chapter_outline_json = """)


template_paragraph = textwrap.dedent("""
    Generate a paragraph for {chapter_title} : {subchapter_title} based on
    the following story outline:

    {story_outline}

    And the following characters:

    {story_characters}

    The story should be a {style} story about
    {theme} suitable for an {age}-year old inspired
    by {inspiration} that teaches {teaching}

    The scene should have a topic sentence,
    supporting content, and a concluding sentence.
    The scene content should be between 100 and
    200 words long and include character and
    location descriptions and introductions,
    dialog, narration and action.

    Here's what has happened up to this scene: {history_summary}

    This scene's description is: {subchapter_title}

    # {chapter_title}
    ## Scene {scene_number}:
    """)

template_summary = textwrap.dedent("""
    Please summarize the events in the following story:

    {summary_input}

    """)

template_rewrite = textwrap.dedent("""
    You are an editor. As an editor, you edit
    draft scripts to convert them to final
    drafts.

    Characters: {characters}

    Story Outline: {outline}

    The theme is {theme}, in the style of a
    {style} story, inspired by {inspiration}.

    The story is meant to teach the kid about {teaching}

    Pretend you are reading it to a {age}-year-old kid.

    Story: {story}
    End of Story

    Make sure to add connecting sentences between
    scenes, and create a flowing story. Keep a
    balance between dialog, descriptions, and
    narration in the final draft.

    Keep chapter titles in your story.
    Proceed with the rewrite of the story.
    The story should be at least {story_length} words long.
    """)

list_template_default = [{
        'characters': {'template': template_characters},
        'outline':    {'template': template_outline},
        'paragraph':  {'template': template_paragraph},
        'summary':    {'template': template_summary},
        'rewrite':    {'template': template_rewrite}}]

import fl.util


# -----------------------------------------------------------------------------
@fl.util.coroutine
def coro(cfg):
    """
    OpenAI workflow engine coroutine.

    """

    list_template = list()
    list_param    = list()
    list_resource = list()

    while True:

        (result, param) = yield (list_template, list_param, list_resource)

        list_template.clear()
        list_param.clear()
        list_resource.clear()

        # Default templates.
        #
        if list_template_default:
            list_template.extend(list_template_default)
            list_template_default.clear()

        # Parameters from outside (e.g. user)
        #
        if param is not None:
            list_param.append(param)

        # Parameters from OpenAI result (i.e. prev step)
        #
        if result is not None:
            (param_new, final_text) = _get_next_outputs(result)
            if param_new is not None:
                list_param.append(param_new)
            if final_text is not None:
                list_resource.append(final_text)


# -----------------------------------------------------------------------------
def _get_next_outputs(result):
    """
    """
    id_prompt = result['request']['_id_prompt']

    ### CHARACTERS ###
    if id_prompt == 'characters':
        story_characters          = result['response']['choices'][0]['text']
        param                     = result['request']['_param']
        param['story_characters'] = story_characters
        return ({'outline': param}, None)

    ### OUTLINE ###
    if id_prompt == 'outline':
        story_outline      = result['response']['choices'][0]['text']
        param              = result['request']['_param']
        list_chapter_param = list()

        for (chapter_title, subchapter_list) in story_outline.items():
            for (scene_number, subchapter_title) in enumerate(subchapter_list):
                param['story_outline']    = story_outline
                param['chapter_title']    = chapter_title
                param['subchapter_title'] = subchapter_title
                param['scene_number']     = scene_number + 1
                list_chapter_param.append(copy.deepcopy(param))

        param_new                     = list_chapter_param.pop(0)
        param_new['_queue']           = list_chapter_param
        param_new['_chapter_text']    = ""
        param_new['_history_summary'] = ""
        param_new['_history']         = ""
        return ({'paragraph': param_new}, None)

    ### PARAGRAPH ###
    if id_prompt == 'paragraph':
        chapter_text               = result['response']['choices'][0]['text']
        param                      = result['request']['_param']
        list_chapter_param         = param['_queue']
        param_new                  = list_chapter_param.pop(0)
        param_new['_queue']        = list_chapter_param
        param_new['summary_input'] = param['_history_summary'] + chapter_text
        param_new['_history']      = param['_history']         + chapter_text
        param_new['_chapter_text'] = chapter_text
        return ({'summary': param_new}, None)

    ### PARAGRAPH SUMMARY ###
    if id_prompt == 'summary':
        summary_text              = result['response']['choices'][0]['text']
        param                     = result['request']['_param']
        param['_history_summary'] = summary_text
        if param['_queue']:
            return ({'paragraph': param}, None)
        else:
            return ({'rewrite': param}, None)

    ### REWRITE ###
    if id_prompt == 'rewrite':
        final_text = result['response']['choices'][0]['text']
        return (None, final_text)
