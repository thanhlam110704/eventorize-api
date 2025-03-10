from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class R2ErrorCode(CoreErrorCode):
    @staticmethod
    def UploadFailed():
        return CustomException(type="r2/error/upload", status=500, title="Error occurred during upload", detail="An unexpected error occurred while uploading the file")
