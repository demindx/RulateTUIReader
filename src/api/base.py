import aiohttp

from src.core.exceptions import RequestException
from src.models.response import RulateResponse


class BaseApiClient:
    async def _validate_response(
        self, response: aiohttp.ClientResponse
    ) -> RulateResponse:
        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise RequestException(str(e))

        if response.headers["Content-Type"] != "application/json":
            raise RequestException(f"Invalid response type: {await response.read()}")

        json = await response.json()

        data = RulateResponse.model_validate(json)

        if data.status == "fail":
            raise RequestException(data.msg)

        return data
