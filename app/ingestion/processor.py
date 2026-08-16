import os
import sys
import uuid

from qdrant_client import QdrantClient
from qdrant_client.http import models

# Import local modules
from app.config import settings
from app.services.retrieval.embedding import embed_texts
from app.ingestion.loaders.pdf import parse_pdf
from app.ingestion.chunking.splitter import chunk_text


# Initialize Qdrant Client
qdrant_client = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY
)


def process_file(
    file_path: str,
    filename: str,
    source_type: str = "pdf"
):
    """
    Processes a single PDF file.

    Pipeline:
    PDF → Text → Chunks → Embeddings → Qdrant
    """

    try:
        # 1. Extract text from PDF
        full_text = parse_pdf(file_path)

        if not full_text or not full_text.strip():
            print(f"⚠️ No text extracted from {filename}")
            return

        # 2. Chunk text
        chunks = chunk_text(full_text)

        if not chunks:
            print(f"⚠️ No chunks generated for {filename}")
            return

        print(
            f"📄 {filename}: "
            f"generated {len(chunks)} chunks"
        )

        # 3. Generate embeddings
        embeddings = embed_texts(chunks)

        # 4. Create Qdrant points
        points = []

        for i, (chunk, vector) in enumerate(
            zip(chunks, embeddings)
        ):
            points.append(
                models.PointStruct(
                    id=str(uuid.uuid4()),
                    vector=vector,
                    payload={
                        "text": chunk,
                        "source": filename,
                        "source_type": source_type,
                        "chunk_index": i,
                    }
                )
            )

        # 5. Store vectors in Qdrant
        qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION,
            points=points
        )

        print(
            f"✅ Indexed {len(points)} chunks "
            f"from {filename}"
        )

    except Exception as e:
        print(
            f"❌ Failed to process "
            f"{filename}: {e}"
        )
        raise


def run_universal_ingestion(
    base_dir: str,
    explicit_source_type: str = "pdf",
    wipe: bool = False
):
    """
    Processes PDF files from a directory
    and stores their embeddings in Qdrant.
    """

    # Handle collection wipe
    if wipe:
        if qdrant_client.collection_exists(
            settings.QDRANT_COLLECTION
        ):
            qdrant_client.delete_collection(
                settings.QDRANT_COLLECTION
            )

            print(
                f"🗑️ Collection "
                f"{settings.QDRANT_COLLECTION} deleted"
            )

    # Ensure collection exists
    if not qdrant_client.collection_exists(
        settings.QDRANT_COLLECTION
    ):
        qdrant_client.create_collection(
            collection_name=settings.QDRANT_COLLECTION,
            vectors_config=models.VectorParams(
                size=1536,
                distance=models.Distance.COSINE
            )
        )

        print(
            f"🆕 Created collection "
            f"{settings.QDRANT_COLLECTION}"
        )

    # Process the PDF directory
    process_directory(
        base_dir,
        explicit_source_type
    )


def process_directory(
    dir_path: str,
    source_type: str = "pdf"
):
    """
    Processes PDF files in a directory.
    """

    files = [
        f
        for f in os.listdir(dir_path)
        if os.path.isfile(
            os.path.join(dir_path, f)
        )
        and f.lower().endswith(".pdf")
    ]

    if not files:
        print(
            f"⚠️ No PDF files found in {dir_path}"
        )
        return

    print(
        f"🔍 Found {len(files)} PDF file(s)"
    )

    for filename in files:

        file_path = os.path.join(
            dir_path,
            filename
        )

        process_file(
            file_path,
            filename,
            source_type
        )


if __name__ == "__main__":

    # Usage:
    # python -m app.ingestion.processor
    # python -m app.ingestion.processor --wipe

    wipe_requested = "--wipe" in sys.argv

    target_dir = "DATA"

    if not os.path.exists(target_dir):
        print(
            f"❌ Path {target_dir} does not exist."
        )
        sys.exit(1)

    run_universal_ingestion(
        target_dir,
        explicit_source_type="pdf",
        wipe=wipe_requested
    )

    print("🏁 Ingestion completed.")