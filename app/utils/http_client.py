from typing import Any, Dict, Optional

import httpx
from partners.v1.telegram.services import error_bot

from .config import settings


async def send(method: str, url: str, verify: bool = True, **kwargs: Any) -> httpx.Response:
    """
    Send an HTTP request using httpx AsyncClient.

    Args:
        method: HTTP method (GET, POST, PUT, DELETE)
        url: Target URL
        verify: SSL verification flag
        **kwargs: Additional arguments to pass to the request

    Returns:
        httpx.Response: Response from the server

    Raises:
        httpx.RequestError: If the request fails
        httpx.HTTPStatusError: If the response has an error status code
    """
    timeout = httpx.Timeout(settings.total_request_timeout, connect=settings.server_connection_timeout)
    transport = httpx.AsyncHTTPTransport(retries=settings.max_retry_attempts, verify=verify)

    try:
        async with httpx.AsyncClient(timeout=timeout, transport=transport, http2=True) as client:
            response = await client.request(method, url, **kwargs)
            return response

    except httpx.RequestError as exc:
        exc_list = str(exc).splitlines()
        await error_bot.send_warning(warning_message=exc_list[0], action="request at http_client.py")
    except httpx.HTTPStatusError as exc:
        exc_list = str(exc).splitlines()
        await error_bot.send_warning(warning_message=exc_list[0], action="request at http_client.py")


async def get(
    url: str,
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    follow_redirects: bool = True,
    verify: bool = True,
    content: Optional[bytes] = None,
) -> httpx.Response:
    return await send(method="GET", url=url, params=params, data=data, json=json, headers=headers, follow_redirects=follow_redirects, verify=verify, content=content)


async def post(
    url: str,
    params: Optional[Dict] = None,
    data: Optional[Dict] = None,
    json: Optional[Dict] = None,
    headers: Optional[Dict] = None,
    files: Optional[Any] = None,
    follow_redirects: bool = True,
    verify: bool = True,
) -> httpx.Response:
    return await send(method="POST", url=url, params=params, data=data, json=json, headers=headers, files=files, follow_redirects=follow_redirects, verify=verify)


async def put(url: str, params: Optional[Dict] = None, data: Optional[Dict] = None, json: Optional[Dict] = None, headers: Optional[Dict] = None, verify: bool = True) -> httpx.Response:
    return await send(method="PUT", url=url, params=params, data=data, json=json, headers=headers, verify=verify)


async def delete(url: str, params: Optional[Dict] = None, data: Optional[Dict] = None, json: Optional[Dict] = None, headers: Optional[Dict] = None, verify: bool = True) -> httpx.Response:
    return await send(method="DELETE", url=url, params=params, data=data, json=json, headers=headers, verify=verify)
