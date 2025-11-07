import datetime
import json
from enum import Enum

class Status(Enum):
    ACTIVE = "active"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Note:
    def __init__(self, title, content, status=Status.ACTIVE, priority=Priority.MEDIUM, tags=None):
        self.id = None 
        self.title = title
        self.content = content
        self.status = status
        self.priority = priority
        self.tags = tags or []
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()
    
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "status": self.status.value,
            "priority": self.priority.value,
            "tags": self.tags,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data):
        note = cls(
            title=data["title"],
            content=data["content"],
            status=Status(data["status"]),
            priority=Priority(data["priority"]),
            tags=data["tags"]
        )
        note.id = data["id"]
        note.created_at = datetime.datetime.fromisoformat(data["created_at"])
        note.updated_at = datetime.datetime.fromisoformat(data["updated_at"])
        return note