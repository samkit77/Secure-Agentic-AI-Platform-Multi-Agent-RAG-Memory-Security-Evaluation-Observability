from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from app.agents.state import AgentState
from app.agents.nodes.planner import planner_node
from app.agents.nodes.retriever import retrieve_node
from app.agents.nodes.responder import generate_node
from app.agents.nodes.relevance_checker import relevance_checker_node
from app.agents.nodes.query_rewriter import query_rewriter_node
from app.agents.nodes.web_search import web_search_node

# ---------------------------------------------------------
# Initialize State Graph
# ---------------------------------------------------------
MAX_QUERY_REWRITES = 2

workflow = StateGraph(AgentState)


# ---------------------------------------------------------
# Define Nodes
# ---------------------------------------------------------

workflow.add_node(
    "planner",
    planner_node
)

workflow.add_node(
    "retriever",
    retrieve_node
)

workflow.add_node(
    "relevance_checker",
    relevance_checker_node
)

workflow.add_node(
    "query_rewriter",
    query_rewriter_node
)

workflow.add_node(
    "web_search",
    web_search_node
)

workflow.add_node(
    "responder",
    generate_node
)


# ---------------------------------------------------------
# Routing Logic
# ---------------------------------------------------------
def route_planner(state: AgentState):

    if state["current_query"] == "CONVERSATIONAL":
        return "responder"

    return "retriever"


# ============================================================
# Relevance Routing
# ============================================================

def route_relevance(state: AgentState):
    """
    Qdrant is always attempted first.

    If Qdrant context is relevant:
        → responder

    If not relevant and rewrites remain:
        → query rewriter

    If not relevant and rewrite limit is exhausted:
        → web search
    """

    if state.get(
        "retrieval_relevant",
        False
    ):
        return "responder"

    rewrite_count = state.get(
        "rewrite_count",
        0
    )

    if rewrite_count < MAX_QUERY_REWRITES:
        return "query_rewriter"

    return "web_search"


# ============================================================
# Entry Point
# ============================================================

workflow.set_entry_point(
    "planner"
)


# ============================================================
# Planner Routing
# ============================================================

workflow.add_conditional_edges(
    "planner",
    route_planner,
    {
        "retriever": "retriever",
        "responder": "responder",
    },
)


# ============================================================
# Qdrant → Relevance Check
# ============================================================

workflow.add_edge(
    "retriever",
    "relevance_checker"
)


# ============================================================
# Relevance → Rewrite / Web / Responder
# ============================================================

workflow.add_conditional_edges(
    "relevance_checker",
    route_relevance,
    {
        "query_rewriter": "query_rewriter",
        "web_search": "web_search",
        "responder": "responder",
    },
)


# ============================================================
# Rewrite → Qdrant
# ============================================================

workflow.add_edge(
    "query_rewriter",
    "retriever"
)


# ============================================================
# Web Search → Responder
# ============================================================

workflow.add_edge(
    "web_search",
    "responder"
)


# ============================================================
# Responder → END
# ============================================================

workflow.add_edge(
    "responder",
    END
)


# ============================================================
# Memory
# ============================================================

checkpointer = MemorySaver()


# ============================================================
# Compile
# ============================================================

rag_agent = workflow.compile(
    checkpointer=checkpointer
)