from langchain.schema.document import Document
from langchain_community.vectorstores import FAISS

from .base import VectorStoreModel


class FaissVectorStore(VectorStoreModel):
    def initialize_vector_store(self, uri: str, collection: str, embedding_function):
        self.vector_store = FAISS(
            embedding_function=embedding_function,
        )
        return self.vector_store

    def initialize_from_documents(self, docs: list[Document], embedding_function):
        """Create a new vector store from documents"""
        self.vector_store = FAISS.from_documents(docs, embedding_function)
        return self.vector_store

    def save_vector_store(self, path: str):
        """Save the vector store to a local path"""
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Initialize first.")

        self.vector_store.save_local(path)

    def load_vector_store(self, path: str, embedding_function):
        """Load a vector store from a local path"""
        self.vector_store = FAISS.load_local(
            path,
            embedding_function,
            allow_dangerous_deserialization=True
        )
        return self.vector_store

    def add_documents(self, documents: list[Document], ids: list[str]) -> list[str]:
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call initialize_vector_store first.")

        return self.vector_store.add_documents(documents=documents, ids=ids)
