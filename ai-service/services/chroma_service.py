import chromadb
from sentence_transformers import SentenceTransformer

# Create persistent ChromaDB client
client = chromadb.PersistentClient(path="./chroma_data")

# Create or load collection
collection = client.get_or_create_collection(
    name="phishing_knowledge"
)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_knowledge(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results["documents"][0]