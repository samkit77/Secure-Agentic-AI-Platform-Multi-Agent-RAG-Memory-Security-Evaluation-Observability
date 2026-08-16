from app.agents.state import AgentState
from app.gateway import get_langchain_llm
from langsmith import traceable


llm = get_langchain_llm(
    feature="query_rewriter"
)


@traceable(name="Query Rewriter Node")
def query_rewriter_node(state: AgentState):
    """
    Rewrites the current retrieval query when the
    retrieved context is not relevant.
    """

    current_query = state["current_query"]

    history = ""

    for msg in state["messages"][:-1]:
        role = (
            "User"
            if msg["role"] == "user"
            else "Assistant"
        )

        history += (
            f"{role}: {msg['content']}\n"
        )

    prompt = f"""
You are a search-query rewriting component in a RAG system.

The previous retrieval query did not retrieve sufficiently
relevant information.

Rewrite the query so that vector search has a better chance
of finding the correct information in the knowledge base.

CURRENT RETRIEVAL QUERY:
{current_query}

CONVERSATION HISTORY:
{history}

Rules:

- Preserve the user's actual intent.
- Remove unnecessary conversational wording.
- Make the query specific and information-rich.
- Do not answer the question.
- Return ONLY the rewritten search query.
"""

    try:

        rewritten_query = (
            llm.invoke(prompt)
            .content
            .strip()
        )

        if not rewritten_query:
            return {
                "current_query": current_query,
                "rewrite_count": state.get(
                    "rewrite_count",
                    0
                ),
                "status": "Query rewrite produced no change.",
                "plan": state["plan"] + [
                    "Query Rewrite: No change"
                ],
            }

        rewrite_count = (
            state.get("rewrite_count", 0) + 1
        )

        return {
            "current_query": rewritten_query,
            "rewrite_count": rewrite_count,
            "status": (
                f"Query rewritten for retrieval: "
                f"{rewritten_query}"
            ),
            "plan": state["plan"] + [
                f"Query Rewrite #{rewrite_count}",
                f"New Search Query: {rewritten_query}",
            ],
        }

    except Exception as e:

        print(
            f"❌ Query rewrite failed: {e}"
        )

        return {
            "current_query": current_query,
            "rewrite_count": state.get(
                "rewrite_count",
                0
            ),
            "status": "Query rewrite failed.",
            "plan": state["plan"] + [
                "Query Rewrite: Failed"
            ],
        }