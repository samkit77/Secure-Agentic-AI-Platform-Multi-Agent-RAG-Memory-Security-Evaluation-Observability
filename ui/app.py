import os
import streamlit as st
import requests
import time
import uuid
from dotenv import load_dotenv


# ===========================================================
# Load Environment Variables
# ===========================================================

env_path = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".env"
    )
)

load_dotenv(dotenv_path=env_path)


# ============================================================
# Page Configuration
# ============================================================

st.set_page_config(
    page_title="Agentic RAG",
    page_icon="🤖",
    layout="wide",
)


# ============================================================
# Avatars
# ============================================================

AI_AVATAR = "🤖"
USER_AVATAR = "👤"


# ============================================================
# Session Management
# ============================================================

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())


if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.title("🧠 Agentic RAG")

    st.markdown("---")

    st.info(
        f"Memory ID: "
        f"{st.session_state.session_id[:8]}"
    )

    if st.button(
        "🗑️ Clear History & Memory",
        width="stretch",
        type="primary"
    ):

        st.session_state.messages = []

        st.session_state.session_id = str(
            uuid.uuid4()
        )

        st.rerun()


# ============================================================
# Main Chat
# ============================================================

st.title("🤖 Agentic RAG Assistant")

st.caption(
    "Ask questions about the uploaded knowledge base."
)


# ============================================================
# Display Conversation History
# ============================================================

for message in st.session_state.messages:

    avatar = (
        AI_AVATAR
        if message["role"] == "assistant"
        else USER_AVATAR
    )

    with st.chat_message(
        message["role"],
        avatar=avatar
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# Chat Input
# ============================================================

if prompt := st.chat_input(
    "Ask about your documentation..."
):

    # Store user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Display user message
    with st.chat_message(
        "user",
        avatar=USER_AVATAR
    ):

        st.markdown(prompt)


    # ========================================================
    # Assistant Response
    # ========================================================

    with st.chat_message(
        "assistant",
        avatar=AI_AVATAR
    ):

        with st.status(
            "🔍 Agent is thinking...",
            expanded=True
        ) as status:

            try:

                # ------------------------------------------------
                # Backend URL
                # ------------------------------------------------

                base_url = os.getenv(
                    "BACKEND_URL",
                    "http://localhost:8000"
                )

                url = f"{base_url}/query"


                # ------------------------------------------------
                # Request
                # ------------------------------------------------

                payload = {
                    "q": prompt,
                    "thread_id": (
                        st.session_state.session_id
                    )
                }


                response = requests.post(
                    url,
                    json=payload,
                    timeout=60
                )


                response.raise_for_status()

                data = response.json()


                # ------------------------------------------------
                # Show Agent Plan
                # ------------------------------------------------

                steps = data.get(
                    "thought_process",
                    []
                )

                for step in steps:

                    st.write(
                        f"⚙️ {step}"
                    )


                status.update(
                    label="✅ Answer Synthesized",
                    state="complete",
                    expanded=False
                )


                # ------------------------------------------------
                # Show Retrieved Sources
                # ------------------------------------------------

                sources = data.get(
                    "sources",
                    []
                )

                if sources:

                    with st.expander(
                        "📄 View Retrieved Context"
                    ):

                        for i, source in enumerate(
                            sources
                        ):

                            preview = (
                                source[:100]
                                .replace("\n", " ")
                                + "..."
                            )

                            with st.expander(
                                f"Chunk {i + 1}: {preview}"
                            ):

                                st.info(source)


            except Exception as e:

                status.update(
                    label="❌ Connection Failed",
                    state="error"
                )

                st.error(
                    f"Backend Offline or unavailable: {e}"
                )

                st.stop()


        # ========================================================
        # Display Answer
        # ========================================================

        answer_placeholder = st.empty()

        full_answer = data.get(
            "answer",
            "No response."
        )


        # Simple visual streaming effect
        curr_text = ""

        for char in full_answer:

            curr_text += char

            answer_placeholder.markdown(
                curr_text + "▌"
            )

            time.sleep(0.005)


        answer_placeholder.markdown(
            full_answer
        )


        # Store assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": full_answer
            }
        )