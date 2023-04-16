import os
import streamlit
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()


def init_embeddings_object():
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    openai_api_key = streamlit.secrets["OPENAI_API_KEY"]
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    return embeddings
