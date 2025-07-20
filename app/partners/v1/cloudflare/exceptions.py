from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class R2ErrorCode(CoreErrorCode):
    @staticmethod
    def UploadFailed():
        return CustomException(type="r2/error/upload", status=500, title="Lỗi tải lên.", detail="Đã xảy ra lỗi không mong muốn khi tải tệp lên.")