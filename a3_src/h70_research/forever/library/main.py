

import sys
import time
import json

import kivy.app
import kivy.clock
import kivy.network.urlrequest
import kivy.properties
import kivy.uix.screenmanager

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

class LoadingScreen(Screen):
    def on_enter(self, *args):
        app = App.get_running_app()

        # screen_manager = self.parent
        # screen_manager = self.manager #self.parent

        # TODO: Send request to backend and generate paragraphs
        time.sleep(5)

        paragraphs = [
            json.dumps(app.settings)
        ]

        # screen_manager.get_screen('reader').paragraphs = paragraphs
        app.paragraphs = kivy.properties.ListProperty(paragraphs)
        screen_manager = self.manager
        print(screen_manager.current) 
        screen_manager.current = 'reader'

class ConfigScreen(Screen):
    # Define dropdowns and text input as ObjectProperties
    theme_values = ['Fairytale', 'Science Fiction Adventure']
    style_values = ['J.K. Rowling', 'Agatha Christie', 'Stephen King']
    inspiration_values = ['Harry Potter', 'Murder on the Orient Express', 'The Shining']
    teaching_values = ['Honesty', 'Courage', 'Compassion']
    age_values = ['Below 18', '18-25', '26-40', '41-60', 'Above 60']
    
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

        screen_manager = self.manager #self.parent
        # screen_manager.get_screen('loading')
        # screen_manager.current = 'loading'
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
            return "No story loaded yet"
        else:
            return app.paragraphs[app.current_paragraph_index]

    def previous_paragraph(self):
        app = App.get_running_app()

        app.current_paragraph_index = (app.current_paragraph_index - 1) % len(app.paragraphs)
        self.ids.paragraph_label.text = self.current_paragraph_text

    def next_paragraph(self):
        app = App.get_running_app()
        app.current_paragraph_index = (app.current_paragraph_index + 1) % len(app.paragraphs)
        self.ids.paragraph_label.text = self.current_paragraph_text


# class ForeverApp(kivy.app.App):

#     def build(self):
#         self.reader = ConfigScreen()
#         req = kivy.network.urlrequest.UrlRequest('http://localhost:8080/story', on_success = self.on_success)
#         return self.reader

class ForeverApp(App):
    def build(self):
        self.settings = {}
        self.paragraphs = []
        self.current_paragraph_index = 0

        # Create the screen manager
        screen_manager = ScreenManager()

        # Create the screens
        second_screen = ConfigScreen(name='parameters')
        third_screen = LoadingScreen(name='loading')
        main_screen = ParagraphScreen(name='reader')

        # Add the screens to the screen manager
        screen_manager.add_widget(second_screen)
        screen_manager.add_widget(third_screen)
        screen_manager.add_widget(main_screen)

        # Create the navigation bar
        nav_bar = BoxLayout(orientation='horizontal', size_hint=(1, 0.1))
        nav_bar.add_widget(Button(text='Reader', on_press=lambda *args: screen_manager.switch_to(main_screen)))
        nav_bar.add_widget(Button(text='Config', on_press=lambda *args: screen_manager.switch_to(second_screen)))
        # nav_bar.add_widget(Button(text='Third', on_press=lambda *args: screen_manager.switch_to(third_screen)))

        # Create the main layout
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(screen_manager)
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



