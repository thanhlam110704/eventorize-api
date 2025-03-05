from typing import List

from config import settings as root_settings
from loguru import logger
from telebot.async_telebot import AsyncTeleBot
from utils import converter

from .config import settings


class BaseBot:
    def __init__(self, bot_token: str, channel_ids: list | str) -> None:
        self.text_mode = "HTML"
        self.bot = AsyncTeleBot(bot_token)
        self.channel_ids = [channel_ids] if type(channel_ids) is str else channel_ids
        self.environment = root_settings.environment

    async def send_message(self, message: str):
        if root_settings.is_production() is False:
            return

        for channel_id in self.channel_ids:
            try:
                await self.bot.send_message(channel_id, message, parse_mode=self.text_mode, disable_web_page_preview=True)
            except Exception as e:
                logger.error(f"Error sending message to telegram: {str(e)}")

    def get_module(self, api_path):
        endpoints = api_path.split("/")
        if len(endpoints) <= 2:
            return endpoints[1]
        return endpoints[1] + "/" + endpoints[2]


class ErrorBot(BaseBot):
    def __init__(self, bot_token, channel_ids):
        super().__init__(bot_token, channel_ids)

    async def send_error(self, exc_list, request, response, request_id, issue_link):
        name_error = file_error = line_number_error = function_error = line_error = None
        if exc_list:
            name_error = exc_list[-1].replace("\r\n", "")
            name_error = name_error[:100]
            error_detail = exc_list[-2]
            error_list = error_detail.split()
            file_error = error_list[error_list.index("File") + 1][:-1]
            line_number_error = error_list[error_list.index("line") + 1][:-1]
            function_error = error_list[error_list.index("in") + 1]
            line_error = error_detail.splitlines()[-1].strip()

        message = (
            f"**❌ THÔNG BÁO LỖI**\n\n"
            f"**Enviroment**: {self.environment}\n"
            f"**Title**: {name_error}\n"
            f"**File error** <pre language='shell'>{file_error}</pre>\n"
            f"**Line**: {line_number_error}\n"
            f"**Function**: {function_error}\n"
            f"**API**: {request.url.path}\n"
            f"**Method**: {request.method}\n"
            f"**Status code**: {response.status_code}\n"
            f"**Request Id**: {request_id}\n"
            f"**Issue link**: {issue_link}\n"
            f"**Line error** <pre language='python'>{line_error}</pre>"
        )
        await self.send_message(message)

    async def send_notify_email_failure(self, error_message: str, recipients: List[str]) -> None:
        message = f"<b>❌ Email Send Failure Notification</b>\n\n" f"<b>Error Message</b>: {error_message}\n" f"<b>Recipients</b>: {', '.join(recipients)}\n"
        await self.send_message(message)

    async def send_warning(self, warning_message: str, action: str) -> None:
        formatted_message = (
            "<b>⚠️ Warning</b>\n\n"
            "<i>An issue occurred while processing the request:</i>\n\n"
            f"<b>Detail</b>: {warning_message}\n"
            f"<b>Action</b>:" f"{action}\n\n"
            "Please check the logs or retry the request if necessary."
        )
        await self.send_message(formatted_message)


class OrderBot(BaseBot):
    def __init__(self, bot_token, channel_ids):
        super().__init__(bot_token, channel_ids)

    async def new_order(self, order_id: str, order_no: str, amount: int, product_name: str, quantity: int, user_fullname: str, user_email: str, created_by: str):
        amount = converter.convert_to_vnd_currency(amount)
        message = (
            f"<b>🛒 New Order</b>\n\n"
            f"<b>Order ID</b>: {order_id}\n"
            f"<b>Order No</b>: {order_no}\n"
            f"<b>Amount</b>: {amount}\n"
            f"<b>Product Name</b>: {product_name}\n"
            f"<b>Quantity</b>: {quantity}\n"
            f"<b>Customer Name</b>: {user_fullname}\n"
            f"<b>Customer Email</b>: {user_email}\n"
            f"<b>Created by</b>: {created_by}"
        )
        await self.send_message(message)

    async def order_accepted(self, order_id: str, order_no: str, amount: int, product_name: str, quantity: int, user_fullname: str, user_email: str, accepted_by: str):
        amount = converter.convert_to_vnd_currency(amount)
        message = (
            f"<b>✅ Accept Order</b>\n\n"
            f"<b>Order ID</b>: {order_id}\n"
            f"<b>Order No</b>: {order_no}\n"
            f"<b>Amount</b>: {amount}\n"
            f"<b>Product Name</b>: {product_name}\n"
            f"<b>Quantity</b>: {quantity}\n"
            f"<b>Customer Name</b>: {user_fullname}\n"
            f"<b>Customer Email</b>: {user_email}\n"
            f"<b>Accepted by</b>: {accepted_by}"
        )
        await self.send_message(message)


error_bot = ErrorBot(bot_token=settings.error_bot_token_telegram, channel_ids=settings.error_channel_ids)
order_bot = OrderBot(bot_token=settings.bot_token_telegram, channel_ids=settings.order_channel_ids)
