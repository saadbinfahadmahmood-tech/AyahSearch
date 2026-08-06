from pydantic import BaseModel


class QuranDocument(BaseModel):
    source_type: str = "quran"
    surah_no: int
    surah_name_en: str
    surah_name_ar: str
    ayah_no: int
    ayah_ar: str
    ayah_en: str
    place_of_revelation: str
    juz_no: int
    document_text: str