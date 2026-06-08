import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_DIR = "chroma_db"
COLLECTION_NAME = "rmp_professor_reviews"

model = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_DIR)
collection = client.get_collection(COLLECTION_NAME)


def retrieve(question, top_k=5):
    query_embedding = model.encode([question]).tolist()[0]

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )

    chunks = []

    for i in range(len(results["documents"][0])):
        chunks.append({
            "source": results["metadatas"][0][i]["source"],
            "chunk_index": results["metadatas"][0][i]["chunk_index"],
            "distance": results["distances"][0][i],
            "text": results["documents"][0][i],
        })

    return chunks


if __name__ == "__main__":
    questions = [
        "Which professor has reasonable or clearly explained exams?",
        "Which professor is described as caring or helpful?",
        "What do students say about attendance expectations?"
    ]

    for question in questions:
        print("\n" + "=" * 80)
        print("QUESTION:", question)
        print("=" * 80)

        results = retrieve(question, top_k=5)

        for chunk in results:
            print("\n---")
            print("Source:", chunk["source"])
            print("Chunk index:", chunk["chunk_index"])
            print("Distance:", round(chunk["distance"], 4))
            print(chunk["text"][:900])