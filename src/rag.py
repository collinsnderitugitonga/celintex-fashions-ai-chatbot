import os
import re
import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

KNOWLEDGE_FILE = os.path.join(
    BASE_DIR,
    "data",
    "celintex_knowledge.txt"
)

CHROMA_DIR = os.path.join(
    BASE_DIR,
    "chroma_db"
)


# ============================================================
# CHROMADB SETUP
# ============================================================

client = chromadb.PersistentClient(
    path=CHROMA_DIR
)

embedding_function = DefaultEmbeddingFunction()

collection = client.get_or_create_collection(
    name="celintex_knowledge",
    embedding_function=embedding_function
)

# ============================================================
# LOAD KNOWLEDGE BASE
# ============================================================

def load_knowledge_base():
    """
    Read the Celintex knowledge base.
    """

    with open(
        KNOWLEDGE_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()


# ============================================================
# SECTION-AWARE CHUNKING
# ============================================================

def split_into_sections(text):
    """
    Split the knowledge base into numbered sections.
    """

    pattern = r"(?=^==================================================\s*\d+\.)"

    sections = re.split(
        pattern,
        text,
        flags=re.MULTILINE
    )

    sections = [
        section.strip()
        for section in sections
        if section.strip()
    ]

    return sections


def split_large_section(section, max_chars=1500):
    """
    Split large sections into smaller chunks.
    """

    if len(section) <= max_chars:
        return [section]

    paragraphs = re.split(
        r"\n\s*\n",
        section
    )

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:

        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if (
            current_chunk
            and len(current_chunk) + len(paragraph) + 2
            > max_chars
        ):

            chunks.append(
                current_chunk.strip()
            )

            current_chunk = paragraph

        else:

            if current_chunk:
                current_chunk += "\n\n"

            current_chunk += paragraph

    if current_chunk:
        chunks.append(
            current_chunk.strip()
        )

    return chunks


# ============================================================
# BUILD VECTOR DATABASE
# ============================================================

def build_knowledge_base():
    """
    Load the knowledge base and store it in ChromaDB.
    """

    global collection

    try:
        client.delete_collection(
            name="celintex_knowledge"
        )
    except Exception:
        pass

    collection = client.create_collection(
        name="celintex_knowledge",
        embedding_function=embedding_function
    )

    text = load_knowledge_base()

    sections = split_into_sections(text)

    documents = []
    ids = []
    metadatas = []

    chunk_number = 0

    for section in sections:

        match = re.search(
            r"^==================================================\s*(\d+\.\s*.+?)\s*=*$",
            section,
            flags=re.MULTILINE
        )

        if match:
            section_name = match.group(1).strip()

        else:
            section_name = "General"

        chunks = split_large_section(
            section
        )

        for chunk in chunks:

            documents.append(
                chunk
            )

            ids.append(
                f"celintex_chunk_{chunk_number}"
            )

            metadatas.append(
                {
                    "section": section_name
                }
            )

            chunk_number += 1

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(
        "Knowledge base indexed successfully."
    )

    print(
        f"Sections found: {len(sections)}"
    )

    print(
        f"Chunks stored: {len(documents)}"
    )


# ============================================================
# SEARCH
# ============================================================

def get_context(query, n_results=3):
    """
    Retrieve relevant information from the Celintex knowledge base.

    Uses direct section matching for common business questions
    and semantic search as a fallback.
    """

    query_lower = query.lower()

    # ========================================================
    # DIRECT SECTION MATCHING
    # ========================================================

    section_keywords = []

    if (
        "opening" in query_lower
        or "hours" in query_lower
        or "open" in query_lower
        or "closing" in query_lower
        or "working hours" in query_lower
    ):
        section_keywords = [
            "1. COMPANY"
        ]

    elif (
        "where" in query_lower
        or "location" in query_lower
        or "address" in query_lower
        or "located" in query_lower
    ):
        section_keywords = [
            "1. COMPANY"
        ]

    elif (
        "custom suit" in query_lower
        or "custom suits" in query_lower
        or "men's suit" in query_lower
        or "mens suit" in query_lower
        or "men suit" in query_lower
    ):
        section_keywords = [
            "7. MEN’S SUITS",
            "9. PRICING RULES"
        ]

    elif (
        "price" in query_lower
        or "prices" in query_lower
        or "cost" in query_lower
        or "costs" in query_lower
        or "how much" in query_lower
    ):
        section_keywords = [
            "9. PRICING RULES"
        ]

    elif (
        "wedding gown" in query_lower
        and (
            "hire" in query_lower
            or "rent" in query_lower
            or "rental" in query_lower
        )
    ):
        section_keywords = [
            "14. WEDDING GOWN HIRE",
            "30. WEDDING GOWN HIRE FAQ"
        ]

    elif (
        "repair" in query_lower
        or "repairs" in query_lower
        or "alteration" in query_lower
        or "alterations" in query_lower
    ):
        section_keywords = [
            "8. CLOTHING REPAIRS"
        ]

    elif (
        "vitenge" in query_lower
        or "african" in query_lower
    ):
        section_keywords = [
            "3. CUSTOMIZED VITENGE"
        ]

    # ========================================================
    # DIRECT SECTION SEARCH
    # ========================================================

    if section_keywords:

        all_data = collection.get(
            include=[
                "documents",
                "metadatas"
            ]
        )

        documents = all_data.get(
            "documents",
            []
        )

        metadatas = all_data.get(
            "metadatas",
            []
        )

        selected = []

        for document, metadata in zip(
            documents,
            metadatas
        ):

            if metadata is None:
                continue

            section = metadata.get(
                "section",
                ""
            )

            for target in section_keywords:

                if target.lower() in section.lower():

                    selected.append(
                        (
                            section,
                            document
                        )
                    )

                    break

        if selected:

            context_parts = []
            seen = set()

            for section, document in selected:

                if document in seen:
                    continue

                seen.add(document)

                context_parts.append(
                    f"[{section}]\n{document}"
                )

                if len(context_parts) >= n_results:
                    break

            return "\n\n".join(
                context_parts
            )

    # ========================================================
    # SEMANTIC SEARCH FALLBACK
    # ========================================================

    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    documents = results.get(
        "documents",
        [[]]
    )[0]

    metadatas = results.get(
        "metadatas",
        [[]]
    )[0]

    context_parts = []
    seen = set()

    for document, metadata in zip(
        documents,
        metadatas
    ):

        if document in seen:
            continue

        seen.add(document)

        if metadata is None:
            metadata = {}

        section = metadata.get(
            "section",
            "General"
        )

        context_parts.append(
            f"[{section}]\n{document}"
        )

    return "\n\n".join(
        context_parts
    )

# ============================================================
# TEST
# ============================================================

if __name__ == "__main__":

    print(
        "==================================="
    )

    print(
        "       CELINTEX RAG SYSTEM"
    )

    print(
        "==================================="
    )

    build_knowledge_base()

    print(
        "\nTesting search...\n"
    )

    question = (
        "What are the opening hours?"
    )

    context = get_context(
        question,
        n_results=3
    )

    print(
        "Question:",
        question
    )

    print(
        "\nRelevant information:"
    )

    print(
        context
    )
