import os
from typing import List, Tuple, Optional

from dotenv import load_dotenv
from langchain import hub
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain_milvus import Milvus
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from pydantic import BaseModel

load_dotenv()

COLLECTION_NAME = os.getenv('COLLECTION')


class ChatMessage(BaseModel):
    role: str  # "human" or "ai"
    content: str


def run_llm(query: str, chat_history: List[Tuple[str, str]], use_stream: Optional[bool] = False):
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
    milvus = Milvus(connection_args={'uri': os.getenv('URI')},
                    collection_name=COLLECTION_NAME,
                    embedding_function=embeddings)
    chat = ChatOpenAI(temperature=0)

    # provides answers based on the retrieved context
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    # this system prompt helps the AI understand that it should reformulate the question
    # based on the chat history to make it a standalone question
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")

    # default search function for retriever is similarity
    # return k=4 more similar documents
    # this uses the LLM to help reformulate the question based on chat history
    history_aware_retriever = create_history_aware_retriever(
        llm=chat, retriever=milvus.as_retriever(), prompt=rephrase_prompt
    )

    # create a chain to combine documents for question answering
    # `create_stuff_documents_chain` feeds all retrieved context into the LLM
    stuff_documents_chain = create_stuff_documents_chain(
        llm=chat, prompt=retrieval_qa_chat_prompt
    )

    qa = create_retrieval_chain(
        retriever=history_aware_retriever,  # get the relevant documents using the embedding function
        combine_docs_chain=stuff_documents_chain
        # run the combine docs chain, gives us the flexibility to plug ir our own functionality for so qme post-process
    )

    if use_stream:
        def response_generator():
            context = None
            # executes the retrieval chain incrementally
            # returning a stream of output chunks instead of a single response
            for chunk in qa.stream({"input": query, "chat_history": chat_history}):
                # Capture context when it appears
                if "context" in chunk and context is None:
                    context = chunk["context"]

                # Yield answer chunks as they come
                # If an answer appears in the chunk, it is yielded as part of a streaming response
                if "answer" in chunk:
                    yield chunk["answer"]

        return response_generator()
    else:
        result = qa.invoke({"input": query, "chat_history": chat_history})
        new_result = {
            "query": result["input"],
            "result": result["answer"],
            "source_documents": result["context"]
        }
        return new_result
