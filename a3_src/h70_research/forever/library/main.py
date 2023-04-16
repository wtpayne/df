

import sys


import kivy.app
import kivy.uix.screenmanager
import kivy.properties 

# import kivy.uix.widget

# import kivy.uix.boxlayout
# import kivy.uix.image
# import kivy.uix.button
# import kivy.uix.label


class ParagraphScreen(kivy.uix.screenmanager.Screen):
    paragraphs = kivy.properties.ListProperty([
        "This is the first paragraph.",
        "This is the second paragraph.",
        "This is the third paragraph."
    ])
    current_paragraph_index = 0

    @property
    def current_paragraph_text(self):
        return self.paragraphs[self.current_paragraph_index]

    def previous_paragraph(self):
        self.current_paragraph_index = (self.current_paragraph_index - 1) % len(self.paragraphs)
        self.ids.paragraph_label.text = self.current_paragraph_text

    def next_paragraph(self):
        self.current_paragraph_index = (self.current_paragraph_index + 1) % len(self.paragraphs)
        self.ids.paragraph_label.text = self.current_paragraph_text


class ForeverApp(kivy.app.App):
    def build(self):
        return ParagraphScreen()


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



