

import sys
import time
import json

import kivy.app
import kivy.clock
import kivy.network.urlrequest
import kivy.properties
import kivy.uix.screenmanager
from kivy.uix.image import Image

# import kivy.uix.widget

# import kivy.uix.boxlayout
# import kivy.uix.image
# import kivy.uix.button
# import kivy.uix.label

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from kivy.uix.label import Label

import codecs

class LoadingScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()

        story = [
                "Eliana is an 11-year-old girl with curly, coppery hair that cascades down her back, bright hazel eyes, and a smattering of freckles across her nose. Despite struggling in school due to her dyslexia, she is fiercely independent, curious, imaginative, and deeply empathetic. Eliana loves nothing more than stories of adventure and magic, and spends most of her free time exploring the world around her. She often finds herself lost in her own imagination, dreaming up new and thrilling tales of daring heroes and mystical creatures. Eliana's dyslexia can sometimes make reading and writing difficult for her, but she refuses to let it hold her back from her love of adventure and magic.",
                "She has learned to find creative ways to cope and excel in other areas, like running and exploring nature. Eliana is excited to see what kind of adventure life has in store for her next.",
                "Eliana was exploring the woods behind her house, listening to the crunch of leaves underfoot. She dug her fingers into the dirt, searching for interesting rocks and bugs.",
                "Suddenly, her hand brushed against something hard and cold. She pulled it out and gasped. It was a silver amulet, etched with strange symbols. Eliana felt a strange energy pulsing from it. She slipped it around her neck and felt a rush of excitement.\n \nShe ran back to her house, eager to show her friends. As soon as she burst through the door, Kai jumped up. \"Whoa, what's that?\" he asked, reaching for the amulet. Eliana pulled back, feeling a strange sense of protectiveness. \"It's mine,\" she said, turning away. \n \nZara noticed the change in Eliana's demeanor and asked kindly, \"What does it do?\" Eliana wasn't sure, but she felt a pull from the amulet, like it was trying to communicate with her. Suddenly, a voice echoed in her head. \"Save us,\" it whispered urgently. \n \nEliana stumbled back, nearly dropping the amulet. She looked around at her friends, confused and scared. \"Did you hear that?\" she asked, her voice quivering. Her friends looked at each other, unsure of what to do. Suddenly, they heard a loud thud from outside. \n \nThey ran to the window and gasped. A dark figure was lurking in the shadows, staring at them with cold, blue eyes. Eliana felt a jolt of recognition. This was the creature from her dreams - the one that had been tormenting the magical creatures. She knew what she had to do. \n \n\"We have to save them,\" she said firmly, clutching the amulet. \"We have to go on a quest.\" Her friends hesitated, but then they saw the determination in Eliana's eyes. They nodded, ready to follow her into this magical world. They had no idea what awaited them, but they knew one thing for sure - they were in this together.",
                "Eliana and her friends gather around the silver amulet, trying to decipher its message. Suddenly, a voice from the amulet speaks to them. \"I am Arin, the Guardian of the Forest,\" the voice says.",
                "Emrys, a dark wizard, is capturing and harming the magical creatures of this land. You must stop him before it's too late.\" Eliana's heart races as she realizes the gravity of their mission. \"We have to help them,\" she declares. \"But how?\" Zara asks. \"We have to find a way to defeat Emrys,\" Eliana replies. \"And we have to do it fast.\" As they discuss their plans, Eliana feels a sense of purpose and determination that she's never felt before. She's always loved exploring and going on adventures, but this is different. This time, lives are at stake, and they're counting on her. As the sun sets and they make their way home, Eliana knows that she can't go back to her ordinary world until they've completed their mission. She's ready to embark on a dangerous journey, even if it means facing her fears and overcoming her dyslexia. She'll do whatever it takes to save the magical creatures and defeat Emrys.",
                "Eliana walked behind her friends, deep in thought. Her dyslexia had always made her feel like she wasn't good enough, and now, on this dangerous mission, it was even more of a hindrance.",
                "What if I mess up?\" she thought. \"What if I can't read the magical symbols or decipher the clues?\" She felt a lump form in her throat and her palms grew sweaty. \n\n\"Hey, Eliana, are you okay?\" Kai's voice interrupted her thoughts. She nodded, not trusting her voice, but he could tell something was wrong. \"What's going on?\" he persisted. \n\n\"It's nothing,\" Eliana said, but her voice trembled. \n\n\"It doesn't sound like nothing,\" Zara chimed in. \"You can talk to us, you know.\" \n\nEliana took a deep breath and decided to confide in her friends. \"It's just...my dyslexia. What if I can't do this? What if I let you guys down?\" \n\nRami put a hand on her shoulder. \"You won't let us down,\" he said firmly. \"We're a team, and we're here to support each other. Besides, your dyslexia is also a strength. You see things in a unique way that the rest of us don't.\" \n\nEliana looked up at him, surprised. \"Really?\" \n\n\"Really. And we're lucky to have you on our team,\" Kai added. \n\nEliana felt a warm feeling in her chest. With her friends by her side, she felt like she could do anything. \"Thanks, guys,\" she said with a smile. \"Let's do this.\" \n\nThey continued on their quest, with Eliana feeling more confident and supported than ever before.",
                "As Eliana and her friends rested in a clearing, they discussed their plan for defeating Emrys. Suddenly, Arin's voice echoed through the trees, \"Beware, Emrys has discovered your plan and is sending his minions to stop you!\" Instantly, the group sprang into action, grabbing their weapons and preparing for battle. Eliana's heart raced as she realized the magnitude of their task. As they made their way through the forest, they encountered a group of shadowy figures with glowing eyes. Rami stepped forward, ready to defend his friends. \"Who goes there?\" he demanded. The figures chuckled darkly and launched an attack. The group fought bravely, but they were outnumbered and outmatched. Eliana's heart sank as Kai was struck down and captured by the minions. Emrys's voice boomed through the trees, \"Surrender now, and you may live. Resist, and you will suffer the consequences.\" Eliana refused to back down, determined to save her friend and continue their mission. As they fled deeper into the forest, the group knew that their journey had just gotten much more difficult.",
                "Eliana's heart was heavy with worry for Kai, but she knew they needed to keep moving forward. As they huddled in a circle, Zara began to hum a tune that gradually grew louder until the group joined in. Eliana closed her eyes and let the melody wash over her, feeling a sense of calmness settle over her. When the song ended, she opened her eyes to see her friends looking at her expectantly. \n\n\"What's our plan?\" Rami asked, his arms crossed over his chest. \n\nEliana took a deep breath and began to explain her idea. \"I think we need to split up. If we all go after Kai, we'll risk getting caught again. But if we split into pairs, we can cover more ground and increase our chances of finding him. Zara and I will search the forest, and Rami, you and Arin can check the caves. We'll meet back here in two hours.\" \n\nZara nodded eagerly, a determined look on her face. \"We won't let you down, Eliana. Kai's counting on us!\" \n\nRami grunted his agreement and turned to Arin. \"Let's go. We don't have much time.\" \n\nAs the group dispersed, Eliana and Zara made their way deeper into the forest. Eliana's heart was pounding with nerves, but she focused on the task at hand. She knew they had to outsmart Emrys's minions if they were going to save Kai and continue their quest. She just hoped their plan would work.",
                "As Eliana and Zara navigate through the dense forest, the trees grow thicker and the underbrush becomes harder to push through. Eliana's dyslexia begins to hinder her as she struggles to read the map and decipher the clues. Frustrated, she takes a deep breath and closes her eyes, trying to visualize the next step. Suddenly, she has an idea. \"Zara, can you describe the symbols on the map to me?\" she asks. Zara nods and begins describing the intricate drawings in detail. Eliana listens carefully and with her imagination, she creates a mental map. Eliana leads the way while Zara keeps a lookout for any danger. \n\nMeanwhile, Rami and Arin cautiously make their way through the winding cave system. The darkness envelopes them, and the echoes of their footsteps bounce off the walls. Suddenly, they hear a faint whispering. They approach quietly and see a group of Emrys's minions huddled together, planning their next move. Rami motions to Arin to be ready and they prepare to strike. As they move in, Rami feels his heart pounding in his chest, but he trusts Arin and his own instincts. They fight fiercely, their moves fluid and precise as they take down their opponents. \n\nAfter the battle, the group reunites, relieved to see each other unharmed. They recount their adventures and share the clues they've discovered. Eliana's friends praise her for her creativity and quick thinking, and she feels a sense of pride and accomplishment. They also discuss their next steps, and Kai suggests a risky plan that could give them the upper hand against Emrys. Eliana is hesitant, but she trusts her friends and knows they have to work together to save Kai and defeat Emrys. As a team, they set out on their next challenge, feeling closer and more confident than ever before.",
                "Eliana felt like she couldn't catch her breath. The obstacles before her seemed insurmountable. Her dyslexia had always made her feel like she had to work twice as hard as everyone else. Now, on this quest to save the magical creatures, it felt like her weakness would be her downfall. \"I don't know if I can do this,\" she said, tears welling up in her eyes. \n\nZara put a gentle hand on her arm. \"Remember when we saved the baby dragon? You were the one who found the hidden path. You have a unique way of seeing things that helps us all.\"\n\nKai nodded. \"And when we were stuck in that underground river, you made us all laugh with your silly jokes. You're more than just your dyslexia, Eliana. You're a great friend and a brave adventurer.\"\n\nRami put a hand on Eliana's shoulder. \"We're a team, Eliana. We each have our strengths and weaknesses. Together, we can overcome anything.\"\n\nEliana wiped her tears and took a deep breath. They were right. She had faced challenges before and had always found a way to persevere. \"Thanks, guys,\" she said, smiling through her tears. \"I don't know what I'd do without you.\"\n\nThey shared a group hug and continued on their quest with renewed determination, knowing that they were stronger together than apart.",
                "Eliana took a deep breath and closed her eyes, trying to calm her racing thoughts. She had been feeling overwhelmed and discouraged by the obstacles they faced, but she knew she couldn't give up now. She thought about the magical creatures they had encountered so far, with their unique abilities and personalities. She realized that they all had something special to offer, just like her and her friends. \n\nAs they continued through the forest, Eliana noticed a shimmering light up ahead. They crept closer and saw a group of tiny fairies, dancing and singing in a circle. Eliana's eyes widened in wonder as she watched them move in perfect harmony, their wings sparkling in the sunlight. \n\nZara giggled and clapped her hands, joining in the dance. Eliana hesitated for a moment, feeling self-conscious, but then she reminded herself of her commitment to the mission. She closed her eyes and let herself sway to the music, feeling the gentle breeze brush against her skin. \n\nWhen the dance ended, the fairies flew away, leaving behind a small pouch of glittering dust. Eliana picked it up and examined it closely, feeling a surge of inspiration. She realized that every creature they encountered had something to offer, whether it was a clue, a tool, or simply a moment of joy. \n\nShe looked at her friends, who were beaming with happiness and excitement. She smiled, feeling grateful for their support and camaraderie. She knew that they still had a long way to go, but she felt renewed and energized. She had the strength and determination to face whatever challenges lay ahead. \n\n\"We can do this,\" she said, looking at each of them in turn. \"Together.\"",
                "As the group continues on their quest, they are suddenly ambushed by Emrys and his minions. In the chaos, Emrys manages to capture one of Eliana's friends as leverage to stop them from completing their mission.",
                "Eliana's heart sinks as she realizes the gravity of the situation. \"No!\" she cries out, reaching for her friend but grasping only air. Emrys cackles triumphantly, pleased with himself for throwing a wrench in their plans. \"You should have known better than to cross me,\" he sneers, disappearing into the shadows with their captive. Eliana clenches her fists and vows to save their friend, no matter what it takes. She turns to her remaining friends, determination etched on her face. \"We can't give up now. We have to keep going.\" The group nods in unison, silently agreeing to stick together and push forward. With renewed resolve, they set off into the unknown, ready for whatever challenges come their way.",
                "Eliana sat cross-legged on her bed, the silver amulet clasped tightly in her hand. She took a deep breath and closed her eyes, reflecting on the journey that had brought her here. She had faced so many challenges - her dyslexia, Emrys and his minions, the dangers of the magical world - but she had persevered, with the help of her friends. \n\nShe smiled as she remembered the way they had all grown and transformed since they first started on their quest. Kai had learned to listen to others and control his impulsiveness, Zara had become more confident in her creativity, and Rami had opened up and shown his kind heart. As for Eliana herself, she had learned to accept and even embrace her dyslexia. She had found ways to use it as an advantage, like when she had created a mental map to find Kai. \n\nNow, as she prepared to face Emrys in the final showdown, she felt a sense of calm and determination wash over her. She knew it wouldn't be easy, but she also knew she had the support and love of her friends. She opened her eyes and looked at the amulet, feeling a surge of power and hope. She whispered to herself, \"We can do this. We can save the magical creatures and stop Emrys. Together.\"",
                "Emrys stood towering over the group, his eyes flashing with malevolent power. \"You think you can stop me?\" he sneered. \"Your puny magic is no match for mine.\" He raised his staff, and a blast of dark energy rippled through the air, sending trees crashing to the ground. \nEliana and her friends stumbled back, but quickly regained their composure. \"We may not be as powerful as you,\" Eliana said, \"but we have something you'll never understand.\" She locked eyes with Emrys. \"We have love, friendship, and the power of inclusivity.\" \nEmrys snorted. \"Sentimental nonsense. Love won't protect you from my spells.\" He raised his staff again, but before he could utter the incantation, Rami charged forward, his fists clenched. \n\"Maybe not,\" he said, \"but this will.\" He landed a powerful punch on Emrys's jaw, causing him to stagger back. \nWhile Emrys was off balance, Kai swooped in, deftly grabbing his staff. \"Got it!\" he shouted. \nZara and Eliana worked quickly, each using their unique talents to decipher the runes etched on the staff. With a final burst of magic, they neutralized the dark energy and sent Emrys reeling. \nThe group cheered as Emrys vanished into the ether, his power broken. They knew there would be more challenges ahead, but they also knew they were stronger together. As they looked around at the beautiful, diverse creatures they had saved, they felt a deep sense of gratitude and satisfaction. They had done it, despite the odds, and they knew they could do it again.",
                "The final confrontation took place inside a vast, dimly lit cave, echoing with the sound of Emrys's menacing laughter. Eliana and her friends stood firm, ready to fight for what was right. Emrys sneered at them, his dark energy crackling and pulsing around him. \"You are no match for me,\" he spat. \"I am the master of magic, and you are nothing.\"\n\nEliana felt a surge of fear, but she shook it off, knowing that her friends were counting on her. As she looked around the cave, she noticed a series of glowing runes etched into the walls. They were in a language she didn't recognize, but she felt a strange connection to them. Suddenly, an idea struck her. \"Guys, look at the walls!\" she shouted. \"I think I can read this!\"\n\nHer friends looked at her skeptically, but they trusted her. Eliana took a deep breath and closed her eyes, feeling the words flow through her mind. As she recited the runes out loud, the cave shook and trembled. Emrys howled in frustration as his power waned, and his minions crumbled to dust. \n\nAs the dust settled, Eliana and her friends stood victorious. The magical creatures they had encountered on their journey emerged from hiding places, cheering and congratulating them. Eliana's friends surrounded her, hugging her and thanking her for her brilliance. Eliana beamed, feeling a sense of pride and accomplishment she had never felt before. Through her struggle with dyslexia, she had found an advantage that helped save the day. She knew that she and her friends had grown and transformed through the journey, learning to appreciate each other's differences and to work together to overcome any challenge.",
                "As the sun sets on the magical world, Eliana and her friends gather to celebrate their victory over Emrys. They sit around a campfire, surrounded by the creatures they've encountered on their journey. Zara sings a song she's composed, and Rami sketches a portrait of their group. Kai tinkers with a gadget he's made from some spare parts, and Eliana marvels at his ingenuity. \n\n\"I can't believe we did it,\" Eliana says, beaming with pride. \"We saved the magical world and all its creatures!\"\n\n\"It wasn't just us,\" Kai chimes in. \"We couldn't have done it without the help of our new friends.\" \n\nThe creatures around them nod in agreement, murmuring their thanks and appreciation. \n\nEliana takes a deep breath and addresses the group. \"I want to say something. Throughout this journey, I've learned something incredibly valuable. I used to feel ashamed of my dyslexia, like it was a weakness. But throughout our adventure, I've discovered that my dyslexia is actually an advantage in the magical world. It allows me to see things differently and solve problems in unique ways.\" \n\nHer friends nod in support, and Zara adds, \"And I've learned to appreciate my sensitivity and imagination, even if it makes me different from others.\" \n\nRami smiles and says, \"I've learned to trust my friends and rely on their strengths to help me when I need it.\" \n\nKai grins and adds, \"And I've learned that sometimes taking risks is worth it when you're fighting for what's right.\" \n\nTogether, they raise their hands in solidarity, united in their newfound appreciation for each other's differences. As they bid farewell to the magical creatures and prepare to return to their own world, Eliana knows that she'll never forget the lessons she's learned on this adventure. She'll always remember the power of love, friendship, and inclusivity, and she'll carry those values with her on all of her future adventures.",
                "Eliana, Kai, Zara, and Rami stood victorious over the defeated Emrys. The magical creatures cheered and applauded, grateful for their heroism. As they made their way back to the portal that would take them home, Eliana reflected on her journey. She had faced her fears and doubts, and had come out stronger on the other side. She now accepted her dyslexia as a part of who she was, and saw it as an advantage in the magical world. \n\n\"Thank you all for everything,\" Eliana said, turning to her friends. \"I couldn't have done it without you.\"\n\n\"Hey, we're a team, remember?\" Kai said with a grin.\n\n\"Always,\" Zara added, beaming.\n\n\"And we're not done yet,\" Rami said, nodding toward the portal. \"Who knows what other adventures await us?\"\n\nEliana smiled, feeling a sense of excitement and possibility. She now knew that she was capable of anything, as long as she had the support and love of her friends. As they stepped through the portal and returned to their ordinary world, Eliana felt a newfound sense of confidence and purpose. She knew that she would continue to go on adventures and help others, now with a deep understanding of the importance of inclusivity and celebrating differences."
        ]

        # app.paragraphs = story
        # screen_manager = self.manager
        # screen_manager.current = 'reader'

        hex_json = codecs.encode(json.dumps(app.settings).encode(), "hex")

        # Send request to backend and check results endpoint for response
        req = UrlRequest('http://localhost:8080/story:' + str(hex_json),
                         on_success=self.on_success)
        Clock.schedule_interval(lambda dt: self.check_results(hex_json), 1)

    def check_results(self, hex_json):
        req = UrlRequest('http://localhost:8080/results:' + str(hex_json),
                         on_success=self.on_check_results_success)

    def on_check_results_success(self, req, result):
        if result is not None:

            print(result)

            app = App.get_running_app()
            app.paragraphs = result
            screen_manager = self.manager
            screen_manager.current = 'reader'

    def on_success(self, req, result):
        print("Request successful")

