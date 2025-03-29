import os

from dotenv import load_dotenv
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_community.document_loaders import FireCrawlLoader
from langchain_milvus import Milvus
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()

COLLECTION_NAME = os.getenv('COLLECTION')

embeddings = OpenAIEmbeddings(model="text-embedding-3-large")


def ingest_docs():
    loader = ReadTheDocsLoader("langchain-docs/api.python.langchain.com/en/latest")
    raw_documents = loader.load()

    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600,
                                                   chunk_overlap=50)  # between each chunk there is a 50 token overlap
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")  # updates the source to the correct http address
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Milvus")

    Milvus.from_documents(
        documents=documents,
        embedding=embeddings,
        connection_args={"uri": os.getenv('URI')},
        collection_name=COLLECTION_NAME,
    )

    print("***Loading data to Milvus vector store***")


def ingest_docs_with_firecrawl():
    langchain_documents_base_urls = [
        "https://python.langchain.com/docs/integrations/chat//",
        "https://python.langchain.com/docs/integrations/llms/",
        "https://python.langchain.com/docs/integrations/text_embedding/",
        "https://python.langchain.com/docs/integrations/document_loaders/",
        "https://python.langchain.com/docs/integrations/document_transformers/",
        "https://python.langchain.com/docs/integrations/vectorstores/",
        "https://python.langchain.com/docs/integrations/retrievers/",
        "https://python.langchain.com/docs/integrations/tools/",
        "https://python.langchain.com/docs/integrations/stores/",
        "https://python.langchain.com/docs/integrations/llm_caching/",
        "https://python.langchain.com/docs/integrations/graphs/",
        "https://python.langchain.com/docs/integrations/memory/",
        "https://python.langchain.com/docs/integrations/callbacks/",
        "https://python.langchain.com/docs/integrations/chat_loaders/",
        "https://python.langchain.com/docs/concepts/",
    ]

    for url in langchain_documents_base_urls:
        print(f"FireCrawling {url}=")
        loader = FireCrawlLoader(
            url=url,
            model="crawl",
            params={
                "crawlerOptions": {"limit": 5},
                "pageOption": {"onlyMainContent": True},
                "wait_until_done": True
            }
        )


if __name__ == '__main__':
    ingest_docs()
