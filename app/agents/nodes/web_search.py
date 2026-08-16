from app.agents.state import AgentState
from app.config import settings
from langsmith import traceable
from tavily import TavilyClient


client = TavilyClient(
    api_key=settings.TAVILY_API_KEY
)


@traceable(name="Web Search Fallback")
def web_search_node(state: AgentState):
    """
    Performs web search only after the maximum number
    of unsuccessful Qdrant retrieval attempts.
    """

    query = state["current_query"]

    try:

        response = client.search(
            query=query,
            search_depth="advanced",
            max_results=5,
            include_answer=False,
        )

        results = response.get(
            "results",
            []
        )

        web_documents = []

        for result in results:

            title = result.get(
                "title",
                "Untitled"
            )

            url = result.get(
                "url",
                ""
            )

            content = result.get(
                "content",
                ""
            ).strip()

            if not content:
                continue

            web_documents.append(
                (
                    f"[WEB SOURCE]\n"
                    f"TITLE: {title}\n"
                    f"URL: {url}\n"
                    f"CONTENT:\n{content}"
                )
            )

        return {
            "documents": web_documents,
            "status": (
                f"Web search fallback returned "
                f"{len(web_documents)} results."
            ),
            "plan": state["plan"] + [
                "Qdrant Retrieval Exhausted",
                "Web Search Fallback Used",
                f"Web Results: {len(web_documents)}",
            ],
        }

    except Exception as e:

        print(
            f"❌ Web search failed: {e}"
        )

        return {
            "documents": [],
            "status": "Web search fallback failed.",
            "plan": state["plan"] + [
                "Web Search: Failed"
            ],
        }