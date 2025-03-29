# LangChain Documentation Helper

A repository for learning LangChain by building a generative AI application.

This is a web application is using a Pinecone as a vectorsotre and answers questions about LangChain 
(sources from LangChain official documentation).

## Tech Stack
Frontend: Streamlit, NextJS ([assistant-ui](https://github.com/assistant-ui/assistant-ui/tree/main) react library for AI chat)
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
  mkdir langchain-docs
  wget -r -A.html -P langchain-docs  https://api.python.langchain.com/en/latest
```

Install dependencies

```bash
  poetry install
```

For simple chat retrieval example using Streamlit:

Start the flask (streamlit) server

```bash
  cd backend
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