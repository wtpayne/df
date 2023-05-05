import openai
import pickle
import os

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

from ..utils import generate_hash


def chunk_text2(text, chunk_max_size=2000, overlap_percentage=0.10):
    # Calculate the maximum chunk size based on the desired overlap percentage
    overlap_size = int(chunk_max_size * overlap_percentage)
    chunk_size = chunk_max_size - overlap_size
    
    # Calculate the number of chunks based on the length of the input text
    num_chunks = int((len(text) + chunk_size - 1) / chunk_size)
    
    # Initialize the list of chunks
    chunks = []
    
    # Loop through the input text, adding chunks to the list
    for i in range(num_chunks):
        start = i * chunk_size
        end = min((i + 1) * chunk_size + overlap_size, len(text))
        chunks.append(text[start:end])

    return chunks

def create_vectors(text, summary, content_id):
    metadata = {"source": content_id}
    document = Document(page_content=summary+text, metadata=metadata)

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )

    documents = text_splitter.split_documents([document])

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(documents, embeddings)

    vec_file_name = f"vector_{generate_hash(content_id)}.pkl"
    vec_path = os.path.join("vectors", vec_file_name)

    with open(vec_path, "wb") as f:
        pickle.dump(vectorstore, f)
        print("saved file")

def summarizer(text, content_id):
    texts = chunk_text2(text)

    summaries = []
    for i, text_ in enumerate(texts):

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Please summarize the following text:\n{text_}\n\nSummary:",
            temperature=0.7,
            max_tokens=500,
            n=1,
            stop=None
        )
        summary = response.choices[0].text.strip()
        print(f"Summary {i} out of {len(texts)}: {summary}")
        summaries.append(summary)

    joined_summaries = '\n'.join(summaries)
    
    if len(joined_summaries) < 1000:
        create_vectors(text, joined_summaries, content_id)
        return joined_summaries
    
    final_summary = summarizer(joined_summaries, content_id)

    return final_summary