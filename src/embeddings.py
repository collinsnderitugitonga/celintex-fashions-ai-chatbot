import chromadb
from chromadb.utils.embedding_functions import DefaultEmbeddingFunction


# Create the embedding function
embedding_function = DefaultEmbeddingFunction()


def create_embedding(text):
    """
    Convert text into a numerical embedding vector.
    """
    embedding = embedding_function([text])
    return embedding[0]


if __name__ == "__main__":
    text = "Celintex Fashion Company sells men's suits and wedding gowns."

    embedding = create_embedding(text)

    print("Embedding created successfully")
    print("Embedding length:", len(embedding))
