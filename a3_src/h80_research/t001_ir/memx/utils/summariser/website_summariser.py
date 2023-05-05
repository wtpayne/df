from langchain.chains import VectorDBQAWithSourcesChain
from langchain import OpenAI
import requests
from bs4 import BeautifulSoup
import os
import pickle

from .summariser import summarizer
from ..utils import generate_hash


def query_website(input_array):
    query = input_array[0]
    content_id = generate_hash(input_array[1])

    filename = f"vectors/vector_{content_id}.pkl"
    if not os.path.exists(filename):
        print("Video doesn't exist in vector library. Analysing...")
        summarize_website(content_id)

    with open(f"vectors/vector_{content_id}.pkl", 'rb') as f:
        vectorstore = pickle.load(f)
        chain = VectorDBQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", vectorstore=vectorstore)
        return chain({"question": query}, return_only_outputs=True)["answer"]

def summarize_website(url):
    # Use requests to get the HTML content of the website.
    response = requests.get(url)
    html_content = response.content

    # Use BeautifulSoup to extract the text from the HTML content.
    soup = BeautifulSoup(html_content, 'html.parser')
    text = soup.get_text()

    summary_text = summarizer(text, url)

    # Return the summary text.
    return summary_text