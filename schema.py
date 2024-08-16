from pydantic import BaseModel
from typing import List
from datetime import datetime

class Message(BaseModel):
    role: str
    content: str
    timestamp: datetime
    
    
class Conversation(BaseModel):
    messages: List[Message]
    
    def to_dict(self):
        return {
            "messages": [message.dict() for message in self.messages]
        }