from fastapi import HTTPException, APIRouter
from fastapi.responses import StreamingResponse

from backend.app.schemas.message import MessageContainer
from backend.app.utils import process_message_container, create_sources_string, stream_chat_response
from backend.utils.core import run_llm

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/")
async def chat_endpoint(messages: MessageContainer):
    try:
        formatted_history = process_message_container(messages)

        last_message = messages.messages[-1]
        user_question = last_message.content[0].text
        if messages.use_stream:
            return StreamingResponse(
                stream_chat_response(query=user_question, chat_history=formatted_history),
                media_type="text/event-stream"
            )

        raw_result = run_llm(query=user_question, chat_history=formatted_history)

        # Convert Document objects to the format expected by the response model
        source_documents = [
            {"page_content": doc.page_content, "metadata": doc.metadata}
            for doc in raw_result["source_documents"]
        ]

        print(source_documents)

        sources = set([doc.get('metadata')["source"] for doc in source_documents])
        sources_string = create_sources_string(source_urls=sources)

        formatted_result = {
            "text": raw_result["result"]
        }

        return formatted_result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
