from typing import Literal
from pydantic import BaseModel, Field

class Message(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=6000)

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=6000)
    history: list[Message] = Field(default_factory=list, max_length=20)
    support_style: Literal["listen", "reflect", "practical"] = "reflect"

class ChatResponse(BaseModel):
    reply: str
    safety_notice: str | None = None

class StoryRequest(BaseModel):
    situation: str = Field(min_length=3, max_length=2500)
    tone: Literal["gentle", "realistic", "hopeful"] = "realistic"
    length: Literal["short", "medium"] = "short"

class StoryResponse(BaseModel):
    title: str
    story: str
    reflection: str
    fictional: bool = True

class DiscoveryRequest(BaseModel):
    query: str = Field(min_length=2, max_length=180)
