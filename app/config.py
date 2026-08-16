import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:

    # --- OPENAI ---
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL","gpt-4o-mini")

    # --- VECTOR DB (QDRANT) ---
    QDRANT_URL = os.getenv("QDRANT_CLUSTER_ENDPOINT")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
    QDRANT_COLLECTION = "rag_test2"

    # --- LLM GATEWAY (PORTKEY) ---
    PORTKEY_API_KEY = os.getenv("PORTKEY_API_KEY")
    PORTKEY_CONFIG=os.getenv("PORTKEY_CONFIG")
    OPENAI_INTEGRATION=os.getenv("OPENAI_INTEGRATION")
    # # --- OBSERVABILITY (LANGSMITH) ---
    # LANGSMITH_TRACING = os.getenv(
    #     "LANGSMITH_TRACING",
    #     "true"
    # )

    # LANGSMITH_API_KEY = os.getenv(
    #     "LANGSMITH_API_KEY"
    # )

    # LANGSMITH_PROJECT = os.getenv(
    #     "LANGSMITH_PROJECT",
    #     "rag_test"
    # )

    # LANGSMITH_ENDPOINT = os.getenv(
    #     "LANGSMITH_ENDPOINT",
    #     "https://api.smith.langchain.com"
    # )


# # Apply LangChain environment variables
# # for automatic LangSmith tracing
# os.environ["LANGCHAIN_TRACING_V2"] = os.getenv(
#     "LANGSMITH_TRACING",
#     "true"
# )

# os.environ["LANGCHAIN_API_KEY"] = os.getenv(
#     "LANGSMITH_API_KEY",
#     ""
# )

# os.environ["LANGCHAIN_PROJECT"] = os.getenv(
#     "LANGSMITH_PROJECT",
#     "rag_test"
# )

# os.environ["LANGCHAIN_ENDPOINT"] = os.getenv(
#     "LANGSMITH_ENDPOINT",
#     "https://api.smith.langchain.com"
# )


settings = Settings()