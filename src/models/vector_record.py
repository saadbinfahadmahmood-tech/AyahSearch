from typing import Any, Dict
from pydantic import BaseModel


class VectorRecord(BaseModel):
    id: str
    document: str
    metadata: Dict[str, Any]