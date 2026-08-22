from pathlib import Path
import shutil

import os
from dotenv import load_dotenv

import chainlit as cl
from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from app.dependencies import create_knowledge_base
from config import UPLOAD_DIRECTORY

# lead environment variables from .env file
load_dotenv()

UPLOAD_DIR = Path(UPLOAD_DIRECTORY)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_URL = os.getenv("DATABASE_URL")

# ============================================================
# Authentication
# ============================================================

DEV_USERS = {
    "prince": "1234",
    "alice": "5678",
}


@cl.password_auth_callback
def auth_callback(username: str, password: str):
    print(f"LOGIN ATTEMPT: username={username!r}")

    if DEV_USERS.get(username) == password:
        print("LOGIN SUCCESSFUL")

        return cl.User(
            identifier=username,
            metadata={
                "role": "user",
            },
        )

    print("LOGIN FAILED")
    return None
# ============================================================
# chat resume
# ============================================================
@cl.on_chat_resume
async def on_chat_resume(thread):
    pass

# ============================================================
# Application services
# ============================================================
(
rag_service, document_service , document_lifecycle_service 
) = create_knowledge_base()



# ============================================================
# Document display
# ============================================================

def _extract_document_info(document: dict) -> tuple[str, str]:
    """
    Extract filename and formatted file type from document metadata.
    """
    filename = document.get("filename", "Unknown document")
    file_type = document.get("type", "").upper() or "FILE"
    return filename, file_type


async def refresh_sidebar(user_id: str) -> None:
    """
    Sidebar is currently handled by Chainlit's native UI.
    Document listing is available through /docs.
    """
    return


async def get_documents_sidebar_content(user_id: str) -> str:
    """
    Generate sidebar content showing uploaded documents.
    Returns markdown string for the sidebar.
    """
    documents = document_service.list_documents(user_id=user_id)

    if not documents:
        return "**📚 Documents**\n\nNo documents in the knowledge base."

    lines = ["**📚 Documents**"]
    for document in documents:
        filename, file_type = _extract_document_info(document)
        lines.append(f"📄 **{filename}** `{file_type}`")
    lines.append("")  # spacer
    return "\n".join(lines)


async def show_documents(user_id: str | None = None) -> None:
    """
    Display all documents currently stored in the knowledge base.
    If user_id is not provided, retrieves from current user session.
    """
    if user_id is None:
        user_id = get_current_user_id()

    documents = document_service.list_documents(user_id=user_id)

    if not documents:
        await cl.Message(
            content=(
                "📚 **Documents**\n\n"
                "No documents are currently in the knowledge base.\n\n"
                "Upload a file to get started!"
            )
        ).send()
        return

    # Create summary message
    doc_count = len(documents)
    summary = f"📚 **Knowledge Base** ({doc_count} document{'s' if doc_count != 1 else ''})\n\n"
    
    # Build document list
    for idx, document in enumerate(documents, 1):
        filename, file_type = _extract_document_info(document)
        summary += f"{idx}. **{filename}** `[{file_type}]`\n"

    await cl.Message(content=summary).send()

    # Send detailed cards for each document
    for document in documents:
        filename, file_type = _extract_document_info(document)
        
        await cl.Message(
            content=(
                f"📄 **{filename}**\n"
                f"Type: `{file_type}`"
            ),
            actions=[
                cl.Action(
                    name="delete_document",
                    label="🗑️ Delete",
                    payload={"filename": filename},
                )
            ],
        ).send()


# ============================================================
# Chat start
# ============================================================

@cl.on_chat_start
async def start():

    await cl.Message(
        content=(
            "👋 **Welcome to AI Knowledge Assistant**\n\n"
            "Upload a PDF, DOCX, TXT, or Markdown file to get started, "
            "then ask questions about your documents.\n\n"
            "**Commands**\n"
            "- `/docs` — View all uploaded documents\n"
            "- `/sync` — Sync manually added files from uploads folder"
        )
    ).send()

    # Keep sidebar open and populated, but don't flood chat with document cards
    user_id = get_current_user_id()
    await refresh_sidebar(user_id)


# ============================================================
# Document deletion
# ============================================================

@cl.action_callback("delete_document")
async def delete_document(action: cl.Action):

    filename = action.payload["filename"]
    user_id = get_current_user_id()

    deleted_chunks = await document_service.delete_document(
        user_id=user_id,
        filename=filename,
    )

    if deleted_chunks == 0:
        await cl.Message(
            content=(
                f"⚠️ `{filename}` was not found "
                "in the knowledge base."
            )
        ).send()
        return

    await cl.Message(
        content=(
            f"🗑️ **Deleted:** `{filename}`\n\n"
            f"Removed chunks: **{deleted_chunks}**"
        )
    ).send()

    # Refresh sidebar
    await refresh_sidebar(user_id)


# ============================================================
# Message handler
# ============================================================

@cl.on_message
async def message_handler(message: cl.Message):

    # --------------------------------------------------------
    # File upload
    # --------------------------------------------------------

    if message.elements:

        for element in message.elements:

            filename = element.name
            temporary_path = Path(element.path)

            await cl.Message(
                content=f"📄 Processing `{filename}`..."
            ).send()

            try:

                # ------------------------------------------------
                # Preserve original filename
                # ------------------------------------------------

                user_id = get_current_user_id()

                user_upload_dir = UPLOAD_DIR / user_id
                user_upload_dir.mkdir(parents=True, exist_ok=True)

                final_path = user_upload_dir / filename

                shutil.copy2(
                    temporary_path,
                    final_path,
                )

                result = await document_lifecycle_service.upload_document(
                    file_path=str(final_path),
                    user_id=user_id,
                )

                if result["duplicate"]:

                    await cl.Message(
                        content=(
                            f"ℹ️ **{filename}** is already in your knowledge base.\n\n"
                            "Skipped duplicate ingestion."
                        )
                    ).send()

                else:

                    await cl.Message(
                        content=(
                            f"✅ **{filename}** has been added.\n\n"
                            f"Chunks created: **{result['chunks']}**"
                        )
                    ).send()

            except Exception as e:

                await cl.Message(
                    content=(
                        f"❌ Failed to process "
                        f"`{filename}`.\n\n"
                        f"Error: `{str(e)}`"
                    )
                ).send()

        # Refresh sidebar after upload
        await refresh_sidebar(user_id)

        return

    # --------------------------------------------------------
    # Command handling
    # --------------------------------------------------------

    user_input = message.content.strip()

    if not user_input:
        return

    # Handle /docs command
    if user_input.lower() == "/docs":
        await show_documents()
        return

    # Handle /sync command
    if user_input.lower() == "/sync":
        user_id = get_current_user_id()
        count = await document_service.sync_uploads_folder(user_id)
        await cl.Message(
            content=f"✅ Synced uploads folder. Ingested {count} new document(s)."
        ).send()
        await refresh_sidebar(user_id)
        return

    # --------------------------------------------------------
    # Normal question
    # --------------------------------------------------------

    user_id = get_current_user_id()

    answer = rag_service.ask(
        question=user_input,
        top_k=3,
        user_id=user_id,
    )

    await cl.Message(
        content=answer
    ).send()

# ============================================================
# Data layer
# ============================================================

@cl.data_layer
def get_data_layer():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured"
        )

    return SQLAlchemyDataLayer(
        conninfo=database_url,
        ssl_require=True,
        show_logger=True,
    )


# ============================================================
# Current authenticated user
# ============================================================

def get_current_user_id() -> str:
    user = cl.user_session.get("user")

    if not user:
        raise RuntimeError("No authenticated user found.")

    return user.identifier