import pandas as pd
from typing import Tuple
from src.models.quran import QuranDocument
from src.models.hadith import HadithDocument
from src.models.vector_record import VectorRecord


class DocumentFactory:

    @staticmethod
    def create_quran_document(row: pd.Series) -> Tuple[QuranDocument, VectorRecord]:
        surah_no = int(row.get("surah_no", 0))
        ayah_no = int(row.get("ayah_no_surah", row.get("ayah_no", 0)))
        surah_name_en = str(row.get("surah_name_en", ""))
        surah_name_ar = str(row.get("surah_name_ar", ""))
        ayah_ar = str(row.get("ayah_ar", ""))
        ayah_en = str(row.get("ayah_en", ""))
        place_of_revelation = str(row.get("place_of_revelation", "Unknown"))
        juz_no = int(row.get("juz_no", 0))

        document_text = f"""QURAN

Surah: {surah_name_en} ({surah_no})
Ayah: {ayah_no}

Arabic:
{ayah_ar}

English:
{ayah_en}""".strip()

        quran_doc = QuranDocument(
            surah_no=surah_no,
            surah_name_en=surah_name_en,
            surah_name_ar=surah_name_ar,
            ayah_no=ayah_no,
            ayah_ar=ayah_ar,
            ayah_en=ayah_en,
            place_of_revelation=place_of_revelation,
            juz_no=juz_no,
            document_text=document_text,
        )

        record_id = f"quran_{surah_no}_{ayah_no}"
        metadata = {
            "source_type": "quran",
            "surah_no": surah_no,
            "surah_name_en": surah_name_en,
            "surah_name_ar": surah_name_ar,
            "ayah_no": ayah_no,
            "place_of_revelation": place_of_revelation,
            "juz_no": juz_no,
        }

        vector_record = VectorRecord(
            id=record_id,
            document=document_text,
            metadata=metadata
        )

        return quran_doc, vector_record

    @staticmethod
    def create_hadith_document(row: pd.Series, index: int) -> Tuple[HadithDocument, VectorRecord]:
        collection = str(row.get("collection", row.get("collection_name", row.get("source", "Hadith")))).strip()
        book = str(row.get("book", row.get("book_name", row.get("chapter", "General")))).strip()
        hadith_no = str(row.get("hadith_no", str(index + 1))).strip()
        narrator = str(row.get("narrator", row.get("narrator_en", ""))).strip()
        hadith_ar = str(row.get("hadith_ar", row.get("text_ar", "")))
        hadith_en = str(row.get("hadith_en", row.get("text_en", "")))
        grade = str(row.get("grade", "Authentic"))

        document_text = f"""HADITH

Collection: {collection}
Book: {book}
Hadith No: {hadith_no}
Narrator: {narrator}

Arabic:
{hadith_ar}

English:
{hadith_en}""".strip()

        hadith_doc = HadithDocument(
            hadith_id=f"hadith_{index + 1}",
            collection_name=collection,
            book_name=book,
            hadith_no=hadith_no,
            narrator_en=narrator,
            hadith_ar=hadith_ar,
            hadith_en=hadith_en,
            grade=grade,
            document_text=document_text
        )

        metadata = {
            "source_type": "hadith",
            "collection_name": collection,
            "book_name": book,
            "hadith_no": hadith_no,
            "narrator_en": narrator,
            "grade": grade
        }

        vector_record = VectorRecord(
            id=f"hadith_{index + 1}",
            document=document_text,
            metadata=metadata
        )

        return hadith_doc, vector_record