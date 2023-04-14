from wordcloud import WordCloud
import plotly.graph_objects as go
import numpy as np

from collections import Counter

class WordCloudGenerator:
    def __init__(self):
        self.text = []

    def add_sentence(self, sentence):
        self.text.append(sentence)

    def get_word_frequencies(self):
        words = [word for sentence in self.text for word in sentence.split()]
        return dict(Counter(words))


class PlotlyWordCloudVisualizer:
    def __init__(self):
        self.fig = go.FigureWidget()

    def update_wordcloud(self, wordcloud_generator):
        words = wordcloud_generator.get_word_frequencies()
        wordcloud = WordCloud(width=800, height=400, background_color="white", max_words=200).generate_from_frequencies(words)

        # Get wordcloud figure as array
        wc_array = np.array(wordcloud.to_image())

        # Create plotly image trace and update figure
        with self.fig.batch_update():
            self.fig.data = []
            self.fig.add_trace(go.Image(z=wc_array))
            self.fig.update_layout(images=[go.layout.Image(
                source=wc_array
            )])
            self.fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
            self.fig.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
            self.fig.layout.template = None


wcg = WordCloudGenerator()
pwcv = PlotlyWordCloudVisualizer()

wcg.add_sentence("This is a sentence.")
pwcv.update_wordcloud(wcg)

wcg.add_sentence("This is another sentence.")
pwcv.update_wordcloud(wcg)

wcg.add_sentence("Yet another sentence.")
pwcv.update_wordcloud(wcg)
