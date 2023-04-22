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


import textwrap


# Load initial prompt templates.
#
story_characters = textwrap.dedent("""
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

story_outline = textwrap.dedent("""

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


paragraph = textwrap.dedent("""
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

















# # from flask import Flask

# # app = Flask(__name__)

# import openai
# from pprint import pprint
# from dotenv import load_dotenv
# import os
# import json

# load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')


# def save_json(foldername, filecontents, jsondata):
#     if not os.path.exists(foldername):
#         os.mkdir(foldername)
#     files = os.listdir(foldername)
#     count = len(files)
#     file_name = f"{filecontents}_{count}.json"

#     with open(os.path.join(foldername, file_name), 'w') as f:
#         json.dump(jsondata, f)

# def load_json(foldername, filename):
#     file_path = os.path.join(foldername, filename)
#     with open(file_path, 'r') as f:
#         data = json.load(f)
#     return data

# def summarise(text):
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[
#             {"role": "system", "content": f"Please summarize the events in the following story:\n {text}"}],
#         temperature=0.0
#     )
#     # response.choices[0].text.strip()
#     output = response.choices[0].message.content
#     return output


# def generate_from_gpt(prompt, model="gpt-3.5-turbo", temperature=0.9):

#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=[
#             {"role": "system", "content": prompt}],
#         temperature=temperature
#     )
#     # response.choices[0].text.strip()
#     output = response.choices[0].message.content
#     return output


# def generate_characters(story_description):
#     prompt = f"Generate a list of 3-5 characters for a story based on the following description: \
#               \n\n{story_description} \
#               \n\nThe story should have five characters, each with a unique personality, backstory, and motivation. \
#               \n\nThe character list should look like this: \
#               \n[ \
#               \n    {{ \
#               \n        \"name\": \"Character Name\", \
#               \n        \"role\": \"Character Role (Protagonist, Antagonist, Supporting)\", \
#               \n        \"age\": \"Character Age\", \
#               \n        \"physical_description\": \"Physical Description\", \
#               \n        \"personality\": \"Character Personality\", \
#               \n        \"backstory\": \"Character Backstory\", \
#               \n        \"motivation\": \"Character Motivation\" \
#               \n        \"arc\": \"Character Arc\" \
#               \n    }}, \
#               \n    {{ \
#               \n        \"name\": \"Character Name\", \
#               \n        \"role\": \"Character Role\", \
#               \n        \"age\": \"Character Age\", \
#               \n        \"physical_description\": \"Physical Description\", \
#               \n        \"personality\": \"Character Personality\", \
#               \n        \"backstory\": \"Character Backstory\", \
#               \n        \"motivation\": \"Character Motivation\" \
#               \n        \"arc\": \"Character Arc\" \
#               \n    }}, \
#               \n    ... \
#               \n] \
#               \n\ncharacter_list = "
#     print("Character Generation Prompt: ")
#     pprint(prompt)
#     output = json.loads(generate_from_gpt(prompt))
#     return output


# def generate_outline(story_description, story_characters):
#     prompt = f"Generate a JSON that includes a chapter outline for a story based on the following description and the Hero's Journey: \
#         \n\n{story_description} \
#         \n\nThe following characters take part in the story: \
#         \n\n{story_characters} \
#         \n\nThe chapter structure JSON should look like this: \
#         \n {{ \
#         \n     \"Act 1: Act Title\": [ \
#         \n      Scene 1: Scene description - Introduce the protagonist and setting \
#         \n      Scene 2: Scene description - Establish the conflict and introduce the antagonist \
#         \n      Scene 3: Scene description - Raise the stakes and create a point of no return for the protagonist \
#         \n      Scene 4: Scene description - Develop the conflict further and increase the tension \
#         \n      Scene 5: Scene description - End Act 1 with a cliffhanger or a major turning point \
#         \n     ], \
#         \n     \"Act 2: Act Title\": [ \
#         \n      Scene 1: Scene description - Show the protagonist reacting to the events of Act 1 and establishing a plan \
#         \n      Scene 2: Scene description - Introduce complications and obstacles that make the protagonist's goal more difficult to achieve \
#         \n      Scene 3: Scene description - Increase the stakes and create more tension \
#         \n      Scene 4: Scene description - Show the protagonist facing their lowest point, with seemingly insurmountable obstacles \
#         \n      Scene 5: Scene description - End Act 2 with a twist or a new complication that sets up the climax \
#         \n     ], \
#         \n     \"Act 3: Act Title\": [ \
#         \n      Scene 1: Scene description - Show the protagonist preparing for the final confrontation \
#         \n      Scene 2: Scene description - Introduce the final obstacle or antagonist \
#         \n      Scene 3: Scene description - The final confrontation, with the protagonist using everything they've learned to overcome the obstacle or defeat the antagonist \
#         \n      Scene 4: Scene description - Show the aftermath of the confrontation and tie up any loose ends \
#         \n      Scene 5: Scene description - End the story with a satisfying resolution or a hint at a new beginning \
#         \n     ] \
#         \n }} \
#         \n\nchapter_outline_json = "
#     print("Outline Generation Prompt: ")
#     pprint(prompt)
#     output = json.loads(generate_from_gpt(prompt))
#     return output


# def generate_paragraph(story_description, story_outline, story_characters, chapter_title, subchapter_title, scene_number, history_summary):
#     prompt = f"Generate a paragraph for {chapter_title} : {subchapter_title} based on the following story outline: \
#     \n\n{story_outline}\
#     \n\nAnd the following characters:\
#     \n\n{story_characters}\
#     \n\nThe story should be {story_description}.\
#     \n\nThe scene should have a topic sentence, supporting content, and a concluding sentence.\
#     \n\nThe scene content should be between 100 and 200 words long and include character and location descriptions and introductions, dialog, narration and action.\
#     \n\nHere's what has happened up to this scene: {history_summary}\
#     \n\nThis scene's description is: {subchapter_title}\
#     \n\n# {chapter_title}\n## Scene {scene_number}: \n"
#     return f"# {chapter_title}\n## Scene {scene_number}: " + generate_from_gpt(prompt)


# def review_and_rewrite_chapter(chapter_text):
#     # Here you could add code to review the chapter and ensure that it's appropriate for the specified age group
#     # For the sake of simplicity, this function currently just returns the original chapter
#     return chapter_text


# def generate_chapters(story_description, story_outline, story_characters):

#     history = ""
#     history_summary = ""
#     for chapter_title, subchapter_list in story_outline.items():
#         for scene_number, subchapter_title in enumerate(subchapter_list):
#             chapter_text = generate_paragraph(
#                 story_description, story_outline, story_characters, chapter_title, subchapter_title, scene_number+1, history_summary)
#             history_summary = summarise(history_summary + chapter_text)
#             print()
#             print(chapter_text)
#             print()
#             # chapter = rewrite_chapter(story_outline, chapter_number, chapter_title)
#             history += chapter_text

#     return history


# def generate_story(theme, style="short", inspiration="", teaching="", age=None):
#     story_description = f"a {style} story about {theme}"
#     if age is not None:
#         story_description += f" suitable for a {age}-year-old"
#     if inspiration:
#         story_description += f" inspired by {inspiration}"
#     if teaching:
#         story_description += f" that teaches {teaching}"
#     story_description += "."

#     story_characters = generate_characters(story_description)
#     print("Story Characters: ")
#     pprint(story_characters)
#     save_json("characters", "character", story_characters)

#     story_outline = generate_outline(story_description, story_characters)
#     print("Story Outline: ")
#     pprint(story_outline)
#     save_json("outlines", "outline", story_outline)

#     chapters = generate_chapters(
#         story_description, story_outline, story_characters)

#     return chapters, story_characters, story_outline


# def rewrite_story(outline, story, characters, theme, style, inspiration, teaching, age):
#     prompt = f"You are an editor. As an editor, you edit draft scripts to convert them to final drafts.\
#     \nCharacters: {characters}\
#     \nStory Outline: {outline}\
#     \nThe theme is {theme}, in the style of a {style} story, inspired by {inspiration}.\
#     \nThe story is meant to teach the kid about {teaching}\
#     \nPretend you are reading it to a {age}-year-old kid. \
#     \n\nStory: {story}\n End of Story\
#     \nMake sure to add connecting sentences between scenes, and create a flowing story.\
#     \nKeep a balance between dialog, descriptions, and narration in the final draft.\
#     \nKeep chapter titles in your story.\
#     \nProceed with the rewrite of the story. \
#     \nThe story should be at least {len(story)} words long."
#     rewrite = generate_from_gpt(prompt, model="gpt-4", temperature=0.15)
#     return rewrite
# # @app.route('/story')
# # def story():
# #     # Call the generate_story function to get the story
# #     return generate_story()


# if __name__ == '__main__':

#     theme="Join Lily and her friends on a journey through time and space as they discover how our universe came to be."
#     style="Science-fiction adventure"
#     inspiration="The Magic School Bus by Joanna Cole and Bruce Degen"
#     teaching="Lily and her friends learn about the big bang theory and the origins of the universe, emphasizing the importance of scientific curiosity and critical thinking."
#     age=9

#     story, story_characters, story_outline = generate_story(
#                                                 theme=theme,
#                                                 style=style,
#                                                 inspiration=inspiration,
#                                                 teaching=teaching,
#                                                 age=age)

#     save_json("stories", "story", {"story": story})

#     # story = load_json("stories", "story_1.json")["story"]
#     # story_characters = load_json("characters", "character_1.json")
#     # story_outline = load_json("outlines", "outline_1.json")

#     rewrite=rewrite_story(story, story_characters, story_outline,
#                             theme=theme,
#                             style=style,
#                             inspiration=inspiration,
#                             teaching=teaching,
#                             age=age)

#     save_json("rewrites", "rewrite", {"rewrite": rewrite})

#     print("Rewrite: ")
#     print(rewrite)
#     # app.run()