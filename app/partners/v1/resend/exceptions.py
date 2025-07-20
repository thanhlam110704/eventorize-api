from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def TemplateNotFound(template_name):
        return CustomException(type="resend/info/template-not-found", status=400, title="Không tìm thấy mẫu.", detail=f"Mẫu {template_name} không được tìm thấy.")