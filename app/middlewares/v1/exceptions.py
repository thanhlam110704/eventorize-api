from fastapi.responses import JSONResponse


class ErrorCode:
    @staticmethod
    def Unauthorize():
        response = {}
        response["type"] = "core/warning/unauthorize"
        response["status"] = 401
        response["title"] = "Unauthorized."
        response["detail"] = "Could not authorize credentials."
        return JSONResponse(status_code=401, content=response)

    @staticmethod
    def SomethingWentWrong():
        response = {}
        response["type"] = "middlewares/error/server"
        response["status"] = 500
        response["title"] = "Something went wrong."
        response["detail"] = "Something went wrong. Please read the documentation or contact support for assistance."
        return JSONResponse(status_code=500, content=response)

    @staticmethod
    def EmailNotVerified():
        response = {}
        response["type"] = "core/warning/email-not-verified"
        response["status"] = 403
        response["title"] = "Email Not Verified."
        response["detail"] = "You must verify your email to use this service."
        return JSONResponse(status_code=403, content=response)
