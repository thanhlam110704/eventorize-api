from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def EventAlreadyEnded(title_event):
        return CustomException(
            type="events/info/event-already-ended", status=400, title="Sự kiện đã kết thúc.", detail=f"Sự kiện '{title_event}' đã kết thúc, bạn không thể tạo chương trình cho nó."
        )

    @staticmethod
    def FileTooLarge():
        return CustomException(type="events/info/file-too-large", status=413, title="Tệp quá lớn.", detail="Tệp tải lên vượt quá kích thước tối đa 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="events/info/image-or-file-required", status=400, title="Yêu cầu hình ảnh hoặc tệp.", detail="Phải cung cấp 'image_url' hoặc 'file'.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="events/info/only-one-input-allowed", status=400, title="Chỉ được cung cấp một đầu vào.", detail="Chỉ cung cấp một trong hai: 'image_url' hoặc 'file'.")

    @staticmethod
    def EventHasTickets():
        return CustomException(type="events/info/event-has-tickets", status=400, title="Sự kiện đã có vé.", detail="Sự kiện này có vé, bạn không thể xóa nó.")

    @staticmethod
    def InvalidFilter():
        return CustomException(type="events/info/invalid-filter", status=400, title="Bộ lọc không hợp lệ.", detail="Bộ lọc không đúng.")