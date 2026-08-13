from datetime import datetime
from pathlib import Path
from uuid import uuid4
import json


# ============================================================
# PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIRECTORY = PROJECT_ROOT / "data"
CHAT_DIRECTORY = DATA_DIRECTORY / "chats"

CHAT_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# CONVERSATION STORE
# ============================================================

class ConversationStore:
    """
    Handles all conversation persistence.

    Responsibilities:
    - Create conversations
    - Load conversations
    - Save conversations
    - Update conversations
    - Delete conversations
    - Remove unused empty conversations

    UI logic does NOT belong here.
    """

    def __init__(self):
        CHAT_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )


    # ========================================================
    # INTERNAL HELPERS
    # ========================================================

    @staticmethod
    def _timestamp():
        return datetime.now().strftime(
            "%Y-%m-%d %H:%M"
        )


    @staticmethod
    def _chat_file(chat_id):
        return CHAT_DIRECTORY / f"{chat_id}.json"


    # ========================================================
    # CREATE
    # ========================================================

    def create_chat(self):
        """
        Create a completely new empty conversation.

        Every call creates a NEW unique conversation.
        """

        now = self._timestamp()

        chat = {
            "id": f"chat_{uuid4().hex}",
            "title": "New conversation",
            "created_at": now,
            "updated_at": now,
            "messages": [],
        }

        self.save_chat(chat)

        return chat


    # ========================================================
    # SAVE
    # ========================================================

    def save_chat(self, chat):
        """
        Save one conversation to JSON.
        """

        chat_id = chat.get("id")

        if not chat_id:
            raise ValueError(
                "Conversation must contain an id."
            )

        path = self._chat_file(chat_id)

        temporary_path = path.with_suffix(
            ".tmp"
        )

        with open(
            temporary_path,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                chat,
                file,
                indent=4,
                ensure_ascii=False,
            )

        temporary_path.replace(path)


    # ========================================================
    # LOAD ONE CHAT
    # ========================================================

    def get_chat(self, chat_id):
        """
        Return one conversation by ID.
        """

        if not chat_id:
            return None

        path = self._chat_file(chat_id)

        if not path.exists():
            return None

        try:

            with open(
                path,
                "r",
                encoding="utf-8",
            ) as file:

                chat = json.load(file)

            return self._normalize_chat(chat)

        except (
            json.JSONDecodeError,
            OSError,
            TypeError,
        ):

            return None


    # ========================================================
    # LOAD ALL CHATS
    # ========================================================

    def get_chats(self):
        """
        Return all valid conversations.

        Newest conversations are returned first.
        """

        chats = []

        for path in CHAT_DIRECTORY.glob(
            "*.json"
        ):

            try:

                with open(
                    path,
                    "r",
                    encoding="utf-8",
                ) as file:

                    chat = json.load(file)

                chat = self._normalize_chat(
                    chat
                )

                chats.append(chat)

            except (
                json.JSONDecodeError,
                OSError,
                TypeError,
            ):

                # Ignore broken files rather than
                # crashing the application.
                continue


        chats.sort(
            key=lambda chat: chat.get(
                "updated_at",
                "",
            ),
            reverse=True,
        )

        return chats


    # ========================================================
    # UPDATE
    # ========================================================

    def update_chat(
        self,
        chat_id,
        title=None,
        messages=None,
    ):
        """
        Update an existing conversation.
        """

        chat = self.get_chat(
            chat_id
        )

        if chat is None:
            return None


        if title is not None:
            chat["title"] = title


        if messages is not None:
            chat["messages"] = messages


        chat["updated_at"] = (
            self._timestamp()
        )

        self.save_chat(chat)

        return chat


    # ========================================================
    # DELETE
    # ========================================================

    def delete_chat(self, chat_id):
        """
        Delete one conversation.
        """

        if not chat_id:
            return False

        path = self._chat_file(
            chat_id
        )

        if not path.exists():
            return False

        try:

            path.unlink()

            return True

        except OSError:

            return False


    # ========================================================
    # DELETE EMPTY CONVERSATIONS
    # ========================================================

    def cleanup_empty_chats(self):
        """
        Delete conversations that contain no messages.

        This prevents unused 'New conversation'
        files from accumulating.
        """

        deleted = 0

        for chat in self.get_chats():

            messages = chat.get(
                "messages",
                [],
            )

            if not messages:

                if self.delete_chat(
                    chat["id"]
                ):

                    deleted += 1

        return deleted


    # ========================================================
    # NORMALIZATION
    # ========================================================

    @staticmethod
    def _normalize_chat(chat):
        """
        Make sure older JSON files remain compatible.
        """

        if not isinstance(
            chat,
            dict,
        ):
            raise TypeError(
                "Invalid conversation format."
            )


        chat.setdefault(
            "title",
            "New conversation",
        )

        chat.setdefault(
            "created_at",
            "",
        )

        chat.setdefault(
            "updated_at",
            chat.get(
                "created_at",
                "",
            ),
        )

        chat.setdefault(
            "messages",
            [],
        )


        if not isinstance(
            chat["messages"],
            list,
        ):

            chat["messages"] = []


        return chat