class ConfigScreen(Screen):

    theme_values = ["Fantasy Adventure",
            "Science Fiction"]
    style_values = ["J.R.R. Tolkien mixed with Ursula K. Le Guin",
            "Octavia Butler mixed with Ray Bradbury"]
    inspiration_values = ["The Dark Is Rising",
            "The Hunger Games"]
    teaching_values = ["Emphasizing the importance of inclusivity and celebrating differences",
            "Highlighting the importance of diversity and unity in the face of oppression"]
    age_values = ['Toddler', 'Preschool', 'Kindergarten', 'Early elementary', 'Upper elementary', 'Middle school', 'High school']

    def submit(self):
        app = App.get_running_app()

        # Get the selected values from the dropdowns and the text from the text input
        theme_value = self.ids.theme_spinner.text
        style_value = self.ids.style_spinner.text
        inspiration_value = self.ids.inspiration_spinner.text
        teaching_value = self.ids.teaching_spinner.text
        age_value = self.ids.age_spinner.text
        text_input_value = self.ids.text_input.text

        # Print the values to the console
        print(f"Theme: {theme_value}")
        print(f"Style: {style_value}")
        print(f"Inspiration: {inspiration_value}")
        print(f"Teaching: {teaching_value}")

        screen_manager = self.manager
        app.settings = {
            "theme": theme_value,
            "style": style_value,
            "inspiration": inspiration_value,
            "teaching": teaching_value,
            "age": age_value,
            "text_input": text_input_value
        }
        screen_manager.current = 'loading'


