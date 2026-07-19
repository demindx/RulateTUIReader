import aiohttp

from src.core.exceptions import RequestError
from src.models.response import RulateResponse


class BaseApiClient:
    async def _validate_response(
        self, response: aiohttp.ClientResponse
    ) -> RulateResponse:
        try:
            response.raise_for_status()
        except aiohttp.ClientResponseError as e:
            raise RequestError(str(e)) from e

        if response.headers["Content-Type"] != "application/json":
            body = await response.read()
            raise RequestError(f"Invalid response type: {body.decode()}")

        json = await response.json()

        data = RulateResponse.model_validate(json)

        if data.status == "fail":
            raise RequestError(data.msg)

        return data
