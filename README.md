# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

This project builds an unofficial guide for student reviews of University of North Texas Computer Science professors using Rate My Professors-style review documents. This knowledge is valuable because official university pages list faculty, courses, and degree requirements, but they do not show student experiences about teaching style, workload, grading, exams, attendance expectations, or whether students would take the professor again. The information is hard to find because it is scattered across separate professor pages and individual student reviews.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

I collected 10 text documents, with one document per professor:

haili_wang_rmp.txt — Student reviews for Haili Wang.
jesus_quevedo_torrero_rmp.txt — Student reviews for Jesus Quevedo-Torrero.
jiang_beilei_rmp.txt — Student reviews for Jiang Beilei.
kirill_morozov_rmp.txt — Student reviews for Kirill Morozov.
russel_pears_rmp.txt — Student reviews for Russel Pears.
ryan_garlick_rmp.txt — Student reviews for Ryan M. Garlick.
sanjukta_bhowmick_rmp.txt — Student reviews for Sanjukta Bhowmick.
stephanie_ludi_rmp.txt — Student reviews for Stephanie Ludi.
tanmay_bera_rmp.txt — Student reviews for Tanmay Bera.
zeenat_tariq_rmp.txt — Student reviews for Zeenat Tariq.

Each document includes professor metadata, overall quality, difficulty, would-take-again percentage when available, and student review entries.

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

I used review-aware chunking. Each document was already structured as one professor profile followed by individual student reviews, so I split the text by review section instead of using only a fixed character limit.

**Chunk size:**
Each chunk contains the professor summary plus one student review, usually around 800–1,200 characters. This size is large enough to keep the professor name, course, rating, difficulty, comment, and tags together.

**Overlap:**
I did not use regular overlap because each review is already a complete standalone unit. I planned to use 200 characters of overlap only as a fallback if a document did not split cleanly by review sections.

**Why these choices fit your documents:**
The documents are short Rate My Professors-style review files, not long articles or guides. One review usually contains one clear student opinion about workload, exams, attendance, grading, or teaching style. Keeping one review with the professor metadata prevents chunks from becoming too small and losing context, while also avoiding large chunks that mix unrelated reviews.

**Final chunk count:**
The pipeline loaded 10 professor documents and created 20 total chunks.

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
I used `sentence-transformers/all-MiniLM-L6-v2` to create embeddings for the review chunks. I chose this model because it runs locally, does not require an API key, is free to use, and works well for semantic search over short text such as professor reviews.

**Production tradeoff reflection:**
For a production system, I would compare embedding models based on retrieval accuracy, latency, cost, context length, and performance on informal student-review language. I would also consider multilingual support and whether the model handles exact terms like professor names, course numbers, and tags well. If cost were not a constraint, I might test a stronger API-hosted embedding model or hybrid search to improve accuracy for exact professor names and course codes.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
My system prompt tells the LLM to answer only from the retrieved chunks and not use outside knowledge. The prompt includes these rules:

Answer using ONLY the provided context.
Do not use outside knowledge.
If the context does not directly answer the question, say:
"I don't have enough information in the provided documents to answer that."
Cite source filenames in the answer.
Do not invent professor names, ratings, courses, research areas, or claims.
If reviews disagree, say that students had mixed opinions.

The retrieved context is formatted with source filenames and chunk indexes, such as:
Source 1: jiang_beilei_rmp.txt | Chunk 0

This helps the model connect each claim to a specific document.

