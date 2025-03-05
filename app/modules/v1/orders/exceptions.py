from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidVatAmount():
        return CustomException(type="orders/validation/invalid-vat-amount", status=400, title="Invalid VAT amount", detail="The VAT amount calculated does not match the provided VAT amount.")

    @staticmethod
    def InvalidTotalAmount():
        return CustomException(
            type="orders/validation/invalid-total-amount", status=400, title="Invalid Total amount", detail="The total amount calculated does not match the provided total amount."
        )

    @staticmethod
    def OrderAlreadyActive():
        return CustomException(
            type="orders/validation/order-already-active", status=400, title="Order Already Active", detail="The order you are trying to accept is already in active status."
        )
