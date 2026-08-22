import asyncio

from sqlalchemy import text

from database.session import AsyncSessionLocal


async def main():

    async with AsyncSessionLocal() as session:

        print(
            "Database:",
            session.bind.url.render_as_string(
                hide_password=True
            ),
        )

        result = await session.execute(
            text("SELECT COUNT(*) FROM documents")
        )

        print(
            "Documents:",
            result.scalar(),
        )

        result = await session.execute(
            text(
                """
                SELECT
                    user_id,
                    filename,
                    processing_status
                FROM documents
                ORDER BY uploaded_at DESC
                """
            )
        )

        print("Rows:")

        for row in result:
            print(row)


if __name__ == "__main__":
    asyncio.run(main())