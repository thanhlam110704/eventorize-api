from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def FileTooLarge():
        return CustomException(type="organizers/info/file-too-large", status=413, title="File too large.", detail="The uploaded file exceeds the maximum size of 5MB.")

    @staticmethod
    def ImageOrFileRequired():
        return CustomException(type="organizers/info/image-or-file-required", status=400, title="Image or File Required", detail="Either 'image_url' or 'file' must be provided.")

    @staticmethod
    def OnlyOneInputAllowed():
        return CustomException(type="organizers/info/only-one-input-allowed", status=400, title="Only One Input Allowed", detail="Provide only one of 'image_url' or 'file'.")

    @staticmethod
    def OrganizerHasEvents():
        return CustomException(type="organizers/info/organizer-has-events", status=400, title="Organizer has events", detail="This organizer has events, so you cannot delete it.")
