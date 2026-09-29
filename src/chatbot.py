import time

from src.rag import get_context
from src.llm import generate_response


def answer_question(query):
    """
    Retrieve relevant Celintex information and
    generate a natural-language response.
    """

    # ========================================================
    # STEP 1: RAG RETRIEVAL
    # ========================================================

    retrieval_start = time.perf_counter()

    context = get_context(query, 3)

    retrieval_time = time.perf_counter() - retrieval_start

    print(
        f"[Speed] RAG retrieval: {retrieval_time:.2f} seconds"
    )

    # ========================================================
    # NO RELEVANT INFORMATION
    # ========================================================

    if not context:
        return (
            "Sorry, I could not find relevant information "
            "in the Celintex knowledge base."
        )

    # ========================================================
    # STEP 2: GEMINI RESPONSE
    # ========================================================

    generation_start = time.perf_counter()

    response = generate_response(
        query,
        context
    )

    generation_time = time.perf_counter() - generation_start

    print(
        f"[Speed] Gemini response: {generation_time:.2f} seconds"
    )

    # ========================================================
    # TOTAL TIME
    # ========================================================

    total_time = retrieval_time + generation_time

    print(
        f"[Speed] Total response time: {total_time:.2f} seconds"
    )

    return response


# ============================================================
# TERMINAL CHATBOT TEST
# ============================================================

if __name__ == "__main__":

    print("===================================")
    print("     CELINTEX FASHION CHATBOT")
    print("===================================")
    print("Type 'exit' to quit.")
    print()

    while True:

        query = input("You: ")

        if query.lower() == "exit":

            print("Chatbot: Goodbye!")

            break

        response = answer_question(query)

        print()
