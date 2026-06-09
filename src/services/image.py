from time import time
import io
import aiohttp
from PIL import Image, ImageDraw
from pydantic import HttpUrl


_MAX_CACHE_SIZE: int = 100


class ImageService:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session: aiohttp.ClientSession = session
        self._cache: dict[str, tuple[Image.Image, float]] = {}

    def _get_cache_size(self) -> float:
        return (
            sum([len(img[0].tobytes()) for img in self._cache.values()]) / 1024
        ) / 1024

    def _get_from_cache(self, url: HttpUrl) -> Image.Image | None:
        img = self._cache.get(str(url))

        if not img:
            return None

        return img[0]

    def _add_to_cache(self, img: Image.Image, url: HttpUrl) -> None:
        size = self._get_cache_size()

        while size >= _MAX_CACHE_SIZE:
            oldest = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            size -= len(self._cache[oldest][0].tobytes())

            del self._cache[oldest]

        self._cache[str(url)] = (img, time())

    async def get_image(self, url: HttpUrl, size: tuple[int, int]) -> Image.Image:
        img = self._get_from_cache(url)

        if img:
            return img

        async with self._session.get(str(url)) as response:
            buff = io.BytesIO(await response.read())

            img = Image.open(buff)

            img.thumbnail(size)

            self._add_to_cache(img, url)

            return img

    async def get_rounded_image(
        self, url: HttpUrl, size: tuple[int, int]
    ) -> Image.Image:
        img = self._get_from_cache(url)
        if img:
            return img

        async with self._session.get(str(url)) as response:
            buff = io.BytesIO(await response.read())

            img = Image.open(buff).convert("RGBA")

            width, height = img.size
            min_side = min(width, height)

            left = (width - min_side) // 2
            top = (height - min_side) // 2
            right = left + min_side
            bottom = top + min_side
            img_square = img.crop((left, top, right, bottom))

            mask = Image.new("L", img_square.size, 0)
            draw = ImageDraw.Draw(mask)

            radius = min_side // 2
            draw.rounded_rectangle((0, 0, min_side, min_side), radius=radius, fill=255)

            img_square.putalpha(mask)

            img_square.thumbnail(size)

            self._add_to_cache(img_square, url)

            return img_square
