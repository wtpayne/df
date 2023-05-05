from youtube_transcript_api import YouTubeTranscriptApi
from langchain.chains import VectorDBQAWithSourcesChain
from langchain import OpenAI
import pickle
import os

from .summariser import summarizer
from ..utils import generate_hash

def query_youtube_video(input_array):
    query = input_array[0]
    content_id = generate_hash(input_array[1])

    filename = f"vectors/vector_{content_id}.pkl"
    if not os.path.exists(filename):
        print("Video doesn't exist in vector library. Analysing...")
        summarize_video_transcript(content_id)

    with open(f"vectors/vector_{content_id}.pkl", 'rb') as f:
        vectorstore = pickle.load(f)
        chain = VectorDBQAWithSourcesChain.from_chain_type(OpenAI(temperature=0), chain_type="stuff", vectorstore=vectorstore)
        return chain({"question": query}, return_only_outputs=True)["answer"]

def summarize_video_transcript(content_id):
    # Call the YouTubeTranscriptApi.get_transcript() method to retrieve the transcript for the video.
    transcript_list = YouTubeTranscriptApi.get_transcript(content_id)

    # Join the text of each transcript segment into a single string.
    transcript_text = ""
    for segment in transcript_list:
        transcript_text += segment["text"] + " "

    summary_text = summarizer(transcript_text, content_id)

    return summary_text

