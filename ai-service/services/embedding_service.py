from sentence_transformers import SentenceTransformer

embedding_model = None


def load_embedding_model():
    global embedding_model

    if embedding_model is None:
        print("Loading embedding model...")

        embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Embedding model loaded.")

    return embedding_model


def create_embedding(text):
    global embedding_model

    if embedding_model is None:
        load_embedding_model()

    vector = embedding_model.encode(text)

    return vector.tolist()