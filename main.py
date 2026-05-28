import asyncio

import aiohttp
from src.api.api import ApiClient
from src.config import config
from yarl import URL

from src.core.keyring import get_token


async def auth_middleware(
    req: aiohttp.ClientRequest, handler: aiohttp.ClientHandlerType
) -> aiohttp.ClientResponse:

    req.url = req.url.update_query({"key": config.API_KEY})

    return await handler(req)


async def main():
    session: aiohttp.ClientSession = aiohttp.ClientSession(
        base_url=URL(str(config.API_BASE_URL)).with_query(key=config.API_KEY),
        headers={
            "user-agent": "RuLateApp Android",
        },
        middlewares=(auth_middleware,),
    )

    client = ApiClient(session)

    token = get_token()

    user = await client.user.login(config.TEST_LOGIN, config.TEST_PASS)

    if token:
        session.headers["Authorization"] = f"Bearer {token}"

    bookmarks = await client.book.get_bookmarks()

    chapters = await client.book.get_chapters(book_id=26517)

    chapter = await client.book.get_chapter(book_id=26517, chapter_id=645204)
    print(chapter)

    await session.close()


if __name__ == "__main__":
    asyncio.run(main())
