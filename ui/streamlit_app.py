import sys
from pathlib import Path

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(
        0,
        str(PROJECT_ROOT),
    )


# ============================================================
# PROJECT IMPORTS
# ============================================================

from app.dependencies import (
    create_knowledge_base,
)

from chat.chatbot import ChatBot

from chat.conversation_store import (
    ConversationStore,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="LEARNBOT — AI Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DIRECTORIES
# ============================================================

DATA_DIRECTORY = (
    PROJECT_ROOT / "data"
)

UPLOAD_DIRECTORY = (
    DATA_DIRECTORY / "uploads"
)

UPLOAD_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONSTANTS
# ============================================================

SUPPORTED_FILE_TYPES = [
    "txt",
    "pdf",
    "docx",
    "md",
    "markdown",
]

FILE_ICONS = {
    "pdf": "📕",
    "docx": "📘",
    "txt": "📄",
    "md": "📝",
    "markdown": "📝",
}

MAX_SIDEBAR_TITLE = 28


# ============================================================
# APPLICATION INITIALIZATION
# ============================================================

@st.cache_resource
def initialize_application():

    knowledge, rag_pipeline, llm = (
        create_knowledge_base()
    )

    return (
        knowledge,
        rag_pipeline,
        llm,
    )


knowledge, rag_pipeline, llm = (
    initialize_application()
)


# ============================================================
# CONVERSATION STORE
# ============================================================

@st.cache_resource
def initialize_conversation_store():

    return ConversationStore()


conversation_store = (
    initialize_conversation_store()
)


# ============================================================
# SESSION STATE
# ============================================================

if "page" not in st.session_state:

    st.session_state.page = "home"


if "current_chat_id" not in st.session_state:

    st.session_state.current_chat_id = None


if "chatbot" not in st.session_state:

    st.session_state.chatbot = ChatBot(
        conversation_history=[],
        llm=llm,
        rag_pipeline=rag_pipeline,
    )


chatbot = st.session_state.chatbot


# ============================================================
# CHAT HELPERS
# ============================================================

def create_chat_title(question):
    """
    Convert the first question into a short
    conversation title.
    """

    title = " ".join(
        question.strip().split()
    )

    if not title:
        return "New conversation"


    max_length = 48

    if len(title) > max_length:

        return (
            title[:max_length]
            .rstrip()
            + "..."
        )

    return title


def short_title(
    title,
    max_length=MAX_SIDEBAR_TITLE,
):
    """
    Short title for sidebar display.
    """

    title = " ".join(
        str(title).split()
    )

    if len(title) <= max_length:
        return title

    return (
        title[:max_length]
        .rstrip()
        + "..."
    )


def get_chats():
    """
    Get conversations from ConversationStore.
    """

    return conversation_store.get_chats()


def get_current_chat():
    """
    Return the active conversation.
    """

    chat_id = (
        st.session_state.current_chat_id
    )

    if not chat_id:
        return None

    return conversation_store.get_chat(
        chat_id
    )


def sync_chatbot_history(chat):
    """
    Restore conversation history into ChatBot.
    """

    chatbot.clear_history()

    if chat is None:
        return


    chatbot.conversation_history = [
        {
            "role": message.get(
                "role",
                "",
            ),
            "content": message.get(
                "content",
                "",
            ),
        }

        for message in chat.get(
            "messages",
            [],
        )

        if message.get("role")
        and message.get("content")
    ]


def start_new_chat():
    """
    ALWAYS create a completely new conversation.

    Important:
    - Removes unused empty conversations.
    - Creates a new unique chat.
    - Makes it the current chat.
    - Clears chatbot memory.
    - Opens the Chat page.
    """

    # Remove abandoned empty chats.
    conversation_store.cleanup_empty_chats()


    # ALWAYS create a new chat.
    new_chat = (
        conversation_store.create_chat()
    )


    # Make the new chat active.
    st.session_state.current_chat_id = (
        new_chat["id"]
    )


    # Clear previous LLM conversation memory.
    chatbot.clear_history()


    # Open actual chatbot page.
    st.session_state.page = "chat"


def open_chat(chat_id):
    """
    Open an existing conversation.
    """

    chat = conversation_store.get_chat(
        chat_id
    )

    if chat is None:
        return False


    st.session_state.current_chat_id = (
        chat_id
    )

    sync_chatbot_history(chat)

    st.session_state.page = "chat"

    return True


def ensure_chat_for_chat_page():
    """
    Make sure Chat page always has a valid
    active conversation.

    It does NOT automatically switch to
    an unrelated old conversation.
    """

    chat = get_current_chat()

    if chat is not None:
        return chat


    # No active conversation exists.
    # Create a fresh one.
    start_new_chat()

    return get_current_chat()


def delete_chat(chat_id):
    """
    Delete a conversation.

    Deletion is handled by ConversationStore.
    """

    deleted = (
        conversation_store.delete_chat(
            chat_id
        )
    )


    if not deleted:
        return False


    # If the deleted conversation was active,
    # clear the active conversation.
    if (
        st.session_state.current_chat_id
        == chat_id
    ):

        st.session_state.current_chat_id = None

        chatbot.clear_history()


    return True


# ============================================================
# DOCUMENT HELPERS
# ============================================================

def get_documents():

    if not UPLOAD_DIRECTORY.exists():
        return []

    return sorted(
        [
            file
            for file in UPLOAD_DIRECTORY.iterdir()
            if file.is_file()
        ],
        key=lambda file: file.name.lower(),
    )


def get_file_icon(file_path):

    extension = (
        file_path.suffix
        .lower()
        .replace(
            ".",
            "",
        )
    )

    return FILE_ICONS.get(
        extension,
        "📄",
    )


# ============================================================
# CUSTOM UI STYLE
# ============================================================

st.markdown(
    """
    <style>

    /* =====================================================
       APPLICATION
       ===================================================== */

    .stApp {
        background-color: #0f1117;
    }


    .main .block-container {
        max-width: 1200px;
        padding-top: 2.5rem;
        padding-bottom: 5rem;
    }


    /* =====================================================
       SIDEBAR
       ===================================================== */

    section[data-testid="stSidebar"] {
        background-color: #151821;
        border-right: 1px solid #292d39;
    }


    .sidebar-brand {
        font-size: 1.35rem;
        font-weight: 800;
        color: #f1f3f7;
    }


    .sidebar-subtitle {
        font-size: 1rem;
        color: #9ba1b2;
        margin-top: 0.25rem;
    }


    /* =====================================================
       SIDEBAR BUTTONS
       ===================================================== */

    section[data-testid="stSidebar"]
    .stButton > button {

        min-height: 46px;

        border-radius: 10px;

        border: 1px solid #303543;

        background-color: #1a1e28;

        color: #e8eaf0;

        font-size: 1rem;

        font-weight: 500;

        transition:
            transform 0.15s ease,
            border-color 0.15s ease,
            background-color 0.15s ease,
            box-shadow 0.15s ease;
    }


    /* Hover = subtle lift */

    section[data-testid="stSidebar"]
    .stButton > button:hover {

        transform: translateY(-2px);

        border-color: #6c63ff;

        background-color: #202432;

        box-shadow:
            0 5px 12px
            rgba(0, 0, 0, 0.25);
    }


    /* Active button */

    section[data-testid="stSidebar"]
    .stButton > button[kind="primary"] {

        background-color: #6c63ff;

        border-color: #6c63ff;

        color: white;

        box-shadow:
            0 4px 12px
            rgba(108, 99, 255, 0.25);
    }


    /* =====================================================
       GENERAL BUTTONS
       ===================================================== */

    .stButton > button {

        border-radius: 10px;

        font-size: 1rem;

        transition:
            transform 0.15s ease,
            border-color 0.15s ease,
            box-shadow 0.15s ease;
    }


    .stButton > button:hover {

        transform: translateY(-2px);

        box-shadow:
            0 5px 12px
            rgba(0, 0, 0, 0.25);
    }


    /* =====================================================
       TEXT
       ===================================================== */

    .hero-title {

        font-size: 3.5rem;

        font-weight: 800;

        letter-spacing: -0.05em;

        line-height: 1.05;
    }


    .hero-subtitle {

        color: #9ba1b2;

        font-size: 1.15rem;

        line-height: 1.7;

        max-width: 760px;
    }


    .section-title {

        font-size: 1.65rem;

        font-weight: 700;

        margin-top: 2rem;
    }


    .page-title {

        font-size: 2.7rem;

        font-weight: 800;

        letter-spacing: -0.03em;
    }


    .muted {

        color: #8c92a3;

        font-size: 0.95rem;
    }


    /* =====================================================
       CHAT
       ===================================================== */

    [data-testid="stChatMessage"] {

        border-radius: 14px;

        font-size: 1.05rem;

        line-height: 1.7;
    }


    [data-testid="stChatInput"] {

        border-radius: 16px;
    }


    [data-testid="stChatInput"] textarea {

        font-size: 1rem;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {

        border-radius: 14px;
    }


    /* =====================================================
       METRICS
       ===================================================== */

    [data-testid="stMetricValue"] {

        font-size: 1.7rem;
    }


    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

documents = get_documents()
chats = get_chats()

with st.sidebar:

    # --------------------------------------------------------
    # BRAND
    # --------------------------------------------------------

    st.markdown(
        '<div class="sidebar-brand">'
        "🧠 LearnBot"
        "</div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        "AI Knowledge Assistant"
        "</div>",
        unsafe_allow_html=True,
    )

    st.divider()


    # --------------------------------------------------------
    # HOME
    # --------------------------------------------------------

    if st.button(
        "🏠  Home",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page
            == "home"
            else "secondary"
        ),
    ):

        st.session_state.page = "home"

        st.rerun()


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "✨  New Chat",
        use_container_width=True,
    ):

        start_new_chat()

        st.rerun()


    st.divider()


    # --------------------------------------------------------
    # WORKSPACE
    # --------------------------------------------------------

    st.caption(
        "WORKSPACE"
    )


    # --------------------------------------------------------
    # CHAT
    # --------------------------------------------------------

    if st.button(
        "💬  Chat",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page
            == "chat"
            else "secondary"
        ),
    ):

        chat = get_current_chat()

        if chat is None:

            start_new_chat()

        else:

            sync_chatbot_history(
                chat
            )

            st.session_state.page = (
                "chat"
            )

        st.rerun()


    # --------------------------------------------------------
    # CHATS
    # --------------------------------------------------------

    if st.button(
        "🗂️  Chats",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page
            == "chats"
            else "secondary"
        ),
    ):

        st.session_state.page = "chats"

        st.rerun()


    # --------------------------------------------------------
    # DOCUMENTS
    # --------------------------------------------------------

    if st.button(
        "📚  Documents",
        use_container_width=True,
        type=(
            "primary"
            if st.session_state.page
            == "documents"
            else "secondary"
        ),
    ):

        st.session_state.page = (
            "documents"
        )

        st.rerun()


    # --------------------------------------------------------
    # RECENT CHATS
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "RECENT CHATS"
    )


    if chats:

        for chat in chats[:6]:

            title = short_title(
                chat.get(
                    "title",
                    "New conversation",
                )
            )


            # Recent chat buttons remain neutral.
            # This prevents the sidebar from having
            # multiple highlighted buttons at once.

            if st.button(
                f"💬  {title}",
                key=f"recent_{chat['id']}",
                use_container_width=True,
            ):

                if open_chat(
                    chat["id"]
                ):

                    st.rerun()

    else:

        st.caption(
            "No conversations yet."
        )


    # --------------------------------------------------------
    # WORKSPACE INFO
    # --------------------------------------------------------

    st.divider()

    st.caption(
        "WORKSPACE INFO"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Documents",
            len(documents),
        )

    with col2:

        st.metric(
            "Chats",
            len(chats),
        )


# ============================================================
# HOME PAGE
# ============================================================

if st.session_state.page == "home":

    st.markdown(
        '<div class="hero-title">'
        "Your workspace.<br>"
        '<span style="color:#07ed82;">'
        "Your knowledge & Docs.<br>"
        "</span>"
        "Your AI assistant."
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        '<div class="hero-subtitle">'
        "LearnBot transforms your documents into a "
        "searchable knowledge base and lets you interact "
        "with them using Retrieval-Augmented Generation."
        "</div>",
        unsafe_allow_html=True,
    )

    st.write("")
    st.write("")


    # --------------------------------------------------------
    # QUICK ACTIONS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    with col1:

        if st.button(
            "💬  Start Chatting",
            type="primary",
            use_container_width=True,
        ):

            chat = get_current_chat()

            if chat is None:
                start_new_chat()
            else:
                sync_chatbot_history(
                    chat
                )
                st.session_state.page = (
                    "chat"
                )

            st.rerun()


    with col2:

        if st.button(
            "📚  Open Documents",
            use_container_width=True,
        ):

            st.session_state.page = (
                "documents"
            )

            st.rerun()


    with col3:

        if st.button(
            "✨  New Conversation",
            use_container_width=True,
        ):

            start_new_chat()

            st.rerun()


    # --------------------------------------------------------
    # WHY LEARNBOT
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        "Why use LearnBot?"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "A simple interface for working with your own knowledge."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(
            border=True
        ):

            st.subheader(
                "📄 Your Knowledge"
            )

            st.write(
                "Upload your own PDFs, DOCX files, "
                "text files, and Markdown documents."
            )

            st.caption(
                "Build a knowledge base from the "
                "material you actually care about."
            )


    with col2:

        with st.container(
            border=True
        ):

            st.subheader(
                "🔎 Smart Retrieval"
            )

            st.write(
                "Your question is converted into an "
                "embedding and compared with stored "
                "document embeddings."
            )

            st.caption(
                "Relevant document chunks are retrieved "
                "before the answer is generated."
            )


    with col3:

        with st.container(
            border=True
        ):

            st.subheader(
                "🤖 Grounded Answers"
            )

            st.write(
                "The retrieved context is provided to "
                "the language model to generate an answer."
            )

            st.caption(
                "Relevant sources can be included "
                "with the response."
            )


    # --------------------------------------------------------
    # HOW RAG WORKS
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        "How your RAG assistant works"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Three stages turn your documents into useful answers."
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(
            border=True
        ):

            st.caption(
                "STEP 01"
            )

            st.subheader(
                "📚 Upload"
            )

            st.write(
                "Add documents to your knowledge base. "
                "The ingestion pipeline processes and "
                "chunks the content."
            )


    with col2:

        with st.container(
            border=True
        ):

            st.caption(
                "STEP 02"
            )

            st.subheader(
                "🔎 Retrieve"
            )

            st.write(
                "Your question is embedded and compared "
                "with stored vectors to find relevant "
                "document context."
            )


    with col3:

        with st.container(
            border=True
        ):

            st.caption(
                "STEP 03"
            )

            st.subheader(
                "✨ Generate"
            )

            st.write(
                "The language model receives the retrieved "
                "context and generates the final response."
            )


    # --------------------------------------------------------
    # WORKSPACE OVERVIEW
    # --------------------------------------------------------

    st.markdown(
        '<div class="section-title">'
        "Your workspace"
        "</div>",
        unsafe_allow_html=True,
    )


    col1, col2, col3 = st.columns(3)


    with col1:

        with st.container(
            border=True
        ):

            st.metric(
                "Documents",
                len(documents),
            )

            st.caption(
                "Files currently available "
                "to the knowledge base."
            )


    with col2:

        with st.container(
            border=True
        ):

            st.metric(
                "Conversations",
                len(chats),
            )

            st.caption(
                "Saved conversations in this workspace."
            )


    with col3:

        with st.container(
            border=True
        ):

            st.metric(
                "Formats",
                "4+",
            )

            st.caption(
                "PDF · DOCX · TXT · Markdown"
            )


# ============================================================
# CHAT PAGE
# ============================================================

elif st.session_state.page == "chat":

    # IMPORTANT:
    # This does NOT select the last conversation.
    # It only creates a new one if there is no active chat.

    chat = ensure_chat_for_chat_page()

    if chat is None:

        st.error(
            "Unable to create a conversation."
        )

        st.stop()


    messages = chat.get(
        "messages",
        [],
    )


    # --------------------------------------------------------
    # HEADER
    # --------------------------------------------------------

    st.markdown(
        '<div class="page-title">'
        "💬 Chat"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Ask questions about your knowledge base."
    )


    st.info(
        f"**Conversation:** "
        f"{chat.get('title', 'New conversation')}"
    )


    # --------------------------------------------------------
    # EMPTY CONVERSATION
    # --------------------------------------------------------

    if not messages:

        st.write("")

        with st.container(
            border=True
        ):

            st.subheader(
                "🧠 Ready when you are"
            )

            st.write(
                "Ask a question about your uploaded "
                "documents and LearnBot will retrieve "
                "relevant context before generating an answer."
            )

            st.caption(
                "Example: What are intelligent agents?"
            )


    # --------------------------------------------------------
    # EXISTING MESSAGES
    # --------------------------------------------------------

    for message in messages:

        role = message.get(
            "role",
            "assistant",
        )

        content = message.get(
            "content",
            "",
        )

        if not content:
            continue


        with st.chat_message(
            role
        ):

            st.markdown(
                content
            )


    # --------------------------------------------------------
    # CHAT INPUT
    # --------------------------------------------------------

    user_input = st.chat_input(
        "Ask something about your knowledge base..."
    )


    if user_input:

        user_input = user_input.strip()


        if not user_input:
            st.stop()


        # ----------------------------------------------------
        # FIRST QUESTION → TITLE
        # ----------------------------------------------------

        if not messages:

            chat["title"] = (
                create_chat_title(
                    user_input
                )
            )


        # ----------------------------------------------------
        # USER MESSAGE
        # ----------------------------------------------------

        messages.append(
            {
                "role": "user",
                "content": user_input,
            }
        )


        with st.chat_message(
            "user"
        ):

            st.markdown(
                user_input
            )


        # ----------------------------------------------------
        # AI RESPONSE
        # ----------------------------------------------------

        with st.chat_message(
            "assistant"
        ):

            with st.spinner(
                "Searching your knowledge base..."
            ):

                try:

                    response = (
                        chatbot.ask_knowledge(
                            question=user_input,
                            top_k=3,
                        )
                    )

                except Exception as error:

                    response = (
                        "Sorry, something went wrong "
                        "while processing your question."
                        "\n\n"
                        f"Error: {error}"
                    )


            st.markdown(
                response
            )


        # ----------------------------------------------------
        # ASSISTANT MESSAGE
        # ----------------------------------------------------

        messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )


        # ----------------------------------------------------
        # SAVE CONVERSATION
        # ----------------------------------------------------

        chat["messages"] = messages

        conversation_store.update_chat(
            chat_id=chat["id"],
            title=chat["title"],
            messages=messages,
        )


        # Keep this conversation active.
        st.session_state.current_chat_id = (
            chat["id"]
        )


        st.rerun()


# ============================================================
# CHATS PAGE
# ============================================================

elif st.session_state.page == "chats":

    st.markdown(
        '<div class="page-title">'
        "🗂️ Chats"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "View, open, and delete your saved conversations."
    )


    chats = get_chats()


    # --------------------------------------------------------
    # NEW CHAT
    # --------------------------------------------------------

    if st.button(
        "✨  Start New Chat",
        type="primary",
    ):

        start_new_chat()

        st.rerun()


    st.write("")


    # --------------------------------------------------------
    # EMPTY
    # --------------------------------------------------------

    if not chats:

        with st.container(
            border=True
        ):

            st.subheader(
                "💬 No conversations yet"
            )

            st.write(
                "Start a new conversation to begin chatting."
            )


    # --------------------------------------------------------
    # CHAT LIST
    # --------------------------------------------------------

    else:

        st.subheader(
            f"{len(chats)} conversation(s)"
        )


        for chat in chats:

            chat_id = chat["id"]

            title = chat.get(
                "title",
                "New conversation",
            )

            messages = chat.get(
                "messages",
                [],
            )


            with st.container(
                border=True
            ):

                col1, col2, col3 = (
                    st.columns(
                        [6, 2, 1]
                    )
                )


                with col1:

                    st.markdown(
                        f"### 💬 {title}"
                    )

                    st.caption(
                        f"Updated: "
                        f"{chat.get('updated_at', '')}"
                    )


                with col2:

                    st.write("")

                    if st.button(
                        "Open",
                        key=f"open_{chat_id}",
                        use_container_width=True,
                    ):

                        open_chat(
                            chat_id
                        )

                        st.rerun()


                with col3:

                    st.write("")

                    if st.button(
                        "🗑️",
                        key=f"delete_{chat_id}",
                        use_container_width=True,
                    ):

                        delete_chat(
                            chat_id
                        )

                        st.rerun()


# ============================================================
# DOCUMENTS PAGE
# ============================================================

elif st.session_state.page == "documents":

    st.markdown(
        '<div class="page-title">'
        "📚 Documents"
        "</div>",
        unsafe_allow_html=True,
    )

    st.caption(
        "Manage the documents used by your knowledge base."
    )


    # --------------------------------------------------------
    # UPLOAD
    # --------------------------------------------------------

    with st.container(
        border=True
    ):

        st.subheader(
            "Add a document"
        )

        st.write(
            "Upload a document to add it to your "
            "RAG knowledge base."
        )

        st.caption(
            "Supported formats: "
            "PDF · DOCX · TXT · Markdown"
        )


        uploaded_file = (
            st.file_uploader(
                "Choose a document",
                type=SUPPORTED_FILE_TYPES,
            )
        )


        if uploaded_file is not None:

            st.write(
                f"Selected: **{uploaded_file.name}**"
            )


            if st.button(
                "➕  Add to Knowledge Base",
                type="primary",
                use_container_width=True,
            ):

                destination = (
                    UPLOAD_DIRECTORY
                    / uploaded_file.name
                )


                try:

                    # Save file.
                    with open(
                        destination,
                        "wb",
                    ) as file:

                        file.write(
                            uploaded_file.getbuffer()
                        )


                    # Ingest file.
                    chunks = (
                        knowledge.ingest_file(
                            str(destination)
                        )
                    )


                    st.success(
                        f"{uploaded_file.name} "
                        "was added successfully."
                    )


                    st.info(
                        f"Chunks indexed: {chunks}"
                    )


                    st.rerun()


                except Exception as error:

                    st.error(
                        "Failed to add document:\n\n"
                        f"{error}"
                    )


    # --------------------------------------------------------
    # DOCUMENT LIBRARY
    # --------------------------------------------------------

    st.write("")

    documents = get_documents()


    st.subheader(
        f"Knowledge Base · "
        f"{len(documents)} document(s)"
    )


    if not documents:

        with st.container(
            border=True
        ):

            st.subheader(
                "📭 No documents yet"
            )

            st.write(
                "Upload your first document above "
                "to start building your knowledge base."
            )


    else:

        for document in documents:

            extension = (
                document.suffix
                .replace(
                    ".",
                    "",
                )
                .upper()
            )

            icon = get_file_icon(
                document
            )


            with st.container(
                border=True
            ):

                col1, col2 = (
                    st.columns(
                        [6, 1]
                    )
                )


                with col1:

                    st.write(
                        f"{icon} **{document.name}**"
                    )

                    st.caption(
                        f"{extension} document"
                    )


                with col2:

                    if st.button(
                        "Remove",
                        key=(
                            f"remove_"
                            f"{document.name}"
                        ),
                    ):

                        try:

                            document.unlink()

                            st.success(
                                f"{document.name} removed."
                            )

                            st.rerun()


                        except Exception as error:

                            st.error(
                                "Could not remove "
                                f"document: {error}"
                            )