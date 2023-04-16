from abc import abstractmethod, ABC


class SearchStrategy(ABC):
    @abstractmethod
    def push_documents(self, texts, embeddings):
        pass
