from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidVatAmount():
        return CustomException(type="orders/validation/invalid-vat-amount", status=400, title="Số tiền VAT không hợp lệ.", detail="Số tiền VAT tính toán không khớp với số tiền VAT cung cấp.")

    @staticmethod
    def InvalidTotalAmount():
        return CustomException(
            type="orders/validation/invalid-total-amount", status=400, title="Tổng số tiền không hợp lệ.", detail="Tổng số tiền tính toán không khớp với tổng số tiền cung cấp."
        )

    @staticmethod
    def OrderAlreadyActive():
        return CustomException(
            type="orders/validation/order-already-active", status=400, title="Đơn hàng đã kích hoạt.", detail="Đơn hàng bạn đang cố chấp nhận đã ở trạng thái kích hoạt."
        )