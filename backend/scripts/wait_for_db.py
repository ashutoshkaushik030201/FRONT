"""Polls the configured database until it accepts connections or attempts are exhausted."""
import asyncio
import os
import sys

import asyncpg


async def wait_for_db(max_attempts: int = 30, delay_seconds: float = 2.0) -> None:
    database_url = os.environ["DATABASE_URL"].replace("postgresql+asyncpg://", "postgresql://")
    for attempt in range(1, max_attempts + 1):
        try:
            conn = await asyncpg.connect(database_url)
            await conn.close()
            print("Database is ready.")
            return
        except (OSError, asyncpg.PostgresError) as exc:
            print(f"[{attempt}/{max_attempts}] Database not ready yet: {exc}")
            await asyncio.sleep(delay_seconds)
    print("Database did not become ready in time.", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    asyncio.run(wait_for_db())
