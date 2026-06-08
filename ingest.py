from pathlib import Path
import re
import json
import html

DOCUMENTS_DIR = Path("documents")
OUTPUT_FILE = Path("chunks.json")


def clean_text(text: str) -> str:
    """
    Clean copied Rate My Professors text.
    Keeps review content but removes messy spacing and HTML artifacts.
    """
    text = html.unescape(text)

    # Remove accidental HTML tags
    text = re.sub(r"<[^>]+>", " ", text)

    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove repeated blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove extra spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()


def chunk_document(text: str, source: str):
    """
    Review-aware chunking.

    Each chunk contains:
    - professor metadata/header
    - one review section

    This keeps the professor name and review together.
    """
    lines = text.splitlines()

    header_lines = []
    review_blocks = []
    current_review = []

    for line in lines:
        line = line.strip()

        if not line:
            continue

        if line.lower().startswith("review "):
            if current_review:
                review_blocks.append("\n".join(current_review))
            current_review = [line]
        else:
            if current_review:
                current_review.append(line)
            else:
                header_lines.append(line)

    if current_review:
        review_blocks.append("\n".join(current_review))

    header = "\n".join(header_lines).strip()

    chunks = []

    for index, review in enumerate(review_blocks):
        chunk_text = f"{header}\n\n{review}".strip()

        if len(chunk_text) > 50:
            chunks.append({
                "id": f"{source}_chunk_{index}",
                "source": source,
                "chunk_index": index,
                "text": chunk_text
            })

    return chunks


def load_documents():
    documents = []

    for path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        raw_text = path.read_text(encoding="utf-8", errors="ignore")
        cleaned_text = clean_text(raw_text)

        if cleaned_text:
            documents.append({
                "source": path.name,
                "text": cleaned_text
            })

    return documents


def main():
    documents = load_documents()

    all_chunks = []

    for doc in documents:
        chunks = chunk_document(doc["text"], doc["source"])
        all_chunks.extend(chunks)

    OUTPUT_FILE.write_text(
        json.dumps(all_chunks, indent=2),
        encoding="utf-8"
    )

    print(f"Loaded documents: {len(documents)}")
    print(f"Created chunks: {len(all_chunks)}")
    print(f"Saved chunks to: {OUTPUT_FILE}")

    print("\nSample 5 chunks:")
    for chunk in all_chunks[:5]:
        print("\n" + "=" * 60)
        print("Source:", chunk["source"])
        print("Chunk index:", chunk["chunk_index"])
        print(chunk["text"][:1000])


if __name__ == "__main__":
    main()