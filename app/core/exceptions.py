from exceptions import CustomException


class ErrorCode:
    @staticmethod
    def NotFound(service_name: str, item: str):
        return CustomException(type=f"{service_name}/warning/not-found", status=404, title="Không tìm thấy.", detail=f"{service_name.capitalize()} với {item} không tồn tại.")

    @staticmethod
    def NotModified(service_name: str):
        return CustomException(type=f"{service_name}/warning/not-modified", status=304, title="Không có thay đổi.", detail="Nội dung không đổi từ yêu cầu trước.")

    @staticmethod
    def Conflict(service_name: str, item: str):
        return CustomException(type=f"{service_name}/warning/conflict", status=409, title="Dữ liệu xung đột.", detail=f"{item} đã tồn tại.")

    @staticmethod
    def InvalidObjectId(_id: str):
        return CustomException(
            type="core/info/invalid-object-id", status=400, title="Định dạng ID không hợp lệ.", detail=f"ID {_id} không hợp lệ."
        )

    @staticmethod
    def InvalidEmail(email: str):
        return CustomException(
            type="core/info/invalid-email", status=400, title="Định dạng email không hợp lệ.", detail=f"Email {email} không hợp lệ."
        )

    @staticmethod
    def InvalidPhone(phone: str):
        return CustomException(
            type="core/info/invalid-phone", status=400, title="Định dạng số điện thoại không hợp lệ.", detail=f"Số {phone} không hợp lệ."
        )

    @staticmethod
    def InvalidDate(date: str):
        return CustomException(
            type="core/info/invalid-date", status=400, title="Định dạng ngày không hợp lệ.", detail=f"Ngày {date} không đúng định dạng YYYY-MM-DD."
        )

    @staticmethod
    def InvalidDateTime(date: str):
        return CustomException(
            type="core/info/invalid-date-time",
            status=400,
            title="Định dạng ngày giờ không hợp lệ.",
            detail=f"Ngày giờ {date} không đúng định dạng YYYY-MM-DD HH:MM:SS."
        )

    @staticmethod
    def InvalidUrl(url: str):
        return CustomException(type="core/info/invalid-url", status=400, title="Định dạng URL không hợp lệ.", detail=f"URL {url} không hợp lệ.")

    @staticmethod
    def Unauthorize():
        return CustomException(type="core/warning/unauthorize", status=401, title="Không được ủy quyền.", detail="Thông tin đăng nhập không hợp lệ.")