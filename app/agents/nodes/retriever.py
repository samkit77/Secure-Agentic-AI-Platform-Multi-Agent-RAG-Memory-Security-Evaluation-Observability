from app.agents.state import AgentState
from app.services.retrieval.qdrant_service import (
    search_enterprise_knowledge
)
from langsmith import traceable


@traceable(name="Retriever Node")
def retrieve_node(state: AgentState):
    """
    Performs vector search in Qdrant.

    Qdrant is always the first retrieval source.
    Web search is handled separately as a fallback.
    """

    query = state["current_query"]

    raw_results = search_enterprise_knowledge(
        query,
        limit=5
    )

    formatted_docs = [
        f"CONTENT: {doc['content']}"
        for doc in raw_results
        if doc.get("content")
    ]

    retrieval_attempts = (
        state.get("retrieval_attempts", 0) + 1
    )

    return {
        "documents": formatted_docs,
        "retrieval_attempts": retrieval_attempts,
        "retrieval_relevant": False,
        "status": (
            f"Retrieved {len(formatted_docs)} "
            f"chunks from Qdrant."
        ),
        "plan": state["plan"] + [
            f"Qdrant Retrieval Attempt: {retrieval_attempts}",
            f"Retrieved: {len(formatted_docs)} chunks",
        ],
    }