class ParagraphScreen(Screen):

    @property
    def current_paragraph_text(self):
        app = App.get_running_app()
        if len(app.paragraphs) == 0:
            self.ids.paragraph_label.text = "No story loaded yet"
            return "No story loaded yet"
        else:
            self.ids.paragraph_label.text = app.paragraphs[app.current_paragraph_index]
            return app.paragraphs[app.current_paragraph_index]

    def previous_paragraph(self):
        app = App.get_running_app()

        if len(app.paragraphs) != 0:
            app.current_paragraph_index = (app.current_paragraph_index - 1) % len(app.paragraphs)
            self.ids.paragraph_label.text = self.current_paragraph_text

    def next_paragraph(self):
        app = App.get_running_app()

        if len(app.paragraphs) != 0:
            app.current_paragraph_index = (app.current_paragraph_index + 1) % len(app.paragraphs)
            self.ids.paragraph_label.text = self.current_paragraph_text

    def on_enter(self, *args):
        self.current_paragraph_text

# class ForeverApp(kivy.app.App):

#     def build(self):
#         self.reader = ConfigScreen()
#         req = kivy.network.urlrequest.UrlRequest('http://localhost:8080/story', on_success = self.on_success)
#         return self.reader

class ForeverApp(App):
    def set_current_screen(self, screen_name):
        self.screen_manager.current = screen_name

    def build(self):
        self.settings = {}
        self.paragraphs = []
        self.current_paragraph_index = 0

        # Create the screen manager
        self.screen_manager = ScreenManager()

        # Create the screens
        second_screen = ConfigScreen(name='parameters')
        third_screen = LoadingScreen(name='loading')
        main_screen = ParagraphScreen(name='reader')

        # Add the screens to the screen manager
        self.screen_manager.add_widget(second_screen)
        self.screen_manager.add_widget(third_screen)
        self.screen_manager.add_widget(main_screen)

        # Create the navigation bar
        nav_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        nav_bar.add_widget(Button(text='Reader', on_press=lambda *args: self.set_current_screen('reader')))
        nav_bar.add_widget(Button(text='Narrative Settings', on_press=lambda *args: self.set_current_screen('parameters')))
        # nav_bar.add_widget(Button(text='Third', on_press=lambda *args: self.set_current_screen('third_screen'))))

        # Create the title label
        title_label = Label(text='Forever Library Narrative Engine 1.0', size_hint=(1, 0.05))

        # Create the main layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(title_label)
        layout.add_widget(self.screen_manager)
        layout.add_widget(nav_bar)

        return layout

