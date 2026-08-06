from pydantic import BaseModel
from typing import Optional


class HadithDocument(BaseModel):
    source_type: str = "hadith"
    hadith_id: str
    collection_name: str
    book_name: str
    hadith_no: str
    narrator_en: Optional[str] = ""
    hadith_ar: Optional[str] = ""
    hadith_en: str
    grade: Optional[str] = "Authentic"
    document_text: str