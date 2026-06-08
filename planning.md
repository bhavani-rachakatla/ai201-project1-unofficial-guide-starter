# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

My domain is student reviews of University of North Texas Computer Science professors, using Rate My Professors-style review documents. This knowledge is valuable because official university pages list faculty, courses, and degree requirements, but they do not show student experiences about teaching style, workload, grading, exams, attendance expectations, or whether students would take the professor again. It is hard to find otherwise because the information is scattered across separate professor pages and individual student reviews, making it difficult to compare professors or search for specific concerns in one place.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

I collected 10 Rate My Professors-style text documents, with one document per University of North Texas Computer Science professor. Each document contains professor-level metadata such as overall quality, difficulty, would-take-again percentage when available, and 2 student review entries with course, quality, difficulty, attendance, grade, comment, and tags.

1. haili_wang_rmp.txt — Student reviews for Haili Wang.
2. jesus_quevedo_torrero_rmp.txt — Student reviews for Jesus Quevedo-Torrero.
3. jiang_beilei_rmp.txt — Student reviews for Jiang Beilei.
4. kirill_morozov_rmp.txt — Student reviews for Kirill Morozov.
5. russel_pears_rmp.txt — Student reviews for Russel Pears.
6. ryan_garlick_rmp.txt — Student reviews for Ryan M. Garlick.
7. sanjukta_bhowmick_rmp.txt — Student reviews for Sanjukta Bhowmick.
8. stephanie_ludi_rmp.txt — Student reviews for Stephanie Ludi.
9. tanmay_bera_rmp.txt — Student reviews for Tanmay Bera.
10. zeenat_tariq_rmp.txt — Student reviews for Zeenat Tariq.

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
Each chunk will contain the professor summary plus one student review, with a target size of about 800–1,200 characters.

**Overlap:**
I will use 200 characters of overlap only as a fallback if a document does not split cleanly by review sections.

**Reasoning:**
My documents are short Rate My Professors-style review files, so review-aware chunking fits better than fixed-size chunking. Each review usually contains one complete student opinion about workload, exams, grading, attendance, or teaching style. Keeping the professor metadata with each review helps the system know which professor and course the comment belongs to. If chunks are too small, retrieval may return fragments without enough context. If chunks are too large, multiple reviews may get mixed together and the answer may overgeneralize.
---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
I will use `sentence-transformers/all-MiniLM-L6-v2` to create embeddings for each review chunk. I chose this model because it runs locally, is free to use, and is suitable for semantic similarity search over short text such as student reviews.

**Top-k:**
I will retrieve the top 5 most relevant chunks for each user query. Top 5 should provide enough context to compare a few relevant professor reviews without overwhelming the LLM with too many loosely related chunks.

**Production tradeoff reflection:**
For a production system, I would compare embedding models based on retrieval accuracy, latency, cost, context length, and support for informal student-review language. I would also consider whether the model handles exact terms like professor names and course codes well. If cost were not a constraint, I might test a stronger embedding model or hybrid search, because semantic search alone may miss exact professor names, course numbers, or short phrases from reviews.
---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question                                                        | Expected answer                                                                                                                                                                        |
| - | --------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Which professor has reasonable or clearly explained exams?      | The system should identify professor(s) whose reviews mention reasonable exams, clear exam expectations, cheat sheets, or helpful exam preparation, and cite the correct review file.  |
| 2 | Which professor is described as caring, helpful, or accessible? | The system should identify professor(s) whose reviews or tags mention being caring, helpful, accessible outside class, or giving clear explanations, and cite the correct source file. |
| 3 | Which professor seems to have a manageable workload?            | The system should cite review(s) that mention manageable homework, enough time for assignments, easy workload, or reasonable class expectations.                                       |
| 4 | What do students say about attendance expectations?             | The system should cite reviews that explicitly mention whether attendance is mandatory, not mandatory, optional, or important for success.                                             |
| 5 | Which professor is best for machine learning research?          | The system should say it does not have enough information in the provided documents unless the reviews specifically mention machine learning research.                                 |


---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. Reviews may be subjective or inconsistent, so the system may need to mention mixed opinions instead of giving one final judgment.

2. Retrieval may return weakly related chunks because the dataset is small and student review language is informal.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

```mermaid
flowchart LR
    A[Rate My Professors TXT Files] --> B[Ingestion and Cleaning]
    B --> C[Review-Aware Chunking]
    C --> D[Embeddings: all-MiniLM-L6-v2]
    D --> E[Vector Store: ChromaDB]
    E --> F[Retrieval: Top 5 Chunks]
    F --> G[Generation: Groq llama-3.3-70b-versatile]
    G --> H[Interface: Gradio]
```
---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will use ChatGPT to help write Python code that loads .txt files from the documents/ folder and splits them using my review-aware chunking strategy. I will give it my Chunking Strategy section and verify the output by printing 5 sample chunks.

**Milestone 4 — Embedding and retrieval:**
I will use ChatGPT to help implement embeddings with sentence-transformers/all-MiniLM-L6-v2 and store them in ChromaDB. I will give it my Retrieval Approach section and verify the output by testing at least 3 queries and checking whether the retrieved chunks are relevant.

**Milestone 5 — Generation and interface:**
I will use ChatGPT to help write the grounded LLM prompt and build a simple Gradio interface. I will verify that answers cite source files and that out-of-scope questions return “not enough information” instead of made-up answers.
