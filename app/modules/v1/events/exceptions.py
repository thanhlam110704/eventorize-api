from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def EventAlreadyEnded(title_event):
        return CustomException(
            type="events/info/event-already-ended", status=400, title="Event has already ended", detail=f"Event '{title_event}' has already ended, so you cannot create an agenda for it."
        )

    @staticmethod
    def FileTooLarge():
        return CustomException(type="events/info/file-too-large", status=413, title="File too large.", detail="The uploaded file exceeds the maximum size of 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="events/info/image-or-file-required", status=400, title="Image or File Required", detail="Either 'image_url' or 'file' must be provided.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="events/info/only-one-input-allowed", status=400, title="Only One Input Allowed", detail="Provide only one of 'image_url' or 'file'.")

    @staticmethod
    def EventHasTickets():
        return CustomException(type="events/info/event-has-tickets", status=400, title="Event has tickets", detail="This event has tickets, so you cannot delete it.")
