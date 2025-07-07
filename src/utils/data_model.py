from typing import Any, Dict
from pydantic import BaseModel


class MetaDataModel(BaseModel):
    index: str
    namespace: str


class NewMessageModel(BaseModel):
    message: str
    metadata: str
    role: str
    created_at: str
    updated_at: str


class MessageModel(BaseModel):
    message: str
    metadata: MetaDataModel
    role: str
    chat_history: str
    created_at: str
    updated_at: str


class SaveMessageModel(BaseModel):
    conversation_id: str
    user_id: str
    message: MessageModel
