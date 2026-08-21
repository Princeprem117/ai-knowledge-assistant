from vectordb.chroma_db import ChromaVectorStore


store = ChromaVectorStore(
    persist_directory="data/chroma"
)

print("\n========== CHROMA STATE ==========")

print("Total vectors:")
print(store.collection.count())

results = store.collection.get(
    include=["metadatas"]
)

print("\nStored IDs:")
print(results["ids"])

print("\nStored metadata:")
print(results["metadatas"])

print("==================================\n")