from fastapi.responses import JSONResponse


class ErrorCode:
    @staticmethod
    def Unauthorize():
        response = {}
        response["type"] = "core/warning/unauthorize"
        response["status"] = 401
        response["title"] = "Không được ủy quyền."
        response["detail"] = "Thông tin đăng nhập không hợp lệ."
        return JSONResponse(status_code=401, content=response)

    @staticmethod
    def SomethingWentWrong():
        response = {}
        response["type"] = "middlewares/error/server"
        response["status"] = 500
        response["title"] = "Có lỗi xảy ra."
        response["detail"] = "Hệ thống gặp lỗi. Vui lòng xem tài liệu hoặc liên hệ hỗ trợ."
        return JSONResponse(status_code=500, content=response)

    @staticmethod
    def EmailNotVerified():
        response = {}
        response["type"] = "core/warning/email-not-verified"
        response["status"] = 403
        response["title"] = "Email chưa được xác minh."
        response["detail"] = "Bạn cần xác minh email để sử dụng dịch vụ này."
        return JSONResponse(status_code=403, content=response)