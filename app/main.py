from dotenv import load_dotenv
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import Optional

from app.agents.graph import rag_agent
from app.guardrails.guardrails import (
    initialize_rails,
    guard,
    validate_output,
)


# ============================================================
# Environment
# ============================================================

load_dotenv()


# ============================================================
# FastAPI
# ============================================================

app = FastAPI(
    title="Agentic RAG "
)


# ============================================================
# Guardrails Initialization
# ============================================================

@app.on_event("startup")
def startup_event():
    initialize_rails()


# ============================================================
# Request Schema
# ============================================================

class QueryRequest(BaseModel):
    q: str
    thread_id: Optional[str] = "default_user"


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():
    return {
        "message": "Agentic RAG API is live."
    }


# ============================================================
# Graph Visualization
# ============================================================

@app.get("/graph")
def get_graph_image():
    """
    Returns a PNG image of the LangGraph workflow.
    """

    try:
        png_bytes = (
            rag_agent
            .get_graph()
            .draw_mermaid_png()
        )

        return Response(
            content=png_bytes,
            media_type="image/png"
        )

    except Exception as e:

        return {
            "error": (
                f"Could not generate graph image: {e}"
            )
        }


# ============================================================
# RAG Query
# ============================================================

@app.post("/query")
def query(request: QueryRequest):
    """
    Executes the LangGraph RAG workflow with
    input and output Guardrails AI validation.
    """

    q = request.q
    thread_id = request.thread_id

    # ========================================================
    # Gate 1: Input Guardrail
    # ========================================================

    rail_fired, rail_response = guard(q)

    if rail_fired:
        return {
            "question": q,
            "answer": rail_response,
            "thought_process": [
                "Input Guardrail: Blocked",
                "Retrieval: Skipped",
            ],
            "status": "Blocked by input guardrails.",
            "sources": [],
        }

    # ========================================================
    # Initial LangGraph State
    # ========================================================

    initial_state = {
        "messages": [
            {
                "role": "user",
                "content": q
            }
        ],
        "current_query": q,
        "documents": [],
        "plan": ["Start"],
        "status": "Initializing Graph...",

        "retrieval_attempts": 0,
        "rewrite_count": 0,
        "retrieval_relevant": False,
    }

    # ========================================================
    # LangGraph Memory Configuration
    # ========================================================

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:

        # ====================================================
        # Run Agentic RAG
        # ====================================================

        final_output = rag_agent.invoke(
            initial_state,
            config=config
        )

        answer = final_output.get(
            "final_answer",
            ""
        )

        # ====================================================
        # Gate 2: Output Guardrail
        # ====================================================

        output_safe, validated_answer = validate_output(
            answer
        )

        if not output_safe:
            return {
                "question": q,
                "answer": (
                    "I’m unable to provide that response "
                    "because it did not pass the output "
                    "safety checks."
                ),
                "thought_process": (
                    final_output.get("plan", [])
                    + ["Output Guardrail: Blocked"]
                ),
                "status": "Blocked by output guardrails.",
                "sources": [],
            }

        # ====================================================
        # Successful Response
        # ====================================================

        return {
            "question": q,
            "answer": validated_answer,
            "thought_process": final_output.get(
                "plan"
            ),
            "status": final_output.get(
                "status"
            ),
            "sources": final_output.get(
                "documents",
                []
            ),
        }

    except Exception as e:

        print(
            f"❌ Backend Execution Failed: {e}"
        )

        return {
            "question": q,
            "answer": (
                "I apologize, but I encountered "
                "an internal error while processing "
                "your request."
            ),
            "thought_process": [
                "Error encountered during execution."
            ],
            "status": "error",
            "sources": [],
        }