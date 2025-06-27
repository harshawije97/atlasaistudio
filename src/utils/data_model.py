from pydantic import BaseModel

class NewMessageModel(BaseModel):
    message: str
    metadata: str
    role: str
    created_at: str
    updated_at: str

class MessageModel(BaseModel):
    message: str
    metadata: str
    chat_history: str
    created_at: str
    updated_at: str