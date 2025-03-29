import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chat import router as chat_router

# Load environment variables
load_dotenv()

app = FastAPI(title="Conversational RAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


app.include_router(chat_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
