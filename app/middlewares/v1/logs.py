import json
import sys
import time
import traceback
import uuid

from db.base import BaseCRUD
from db.engine import engine_logs
from fastapi import Request
from loguru import logger
from partners.v1.telegram.services import error_bot

# from starlette.background import BackgroundTask
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.base import BaseHTTPMiddleware

from .config import ACTION_EXCEPT, UNSEND_NOTIFY_ENDPOINTS, settings
from .exceptions import ErrorCode as MiddlewareErrorCode


class Logs:
    def __init__(self, request: Request) -> None:
        self.request = request
        self.start_time = time.time()
        self.request_id = self.get_request_id()
        self.endpoint = self.get_endpoint(request)

    def get_request_id(self):
        return str(uuid.uuid4())

    def get_endpoint(self, request):
        endpoints = (request.url.path).split("/")
        if len(endpoints) <= 2:
            return endpoints[1]
        return endpoints[1] + "/" + endpoints[2]

    async def get_process_time(self):
        return str(time.time() - self.start_time)

    async def _parse_body(self, body):
        try:
            data = json.loads(body.decode("utf-8"))
            if not data:
                return {}
            return data
        except Exception:
            return {}

    async def set_request_body(self, request):
        content_type = request.headers.get("Content-Type", "")
        if "application/json" in content_type:
            try:
                self.request_body = await request.json()
            except ValueError:
                self.request_body = {}
        elif "multipart/form-data" in content_type:
            async with request.form() as form:
                item = {k: str(v) for k, v in form.items()}
                self.request_body = item
        else:
            self.request_body = {}

    async def set_response_body(self, response, status_code: int, is_error: bool = False):
        if is_error:
            json_content = {"error": response}
            body = json.dumps(json_content, indent=2).encode("utf-8")
        else:
            body = b"".join(response)
        self.response_body = await self._parse_body(body)
        self.status_code = status_code

    async def save(self):
        if self.request.url.path in ACTION_EXCEPT or not self.endpoint:
            return None
        if settings.environment not in ["production", "staging"]:
            return

        request_data = {
            "url": str(self.request.url),
            "method": self.request.method,
            "status_code": self.status_code,
            "header": dict(self.request.headers),
            "params": dict(self.request.query_params),
            "body": self.request_body,
            "request_ip": self.request.client.host,
            "created_at": time.time(),
        }

        data_save = {"endpoint": self.endpoint, "request_id": self.request_id, "request": request_data, "response": self.response_body, "created_at": time.time()}
        crud = BaseCRUD(engine_logs, self.endpoint)
        await crud.save(data_save)


class LogsMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)

    async def dispatch(self, request, call_next):
        log = Logs(request)
        await request.body()
        await log.set_request_body(request)
        exc_list = issue_link = None
        try:
            response = await call_next(request)
            response_body = [chunk async for chunk in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body))
            await log.set_response_body(response_body, response.status_code, is_error=False)
        except Exception as err:
            exc_list = traceback.format_exception(*sys.exc_info())
            exc = "".join(exc_list)
            logger.debug(exc)
            await log.set_response_body(exc, status_code=500, is_error=True)
            response = MiddlewareErrorCode.SomethingWentWrong()

        response.headers["X-Process-Time"] = await log.get_process_time()
        response.headers["X-Request-ID"] = log.request_id

        # Save log
        # response.background = BackgroundTask(log.save)
        # Don't send notify with url get/me
        if request.url.path in UNSEND_NOTIFY_ENDPOINTS:
            return response

        if response.status_code == 500:
            await error_bot.send_error(exc_list, request, response, log.request_id, issue_link)
        return response
