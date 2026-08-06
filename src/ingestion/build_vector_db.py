import os
import pandas as pd
from src.config.settings import settings
from src.factories.document_factory import DocumentFactory
from src.repositories.chroma_repository import ChromaRepository

from ollama import Client

client = Client(
    host="http://localhost:11434",
    timeout=160000
)

def build_quran_collection(raw_dir: str):
    quran_path = os.path.join(raw_dir, "quran.csv")
    if not os.path.exists(quran_path):
        print(f"[-] Quran dataset not found at {quran_path}. Skipping.")
        return

    print("[+] Loading Quran raw CSV...")
    df = pd.read_csv(quran_path)
    
    # records = [DocumentFactory.create_quran_document(row)[1] for _, row in df.iterrows()]
    
    records = []

    for _, row in df.iterrows():
        # Make the document from the row
        result = DocumentFactory.create_quran_document(row)

        # Grab the second item (index 1)
        second_item = result[1]

        # Add it to our list
        records.append(second_item)


    repo = ChromaRepository(
        db_path=settings.chroma_path,
        collection_name=settings.quran_collection
    )

    total_records = len(records)
    batch_size = 5
    print(f"[+] Indexing {total_records} Quran verses into ChromaDB...")

    # Process in batches to track percentage progress
    for i in range(0, total_records, batch_size):
        batch = records[i:i + batch_size]
        repo.add_documents(batch, batch_size=batch_size)
        
        processed = min(i + batch_size, total_records)
        percentage = (processed / total_records) * 100
        print(f"[{percentage:.2f}%] Indexed {processed}/{total_records} records", end="\r")

    print(f"\n[✓] Quran indexing completed.")


# def build_hadith_collection(raw_dir: str):
#     hadith_path = os.path.join(raw_dir, "hadith.csv")
#     if not os.path.exists(hadith_path):
#         print(f"[-] Hadith dataset not found at {hadith_path}. Skipping.")
#         return

#     print("[+] Loading Hadith raw CSV...")
#     df = pd.read_csv(hadith_path)
#     records = [DocumentFactory.create_hadith_document(row, idx)[1] for idx, row in df.iterrows()]

#     repo = ChromaRepository(
#         db_path=settings.chroma_path,
#         collection_name=settings.hadith_collection
#     )

#     total_records = len(records)
#     batch_size = 5
#     print(f"[+] Indexing {total_records} Hadiths into ChromaDB...")

#     for i in range(0, total_records, batch_size):
#         batch = records[i:i + batch_size]
#         repo.add_documents(batch, batch_size=batch_size)
        
#         processed = min(i + batch_size, total_records)
#         percentage = (processed / total_records) * 100
#         print(f"[{percentage:.2f}%] Indexed {processed}/{total_records} records", end="\r")

#     print(f"\n[✓] Hadith indexing completed.")


def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    raw_dir = os.path.join(root_dir, "data", "raw")
    os.makedirs(settings.chroma_path, exist_ok=True)

    build_quran_collection(raw_dir)
    # build_hadith_collection(raw_dir)

    print("=== Vector Database Build Complete ===")


if __name__ == "__main__":
    main()