from abc import ABC, abstractmethod
from langchain_core.vectorstores.base import VectorStore
from langchain_core.documents import Document


class VectorStoreModel(ABC):
    def __init__(self):
        self.vector_store: VectorStore = None

    @abstractmethod
    def initialize_vector_store(self, uri: str, collection: str, embedding_function):
        pass

    @abstractmethod
    def add_documents(self, documents: list[Document], ids: list[str]):
        pass