**How source attribution is surfaced in the response:**
Each retrieved chunk includes metadata for the source filename and chunk index. The answer prompt asks the model to cite source filenames directly, and the Gradio interface also displays a separate “Retrieved Sources” box showing the files used during retrieval.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Which professor has reasonable or clearly explained exams? | The system should cite reviews mentioning reasonable exams, clear exam expectations, cheat sheets, or exam preparation. | The system identified Kirill Morozov and Jiang Beilei. It cited Morozov’s review saying his exam style is unique but doable if students study, and Beilei’s review saying exams were reasonable and clearly explained. | Relevant | Accurate |
| 2 | Which professor is described as caring or helpful? | The system should cite reviews or tags mentioning caring, helpfulness, accessibility, or clear explanations. | The system identified professors such as Tanmay Bera, Kirill Morozov, and Haili Wang based on reviews mentioning that they care about students, explain concepts clearly, listen to feedback, or give helpful guidance. | Relevant | Accurate |
| 3 | Which professor seems to have a manageable workload? | The system should cite reviews mentioning manageable homework, enough time for assignments, easy workload, or reasonable class expectations. | The system cited reviews mentioning easy classes, enough time for assignments, non-penalty extensions, or the ability to complete work efficiently. | Partially relevant | Partially accurate |
| 4 | What do students say about attendance expectations? | The system should cite reviews that explicitly mention attendance as mandatory, not mandatory, optional, or important. | The system summarized that attendance expectations vary by professor. Some reviews list attendance as not mandatory, while at least one review lists attendance as mandatory. | Relevant | Accurate |
| 5 | Which professor is best for machine learning research? | The system should say it does not have enough information unless the documents specifically mention machine learning research. | The system should respond that it does not have enough information in the provided documents to answer because the review files discuss class experience, not research specialization. | Relevant if it refuses / Off-target if it retrieves general professor reviews | Accurate if it refuses / Inaccurate if it invents an answer |


**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
Which professor is best to get an A grade?

**What the system returned:**
The system returned professors whose reviews mentioned high grades, easy classes, good ratings, or positive student experiences. However, it treated those review details as evidence for “best,” even though the documents do not directly compare all professors by grade outcomes.

**Root cause (tied to a specific pipeline stage):**
This was mainly a retrieval and data coverage issue. The retrieval step found chunks with related words such as grades, easy class, A, and positive reviews, but the dataset only has a few reviews per professor and does not contain a direct comparison of which professor is best for earning an A. Because the retrieved context was only partially related, the generation step produced a reasonable-sounding answer but could not fully support the comparison.

**What you would change to fix it:**
I would collect more reviews per professor and add metadata fields for grade, difficulty, workload, and exam style. I would also add a rule in the prompt to treat “best” questions as subjective unless the retrieved documents contain direct comparison evidence.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**
The spec helped me decide on review-aware chunking before writing code. Because I had already planned to keep professor metadata together with each student review, the ingestion script was easier to design and the chunks were more useful for retrieval. It also helped me stay focused on the required RAG pipeline instead of adding extra features before the basic system worked.

**One way your implementation diverged from the spec, and why:**
My original plan expected a larger number of chunks, but the final system created 20 chunks from 10 professor documents. I kept this smaller chunk count because each professor file only had about two reviews, and each chunk was intentionally structured as one full review plus professor metadata. This was a practical choice because the project timeline was short, and the final chunks were still readable, self-contained, and useful for retrieval.
---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
I gave ChatGPT my `planning.md` domain, documents, and chunking strategy sections. I explained that my documents were Rate My Professors-style `.txt` files with professor metadata followed by individual reviews.
- *What it produced:*
It helped generate the `ingest.py` script that loads all `.txt` files from the `documents/` folder, cleans whitespace and HTML artifacts, and splits each professor file into review-aware chunks.
- *What I changed or overrode:*
I kept the chunking review-aware instead of using a simple fixed-size split. I also verified the output manually by printing sample chunks and checking that each chunk included the professor name, course, review comment, tags, and source filename.

**Instance 2**

- *What I gave the AI:*
I gave ChatGPT my retrieval approach, including the embedding model `sentence-transformers/all-MiniLM-L6-v2`, ChromaDB as the vector store, and top-k retrieval of 5 chunks.
- *What it produced:*
It helped generate `build_index.py` and `retrieve.py`, which embed the chunks, store them in ChromaDB with source metadata, and retrieve relevant chunks for a user query.
- *What I changed or overrode:*
I tested retrieval with my evaluation questions before adding generation. I reviewed the returned chunks and distance scores to make sure the retrieved reviews were actually relevant to the questions.
