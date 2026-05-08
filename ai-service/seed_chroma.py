from pathlib import Path
from services.chroma_service import collection

knowledge_dir = Path("knowledge")

for idx, file in enumerate(knowledge_dir.glob("*.txt")):
    content = file.read_text(encoding="utf-8")

    collection.add(
        documents=[content],
        ids=[str(idx)],
        metadatas=[{"source": file.name}]
    )

    print(f"Added: {file.name}")

print("ChromaDB seeded successfully.")