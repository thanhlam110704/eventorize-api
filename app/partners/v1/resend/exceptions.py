from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def TemplateNotFound(template_name):
        return CustomException(type="resend/info/template-not-found", status=400, title="Template Not Found", detail=f"This {template_name} template was not found.")
