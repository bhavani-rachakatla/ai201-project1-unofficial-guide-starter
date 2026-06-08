import gradio as gr

from query import ask


def handle_query(question):
    if not question.strip():
        return "Please enter a question.", "", ""

    result = ask(question)

    answer = result["answer"]

    sources = "\n".join(
        f"• {source}" for source in result["sources"]
    )

    retrieved_chunks = "\n\n".join(
        f"Source: {chunk['source']} | Chunk: {chunk['chunk_index']} | Distance: {chunk['distance']:.4f}\n"
        f"{chunk['text'][:800]}"
        for chunk in result["retrieved_chunks"]
    )

    return answer, sources, retrieved_chunks


with gr.Blocks() as demo:
    gr.Markdown("# The Unofficial Guide: Rate My CS Professor")
    gr.Markdown(
        "Ask questions about UNT Computer Science professor reviews. "
        "Answers are grounded only in the collected review documents."
    )

    question = gr.Textbox(
        label="Your question",
        placeholder="Example: Which professor has reasonable exams?",
    )

    ask_button = gr.Button("Ask")

    answer = gr.Textbox(label="Answer", lines=8)
    sources = gr.Textbox(label="Retrieved Sources", lines=5)
    retrieved_chunks = gr.Textbox(label="Retrieved Chunks", lines=14)

    ask_button.click(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved_chunks],
    )

    question.submit(
        handle_query,
        inputs=question,
        outputs=[answer, sources, retrieved_chunks],
    )


if __name__ == "__main__":
    demo.launch()