from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def AlreadyCheckIn():
        return CustomException(type="attendees/info/already-check-in", status=400, title="Already check in.", detail="Check in already exists.")

    @staticmethod
    def AlreadyCheckOut():
        return CustomException(type="attendees/info/already-check-out", status=400, title="Already check out.", detail="Check out already exists.")
    
    @staticmethod
    def NotFoundEvent(item: str):
        return CustomException(type="attendees/warning/not-found", status=404, title="Not Found.", detail=f"Event with {item} could not be found.")
