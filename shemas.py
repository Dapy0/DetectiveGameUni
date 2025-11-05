from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ScriptNode(BaseModel):
    id: str
    speaker: str
    text: str
    tags: Optional[List[str]] = None