if __name__ == '__main__':
    ForeverApp().run()


# pages = [
#     {'text': 'Once upon a time, there was a cat.'},
#     {'text': 'The cat liked to chase mice.'},
#     {'text': 'One day, the cat caught a mouse and ate it.'},
#     {'text': 'The end.'}
# ]


# # =============================================================================
# class ForeverApp(kivy.app.App):
#     """
#     """

#     # -------------------------------------------------------------------------
#     def build(self):

#         # Create a box layout to hold the text and image
#         layout = kivy.uix.boxlayout.BoxLayout(orientation='horizontal')

#         # Create a label to display the text
#         self.text_label = kivy.uix.label.Label(text=pages[0]['text'])
#         layout.add_widget(self.text_label)

#         # Create an image widget to display the picture
#         # self.image_widget = kivy.uix.image.Image(source=pages[0]['image'])
#         # layout.add_widget(self.image_widget)

#         # Create buttons to move to the next and previous pages
#         self.prev_button = kivy.uix.button.Button(text='Prev')
#         self.prev_button.bind(on_press=self.show_prev_page)
#         layout.add_widget(self.prev_button)

#         self.next_button = kivy.uix.button.Button(text='Next')
#         self.next_button.bind(on_press=self.show_next_page)
#         layout.add_widget(self.next_button)

#         return layout

#     # -------------------------------------------------------------------------
#     def show_next_page(self, obj):
#         # Update the text and image to the next page
#         current_page_index = pages.index({'text': self.text_label.text})
#         if current_page_index < len(pages) - 1:
#             next_page_index = current_page_index + 1
#             self.text_label.text = pages[next_page_index]['text']

#     # -------------------------------------------------------------------------
#     def show_prev_page(self, obj):
#         # Update the text and image to the previous page
#         current_page_index = pages.index({'text': self.text_label.text})
#         if current_page_index > 0:
#             prev_page_index = current_page_index - 1
#             self.text_label.text = pages[prev_page_index]['text']

# # -----------------------------------------------------------------------------
# def main():
#     """
#     """
#     ForeverApp().run()
#     return 0


# # -----------------------------------------------------------------------------
# if __name__ == '__main__':
#     sys.exit(main())



