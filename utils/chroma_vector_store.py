from langchain.vectorstores import Chroma
from utils.vector_store_strategy import SearchStrategy


class ChromaSearch(SearchStrategy):
    def push_documents(self, texts, embeddings):
        num_texts = len(texts)
        print(f'Pushing {num_texts} documents to Chroma DB')

        for i, text in enumerate(texts):
            text.metadata = {"source": f"{i}-pl"}

        vector_store = Chroma.from_documents(texts, embeddings)

        print(f'Finished pushing {num_texts} documents to Chroma DB')
        return vector_store
