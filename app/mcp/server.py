from mcp.server.fastmcp import FastMCP
from langchain_community.tools import DuckDuckGoSearchRun


mcp = FastMCP("Secure Agentic RAG")

duckduckgo = DuckDuckGoSearchRun()


@mcp.tool()
async def web_search(query: str) -> str:
    """Search the web using DuckDuckGo."""
    try:
        query = f"{query}"

        return duckduckgo.invoke(query)

    except Exception as e:
        return f"Error during web search: {str(e)}"


if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
    )