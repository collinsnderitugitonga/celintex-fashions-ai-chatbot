from google import genai

from src.config import GEMINI_API_KEY, MODEL_NAME


if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY is not set in the .env file."
    )


client = genai.Client(
    api_key=GEMINI_API_KEY
)


SYSTEM_PROMPT = """
You are the AI customer assistant for Celintex Fashion Company.

Your job is to answer customer questions using ONLY the information
provided in the retrieved Celintex knowledge base.

Rules:

1. Do not invent prices, products, services, stock, delivery details,
   payment details, order status, or policies.

2. If the knowledge base says information must be confirmed by Celintex,
   clearly tell the customer that it needs confirmation.

3. Keep answers friendly, professional, concise, and easy to understand.

4. When appropriate, provide the Celintex contact number:
   0722285544

5. If the retrieved information does not answer the customer's question,
   say that you don't have enough information and direct the customer
   to contact Celintex.

6. Never pretend that you checked information that is not in the
   knowledge base.
"""


def stream_response(query, context):
    """
    Stream Gemini's response chunk by chunk.
    """

    prompt = f"""
{SYSTEM_PROMPT}

CUSTOMER QUESTION:
{query}

RETRIEVED CELINTEX INFORMATION:
{context}

Answer the customer's question using the information above.
"""

    stream = client.interactions.create(
        model=MODEL_NAME,
        input=prompt,
        stream=True
    )

    for event in stream:

        if event.event_type == "step.delta":

            if event.delta.type == "text":

                text = event.delta.text

                if text:
                    yield text
def generate_response(query, context):
    """
    Generate a complete Gemini response.
    """

    prompt = f"""
{SYSTEM_PROMPT}

CUSTOMER QUESTION:
{query}

RETRIEVED CELINTEX INFORMATION:
{context}

Answer the customer's question using the information above.
"""

    response = client.interactions.create(
        model=MODEL_NAME,
        input=prompt
    )

    return response.output_text
