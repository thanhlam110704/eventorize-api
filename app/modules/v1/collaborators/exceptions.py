from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def CollaboratorAlreadyAccepted():
        return CustomException(
            type="collaborators/info/already-accepted", status=400, title="Collaborator already accepted.", detail="The collaborator has already been accepted and cannot be accepted again."
        )

    @staticmethod
    def CollaboratorAlreadyInvited():
        return CustomException(
            type="collaborators/info/already-invited", status=400, title="Collaborator already invited.", detail="The collaborator has already been invited and is currently pending."
        )
