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

import pprint
import textwrap


# Load initial prompt templates.
#
template_characters = textwrap.dedent("""
    Generate a list of 3-5 characters for a story based on the following description:

          "A {style} story about {theme} suitable for an {age}-year old
          inspired by {inspiration} that teaches {teaching}. 
          Customise the story so that {custom_instruction}"

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
        "Act 1: Act Title" : [ # Establishing the World and the Characters
        "Scene 1": "Scene description" # Introduce the protagonist and their ordinary world, highlighting their strengths, flaws, and desires.
        "Scene 2": "Scene description" # Inciting incident: Disrupt the protagonist's world and establish the conflict, introducing the antagonist or obstacles.
        "Scene 3": "Scene description" # Raise the stakes and establish the point of no return for the protagonist.
        "Scene 4": "Scene description" # Protagonist's initial response to the conflict, highlighting their strengths and weaknesses.
        "Scene 5": "Scene description" # End Act 1 with a major turning point or a cliffhanger that sets up the rest of the story
        ],
        "Act 2: Act Title" : [ # Confronting the Obstacles and Building Tension
        "Scene 1": "Scene description" # The protagonist's plan to overcome the obstacle, showcasing their resourcefulness and creativity.
        "Scene 2": "Scene description" # Introduce complications, obstacles, and setbacks that challenge the protagonist's plan and increase the stakes.
        "Scene 3": "Scene description" # The protagonist faces their lowest point, with seemingly insurmountable obstacles and doubts about their ability to succeed.
        "Scene 4": "Scene description" # The protagonist regroups and renews their commitment to their goal, finding inspiration and support from allies.
        "Scene 5": "Scene description" # End Act 2 with a twist or a new complication that sets up the climax
        ],
        "Act 3: Act Title" : [ # The Final Confrontation and Resolution
        "Scene 1": "Scene description" # Show the protagonist preparing for the final confrontation, reflecting on their journey and growth.
        "Scene 2": "Scene description" # Introduce the final obstacle or antagonist, challenging the protagonist in unexpected ways.
        "Scene 3": "Scene description" # The final confrontation, with the protagonist using everything they've learned to overcome the obstacle or defeat the antagonist.
        "Scene 4": "Scene description" # Show the aftermath of the confrontation and tie up any loose ends, resolving subplots and character arcs.
        "Scene 5": "Scene description" # End the story with a satisfying resolution or a hint at a new beginning that shows the protagonist's growth and transformation
        ]
        }}
        chapter_outline_json = """)


template_paragraph = textwrap.dedent("""
    Generate a paragraph for {chapter_title} : {subchapter_title} based on
    the following story outline:

    {story_outline}

    And the following characters:

    {story_characters}

    The story should be {story_description}.
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

template_rewrite = textwrap.dedent("""
    You are an editor. As an editor, you edit draft scripts to convert them to final drafts.
    Characters: {characters}
    Story Outline: {outline}
    The theme is {theme}, in the style of a {style} story, inspired by {inspiration}.
    The story is meant to teach the kid about {teaching}
    Pretend you are reading it to a {age}-year-old kid.
    Customise the story so that {custom_instruction}.
    Story: {story} End of Story
    Make sure to add connecting sentences between scenes, and create a flowing story.
    Keep a balance between dialog, descriptions, and narration in the final draft.
    Keep chapter titles in your story.
    Proceed with the rewrite of the story.
    The story should be at least {len(story)} words long.
    """)

list_template_default = [{
        'characters': {'template': template_characters},
        'outline':    {'template': template_outline},
        'paragraph':  {'template': template_paragraph},
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

    while True:

        (result, param) = yield (list_template, list_param)

        list_template.clear()
        list_param.clear()

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
            param_new = _get_params(result)
            if param_new is not None:
                list_param.append(param_new)


# -----------------------------------------------------------------------------
def _get_params(result):
    """
    """
    id_prompt = result['request']['_id_prompt']
    param     = result['request']['_param']


    if id_prompt == 'characters':
        story_characters = result['response']['choices'][0]['text']
        param['story_characters'] = story_characters
        return {
            'outline': param
        }

    if id_prompt == 'outline':
        story_outline = result['response']['choices'][0]['text']

        queue_param = list()
        for (chapter_title, subchapter_list) in story_outline.items():
            for (scene_number, subchapter_title) in enumerate(subchapter_list):
                queue_param.append()


            # chapter_text = generate_paragraph(
            #     story_description, story_outline, story_characters, chapter_title, subchapter_title, scene_number+1, history_summary)
            # history_summary = summarise(history_summary + chapter_text)
            # print()
            # print(chapter_text)
            # print()
            # # chapter = rewrite_chapter(story_outline, chapter_number, chapter_title)
            # history += chapter_text


        param['story_outline'] = story_outline
        return {
            'something': param
        }



    return chapters, story_characters, story_outline

































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


