from langchain.schema.document import Document
from langchain_milvus import Milvus

from .base import VectorStoreModel


class MilvusVectorStore(VectorStoreModel):
    def initialize_vector_store(self, uri: str, collection: str, embedding_function):
        self.vector_store = Milvus(
            connection_args={'uri': uri},
            collection_name=collection,
            embedding_function=embedding_function
        )
        return self.vector_store

    def add_documents(self, documents: list[Document], ids: list[str]) -> list[str]:
        if not self.vector_store:
            raise ValueError("Vector store not initialized. Call initialize_vector_store first.")

        return self.vector_store.add_documents(documents=documents, ids=ids)
