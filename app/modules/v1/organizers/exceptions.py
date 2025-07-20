from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def FileTooLarge():
        return CustomException(type="organizers/info/file-too-large", status=413, title="Tệp quá lớn.", detail="Tệp tải lên vượt quá kích thước tối đa 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="organizers/info/image-or-file-required", status=400, title="Yêu cầu hình ảnh hoặc tệp.", detail="Phải cung cấp 'image_url' hoặc 'file'.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="organizers/info/only-one-input-allowed", status=400, title="Chỉ được cung cấp một đầu vào.", detail="Chỉ cung cấp một trong hai: 'image_url' hoặc 'file'.")

    @staticmethod
    def OrganizerHasEvents():
        return CustomException(type="organizers/info/organizer-has-events", status=400, title="Nhà tổ chức có sự kiện.", detail="Nhà tổ chức này có sự kiện, bạn không thể xóa.")