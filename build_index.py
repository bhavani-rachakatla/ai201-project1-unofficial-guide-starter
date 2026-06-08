import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

CHUNKS_FILE = Path("chunks.json")
CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "rmp_professor_reviews"


def main():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError("chunks.json not found. Run python ingest.py first.")

    chunks = json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))

    print(f"Loaded {len(chunks)} chunks from chunks.json")

    # Load local embedding model
    print("Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    texts = [chunk["text"] for chunk in chunks]
    ids = [chunk["id"] for chunk in chunks]

    # Metadata is important for citations later
    metadatas = [
        {
            "source": chunk["source"],
            "chunk_index": chunk["chunk_index"],
        }
        for chunk in chunks
    ]

    print("Creating embeddings...")
    embeddings = model.encode(texts).tolist()

    # Create persistent ChromaDB database
    client = chromadb.PersistentClient(path=CHROMA_DIR)

    # Delete old collection so rebuild is clean
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print("Index built successfully.")
    print(f"Stored chunks in ChromaDB: {collection.count()}")


if __name__ == "__main__":
    main()