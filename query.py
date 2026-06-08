import os

from dotenv import load_dotenv
from groq import Groq

from retrieve import retrieve

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found. Add it to your .env file.")

client = Groq(api_key=GROQ_API_KEY)


def build_context(chunks):
    """
    Converts retrieved chunks into a context block for the LLM.
    Each chunk includes source filename and chunk index for citation.
    """
    context_parts = []

    for i, chunk in enumerate(chunks, start=1):
        context_parts.append(
            f"[Source {i}: {chunk['source']} | Chunk {chunk['chunk_index']}]\n"
            f"{chunk['text']}"
        )

    return "\n\n".join(context_parts)


def generate_answer(question, chunks):
    """
    Generates a grounded answer using only retrieved chunks.
    """
    context = build_context(chunks)

    system_prompt = """
You are a grounded RAG assistant for an unofficial student guide about UNT Computer Science professors.

Rules:
1. Answer using ONLY the provided context.
2. Do not use outside knowledge.
3. If the context does not directly answer the question, say:
   "I don't have enough information in the provided documents to answer that."
4. Cite source filenames in the answer.
5. Do not invent professor names, ratings, courses, research areas, or claims.
6. If reviews disagree, say that students had mixed opinions.
"""

    user_prompt = f"""
Context:
{context}

Question:
{question}

Write a concise answer. Include the source filename(s) used.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
        temperature=0.1,
    )

    return response.choices[0].message.content


def ask(question):
    """
    End-to-end RAG function:
    1. Retrieve top chunks
    2. Generate grounded answer
    3. Return answer, sources, and retrieved chunks
    """
    chunks = retrieve(question, top_k=5)
    answer = generate_answer(question, chunks)

    sources = sorted(set(chunk["source"] for chunk in chunks))

    return {
        "question": question,
        "answer": answer,
        "sources": sources,
        "retrieved_chunks": chunks,
    }


if __name__ == "__main__":
    question = input("Ask a question: ")
    result = ask(question)

    print("\nANSWER:")
    print(result["answer"])

    print("\nSOURCES RETRIEVED:")
    for source in result["sources"]:
        print("-", source)

    print("\nRETRIEVED CHUNKS:")
    for chunk in result["retrieved_chunks"]:
        print("\n---")
        print("Source:", chunk["source"])
        print("Chunk index:", chunk["chunk_index"])
        print("Distance:", round(chunk["distance"], 4))
        print(chunk["text"][:700])