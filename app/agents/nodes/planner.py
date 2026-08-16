from app.agents.state import AgentState
from app.gateway import get_langchain_llm
from langsmith import traceable

# Portkey-backed LLM
llm = get_langchain_llm(feature="planner")

@traceable(name="Planner Node")
def planner_node(state: AgentState):
    """
    The Planner determines whether retrieval from the
    knowledge base is needed based on the conversation.
    """

    # Get conversation history excluding the latest message
    history = ""

    for msg in state["messages"][:-1]:
        role = "User" if msg["role"] == "user" else "Assistant"
        history += f"{role}: {msg['content']}\n"

    user_message = (
        state["messages"][-1]["content"]
        if state["messages"]
        else ""
    )

    prompt = f"""
    You are an intelligent RAG Assistant Planner.

    Analyze the conversation history and the latest user message.

    CONVERSATION HISTORY:
    {history}

    LATEST MESSAGE:
    "{user_message}"

    Your task:

    1. If the latest message is a greeting, casual conversation,
       or can be answered using only the conversation history,
       output exactly:

    CONVERSATIONAL

    2. If the latest message requires information from the
       knowledge base / uploaded documents, generate a concise
       search query that can be used to retrieve relevant
       information from the knowledge base.

    Output ONLY one of the following:

    CONVERSATIONAL

    OR

    A concise search query.
    """

    decision = llm.invoke(prompt).content.strip()

    if decision.upper() == "CONVERSATIONAL":
        return {
            "current_query": "CONVERSATIONAL",
            "status": "Handling conversationally.",
            "plan": [
                "Intent: Conversational",
                "Retrieval: Skipped"
            ]
        }

    return {
        "current_query": decision,
        "status": f"Knowledge retrieval needed. Searching for: {decision}",
        "plan": [
            "Intent: Knowledge Retrieval",
            f"Search Term: {decision}"
        ]
    }