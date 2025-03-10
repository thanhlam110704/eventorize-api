from pathlib import Path
from typing import List, Union

from config import settings as root_settings
from core.schemas import EmailStr
from jinja2 import Template
from loguru import logger
from partners.v1.telegram.services import error_bot
from utils import http_client

from .config import settings
from .exceptions import ErrorCode as ResendErrorCode


class BaseResend:
    def __init__(self, api_key: str, host_mail: str, sender_name: str):
        """
        Initialize the BaseResend class.

        Args:
            api_key (str): The API key for Resend service.
            host_mail (str): The sender's email address.
            sender_name (str): The name to be displayed as the sender.
        """
        self.url = "https://api.resend.com/emails"
        self.api_key = api_key
        self.sender_email = host_mail
        self.sender_name = sender_name
        self.template_base_path = Path("../app/assets/templates")
        self.environment = root_settings.environment

        self.headers = {}
        self.headers["Authorization"] = f"Bearer {self.api_key}"
        self.headers["Content-Type"] = "application/json"

    async def get_template(self, template_name: str) -> str:
        """
        Load an email template from a file.

        Args:
            template_name (str): Name of the template file (without extension).

        Returns:
            str: The content of the template file.

        Raises:
            ResendErrorCode.TemplateNotFound: If the template file is not found.
        """
        template_path = self.template_base_path / f"{template_name}.html"
        try:
            with template_path.open("r", encoding="UTF-8") as file:
                return file.read()
        except FileNotFoundError:
            logger.error(f"Template not found: {template_path}")
            raise ResendErrorCode.TemplateNotFound(template_name=template_name)

    async def render(self, data: dict, template_name: str) -> str:
        """
        Render an email template with the provided data.

        Args:
            data (dict): Dictionary of data to render into the template.
            template_name (str): Name of the template to render.

        Returns:
            str: Rendered HTML string.
        """
        html_template = await self.get_template(template_name)
        jinja2_template = Template(html_template)
        return jinja2_template.render(**data)

    async def send_mail(self, recipients: Union[EmailStr, List[EmailStr]], subject: str, content: str):
        """
        Send an email using Resend.

        Args:
            recipients (Union[EmailStr, List[EmailStr]]): One or more recipient email addresses.
            subject (str): Subject of the email.
            content (str): HTML content of the email.

        Returns:
            dict: The email object from the Resend API response.

        Raises:
            ResendErrorCode.EmailSendFailed: If the email fails to send.
        """
        # Only send emails in production environment
        # if root_settings.is_production() is False:
        #     return
        # Normalize recipients to always be a list
        recipients_list = recipients if isinstance(recipients, list) else [recipients]
        payload = {"from": f"{self.sender_name} <{self.sender_email}>", "to": recipients_list, "subject": subject, "html": content}
        try:
            await http_client.post(url=self.url, json=payload, headers=self.headers)
        except Exception as e:
            logger.error(f"Failed to send email to {recipients_list}: {str(e)}")
            exc_list = str(e).splitlines()
            await error_bot.send_notify_email_failure(error_message=exc_list[0], recipients=recipients_list)


class UserMailService(BaseResend):
    def __init__(self, api_key: str, host_mail: str, sender_name: str):
        super().__init__(api_key, host_mail, sender_name)

    async def send_verification_email(self, recipient: EmailStr, fullname: str, otp: str) -> dict:
        data = {}
        data["fullname"] = fullname
        data["verification_link"] = f"{settings.verification_link}?email={recipient}&otp={otp}"
        data["otp"] = otp
        html_content = await self.render(data=data, template_name="verify_email")
        return await self.send_mail(recipients=recipient, subject="Welcome to Eventorize", content=html_content)

    async def send_reset_password_email(self, recipient: EmailStr, fullname: str, otp: str) -> dict:
        data = {}
        data["fullname"] = fullname
        data["reset_password_link"] = f"{settings.reset_password_link}?email={recipient}&otp={otp}"
        data["otp"] = otp
        html_content = await self.render(data=data, template_name="reset_password")
        return await self.send_mail(recipients=recipient, subject="Reset your password", content=html_content)


user_mail_services = UserMailService(api_key=settings.resend_api_key, host_mail=settings.host_email, sender_name=settings.sender_name)
