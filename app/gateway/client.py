from portkey_ai import (
    Portkey,
    createHeaders,
    PORTKEY_GATEWAY_URL,
)

from langchain_openai import ChatOpenAI

from app.config import settings


# ============================================================
# Portkey Saved Configuration
# ============================================================

PORTKEY_CONFIG = settings.PORTKEY_CONFIG
OPENAI_INTEGRATION = settings.OPENAI_INTEGRATION


# ============================================================
# Native Portkey Client
# ============================================================

portkey_client = Portkey(
    api_key=settings.PORTKEY_API_KEY,
)


# ============================================================
# LangChain LLM
# ============================================================

def get_langchain_llm(
    feature: str = "rag"
) -> ChatOpenAI:
    """
    Returns a LangChain ChatOpenAI instance
    routed through Portkey.

    Portkey handles:
    - Gateway
    - Retry

    OpenAI is the actual LLM provider.
    """

    return ChatOpenAI(
        api_key=settings.PORTKEY_API_KEY,
        base_url=PORTKEY_GATEWAY_URL,

        # Saved Portkey OpenAI integration
        model=f"{OPENAI_INTEGRATION}/{settings.OPENAI_MODEL}",

        temperature=0,

        default_headers=createHeaders(
            api_key=settings.PORTKEY_API_KEY,
            config=PORTKEY_CONFIG,
            metadata={
                "feature": feature,
                "_user": "rag-system",
                "environment": "development",
            },
        ),
    )


