# LangChain Documentation Helper

This project implements a Retrieval-Augmented Generation (RAG) pipeline by storing documents in a Milvus vector database, enabling efficient similarity searches. 

It features:
- Document Ingestion: Embeds and stores documents in Milvus for retrieval
- Custom API Backend (FastAPI): Handles LLM context interaction and document retrieval
- Next.js + Assistant UI: A chat interface for user interaction, integrating real-time streaming responses from the LLM

### Assistant UI Example

![Description](https://github.com/grilo13/rag-documentation-helper/blob/main/static/assistant_ui_rag.gif)

### Streamlit Example

![Description](https://github.com/grilo13/rag-documentation-helper/blob/main/static/streamlit_rag.gif)

## Tech Stack
Frontend: Streamlit, Next.js ([assistant-ui](https://github.com/assistant-ui/assistant-ui/tree/main) react library for AI chat)
Server Side: LangChain, FastAPI
Vectorstore: Milvus

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`URI`: URI for the Milvus vector store

`COLLECTION`: collection to store and retrieve documents

`OPENAI_API_KEY`

## Run Locally

Clone the project

```bash
  git clone https://github.com/grilo13/rag-documentation-helper.git
```

Go to the project directory

```bash
  cd documentation-helper
```

Download LangChain Documentation
```bash
  cd backend
  mkdir langchain-docs
  wget -r -A.html -P langchain-docs  https://api.python.langchain.com/en/latest
```

Install dependencies

```bash
  poetry install
```

Insert the documents in the Milvus Vector Store
```bash
  python ingestion.py
```

For simple chat retrieval example using Streamlit:

Start the flask (streamlit) server

```bash
  streamlit run streamlit_app.py
```

For complex usage using Next.js + AssistantUI and FastAPI app:

Run API (on localhost:8000)

```bash
  cd backend/app/
  python main.py
```

Install Next.js dependencies

```bash
npm install
```

And run Next.js app (on localhost:3000)

```bash
  cd frontend
  npm run dev
```

## 🔗 Links
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/pedrogrilo13/)
