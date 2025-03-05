from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def EndTimeAfterStartTime():
        return CustomException(type="agendas/info/end-time-after-start-time", status=400, title="Incorrect time", detail="End time must be after start time.")

    @staticmethod
    def StartTimeOutOfRange():
        return CustomException(type="agendas/info/start-time-out-of-range", status=400, title="Start time out of event range", detail="Start time must be within event time range.")

    @staticmethod
    def EndTimeOutOfRange():
        return CustomException(type="agendas/info/end-time-out-of-range", status=400, title="End time out of event range", detail="End time must be within event time range.")

    @staticmethod
    def NotFound(agenda_id, event_id):
        return CustomException(type="agendas/info/not-found", status=400, title="Not found agenda", detail=f"No found agenda '{agenda_id}' for event '{event_id}'")

    @staticmethod
    def CheckInputTime():
        return CustomException(type="agendas/info/check-input-time", status=400, title="Missing field time", detail="Please input both start time and end time of agenda")
