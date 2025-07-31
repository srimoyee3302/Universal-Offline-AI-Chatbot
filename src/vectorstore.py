import os
from langchain_community.vectorstores import FAISS
from langchain.schema import Document

def build_vector_db(chunks, embedding_model, db_path):
    # Validate chunks: they must be instances of Document with valid page_content
    valid_chunks = []
    for i, chunk in enumerate(chunks):
        if isinstance(chunk, Document):
            if hasattr(chunk, "page_content") and isinstance(chunk.page_content, str):
                valid_chunks.append(chunk)
            else:
                print(f"[Chunk Skipped] Invalid or missing page_content at index {i}")
        else:
            print(f"[Chunk Skipped] Not a Document instance at index {i}: {type(chunk)}")

    if not valid_chunks:
        raise ValueError("No valid Document chunks to store in vector DB.")

    db = FAISS.from_documents(valid_chunks, embedding_model)
    db.save_local(db_path)
    print(f"[INFO] Vector database saved to: {db_path}")


def load_vector_db(db_path, embedding_model):
    db = FAISS.load_local(db_path, embedding_model, allow_dangerous_deserialization=True)

    # Optional debug check to validate documents retrieved
    try:
        test_docs = db.similarity_search("test", k=1)
        print(f"[DEBUG] Sample retrieved doc: {test_docs[0] if test_docs else 'None'}")
    except Exception as e:
        print(f"[DEBUG] Error while retrieving from vectorstore: {e}")

    return db
