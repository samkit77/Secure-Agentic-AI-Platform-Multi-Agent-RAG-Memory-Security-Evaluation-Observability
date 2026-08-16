from typing import TypedDict, List, Annotated
import operator


class AgentState(TypedDict):

    # Messages are appended to conversation history
    messages: Annotated[
        List[dict],
        operator.add
    ]

    current_query: str
    documents: List[str]
    plan: List[str]
    status: str
    final_answer: str

    # Retrieval refinement
    retrieval_attempts: int
    rewrite_count: int
    retrieval_relevant: bool