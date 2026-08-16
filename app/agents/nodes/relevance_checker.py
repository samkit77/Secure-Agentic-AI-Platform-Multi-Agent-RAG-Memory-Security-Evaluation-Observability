from app.agents.state import AgentState
from app.gateway import get_langchain_llm
from langsmith import traceable


llm = get_langchain_llm(
    feature="relevance_checker"
)


@traceable(name="Retrieval Relevance Check")
def relevance_checker_node(state: AgentState):
    """
    Checks whether Qdrant's retrieved context is relevant
    enough to answer the current query.
    """

    query = state["current_query"]
    documents = state.get("documents", [])

    if not documents:
        return {
            "retrieval_relevant": False,
            "status": "No Qdrant context retrieved.",
            "plan": state["plan"] + [
                "Relevance Check: NOT RELEVANT"
            ],
        }

    context = "\n\n".join(documents)

    prompt = f"""
You are a retrieval relevance evaluator for a RAG system.

Determine whether the retrieved Qdrant context contains
useful information for answering the user's query.

USER QUERY:
{query}

RETRIEVED CONTEXT:
{context}

Rules:

- RELEVANT means the context contains useful information
  that can answer or materially support the query.
- NOT_RELEVANT means the context is unrelated or
  insufficient.

Return ONLY:

RELEVANT

or

NOT_RELEVANT
"""

    try:

        decision = (
            llm.invoke(prompt)
            .content
            .strip()
            .upper()
        )

        is_relevant = (
            decision == "RELEVANT"
        )

        return {
            "retrieval_relevant": is_relevant,
            "status": (
                "Qdrant context is relevant."
                if is_relevant
                else "Qdrant context is not relevant."
            ),
            "plan": state["plan"] + [
                (
                    "Relevance Check: RELEVANT"
                    if is_relevant
                    else "Relevance Check: NOT RELEVANT"
                )
            ],
        }

    except Exception as e:

        print(
            f"❌ Relevance check failed: {e}"
        )

        # Do not create a retry loop because the
        # evaluator itself failed.
        return {
            "retrieval_relevant": True,
            "status": "Relevance check unavailable.",
            "plan": state["plan"] + [
                "Relevance Check: Skipped"
            ],
        }