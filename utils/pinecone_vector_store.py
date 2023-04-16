import os

from dotenv import load_dotenv
from langchain.vectorstores import Pinecone
import pinecone

from utils.vector_store_strategy import SearchStrategy

load_dotenv()

# can be moved to a separate config class
def get_index_name():
    # load environment variables from .env file
    index_name = os.getenv("PINECONE_INDEX_NAME")
    return index_name


def init_pinecone():
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_api_env = os.getenv("PINECONE_API_ENV")
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_api_env)


class PineconeSearch(SearchStrategy):
    def push_documents(self, texts, embeddings):
        init_pinecone()

        index_name = get_index_name()

        num_texts = len(texts)
        print(f'Pushing {num_texts} documents to Pinecone index: {index_name}')

        doc_contents = [t.page_content for t in texts]
        vector_store = Pinecone.from_texts(doc_contents, embeddings, index_name=index_name)
        return vector_store
