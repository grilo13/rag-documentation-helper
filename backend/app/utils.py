from typing import Set, List, Tuple
import json
from schemas.message import MessageContainer
from backend.src.utils.core import run_llm


def process_message_container(message_container: MessageContainer) -> List[Tuple[str, str]]:
    """
    Process a MessageContainer to extract formatted history of (human, ai) message pairs.

    Args:
        message_container: The input MessageContainer with messages in the original format

    Returns:
        List of tuples containing (human_content, ai_content) pairs
    """
    # Convert messages to simple role/content pairs
    processed_messages = []

    for message in message_container.messages:
        # Convert role from "user" to "human" and "assistant" to "ai"
        role = "human" if message.role == "user" else "ai"

        # Combine all text content into a single string
        content = " ".join([item.text for item in message.content if item.type == "text"])

        # Add to processed messages
        processed_messages.append({"role": role, "content": content})

    return processed_messages


def create_sources_string(source_urls: Set[str]) -> str:
    if not source_urls:
        return ""
    sources_list = list(source_urls)
    sources_list.sort()
    sources_string = "sources:\n"
    for i, source in enumerate(sources_list):
        sources_string += f"- {source}\n"
    return sources_string


def stream_chat_response(query: str, chat_history: List[Tuple[str, str]]):
    """Generator function that yields streaming chat responses"""
    response_stream = run_llm(query, chat_history, use_stream=True)
    for chunk in response_stream:
        # Format according to SSE specification
        yield f"data: {json.dumps({'chunk': chunk})}\n\n"
