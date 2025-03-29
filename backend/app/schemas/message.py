from datetime import datetime
from typing import List, Dict, Optional, Literal, Any

from pydantic import BaseModel, Field


class TextContent(BaseModel):
    type: Literal["text"]
    text: str


class MessageMetadata(BaseModel):
    custom: Dict[str, Any] = Field(default_factory=dict)


class Message(BaseModel):
    id: str
    createdAt: datetime
    role: Literal["user", "assistant", "system"]
    content: List[TextContent]
    attachments: List[Any] = Field(default_factory=list)
    metadata: MessageMetadata


class MessageContainer(BaseModel):
    messages: List[Message]
    use_stream: Optional[bool] = False
