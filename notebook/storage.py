import json
import os
from typing import List, Optional
from models import Note

class Storage:
    def __init__(self, filename="notes.json"):
        self.filename = filename
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump([], f)
    
    def load_notes(self) -> List[Note]:
        with open(self.filename, 'r') as f:
            data = json.load(f)
        return [Note.from_dict(note_data) for note_data in data]
    
    def save_notes(self, notes: List[Note]):
        with open(self.filename, 'w') as f:
            json.dump([note.to_dict() for note in notes], f, indent=2)
    
    def get_next_id(self, notes: List[Note]) -> int:
        if not notes:
            return 1
        return max(note.id for note in notes) + 1