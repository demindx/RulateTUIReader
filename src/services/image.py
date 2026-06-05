import io
import aiohttp
from PIL import Image, ImageDraw
from pydantic import HttpUrl


class ImageService:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        self._session: aiohttp.ClientSession = session

    async def get_image(self, url: HttpUrl) -> Image.Image:
        async with self._session.get(str(url)) as response:
            buff = io.BytesIO(await response.read())

            return Image.open(buff)

    async def get_rounded_image(self, url: HttpUrl) -> Image.Image:
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

            return img_square
