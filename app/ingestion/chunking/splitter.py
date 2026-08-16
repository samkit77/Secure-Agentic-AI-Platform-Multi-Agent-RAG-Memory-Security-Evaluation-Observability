from typing import List
from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_text(text: str, chunk_size: int = 1500) -> List[str]:
    """
    Splits text into chunks using recursive character splitting.

    The splitter tries to preserve natural boundaries such as:
    paragraphs -> lines -> sentences -> words -> characters.

    Args:
        text: Input text extracted from the PDF.
        chunk_size: Maximum size of each chunk.

    Returns:
        A list of non-empty text chunks.
    """

    if not text.strip():
        return []

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            "",
        ],
    )

    chunks = text_splitter.split_text(text)

    return [chunk.strip() for chunk in chunks if chunk.strip()]