from models.document import Document
from chunkers.recursive_chunker import RecursiveChunker


document = Document(
    content=(
        "Agents and Environments\n\n"
        "An agent is anything that can be viewed as perceiving "
        "its environment through sensors and acting upon that "
        "environment through actuators.\n\n"
        "A rational agent is one that does the right thing. "
        "A rational agent should be autonomous."
    ),
    metadata={"source": "sample.txt"}
)


chunker = RecursiveChunker(
    chunk_size=100,
    chunk_overlap=20
)


chunks = chunker.chunk(document)


for i, chunk in enumerate(chunks, 1):
    print(f"\n--- Chunk {i} ---")
    print(repr(chunk.content))
    print(f"Length: {len(chunk.content)}")
    print(f"Metadata: {chunk.metadata}")