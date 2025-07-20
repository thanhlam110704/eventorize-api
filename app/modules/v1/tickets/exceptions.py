from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidDateOfSale():
        return CustomException(
            type="tickets/info/invalid-date-of-sale", status=400, title="Ngày bán không hợp lệ.", detail="Ngày bắt đầu bán phải trước ngày kết thúc bán."
        )

    @staticmethod
    def InvalidQuantity():
        return CustomException(type="tickets/info/invalid-quantity", status=400, title="Số lượng không hợp lệ.", detail="Số lượng phải từ 1 đến 100000.")

    @staticmethod
    def InvalidMaxQuantity():
        return CustomException(type="tickets/info/invalid-max", status=400, title="Số lượng tối đa không hợp lệ.", detail="Số lượng tối đa phải từ 1 đến 100.")

    @staticmethod
    def InvalidMinQuantity():
        return CustomException(type="tickets/info/invalid-min", status=400, title="Số lượng tối thiểu không hợp lệ.", detail="Số lượng tối thiểu phải từ 1 đến 100.")

    @staticmethod
    def InvalidMaxMin():
        return CustomException(type="tickets/info/invalid-max-min", status=400, title="Số lượng tối thiểu không hợp lệ.", detail="Số lượng tối thiểu phải nhỏ hơn hoặc bằng tối đa.")

    @staticmethod
    def InvalidPrice():
        return CustomException(type="tickets/info/invalid-price", status=400, title="Giá không hợp lệ.", detail="Giá vé phải lớn hơn hoặc bằng 0$.")

    @staticmethod
    def InvalidEventId():
        return CustomException(type="tickets/info/invalid-event-id", status=400, title="ID sự kiện không hợp lệ.", detail="ID sự kiện cung cấp không khớp với vé.")

    @staticmethod
    def TicketNotYetOnSale():
        return CustomException(type="tickets/info/not-yet-on-sale", status=400, title="Vé chưa mở bán.", detail="Vé chưa được mở bán.")

    @staticmethod
    def TicketExpired():
        return CustomException(type="tickets/info/ticket-expired", status=400, title="Vé đã hết hạn.", detail="Thời gian bán vé đã kết thúc.")

    @staticmethod
    def TicketSoldOut():
        return CustomException(type="tickets/info/sold-out", status=400, title="Vé đã bán hết.", detail="Vé đã hết và không còn sẵn.")

    @staticmethod
    def TicketNotEnough():
        return CustomException(type="tickets/info/not-enough", status=400, title="Không đủ vé.", detail="Số lượng vé còn lại ít hơn số lượng yêu cầu.")

    @staticmethod
    def InvalidMiniumQuantity():
        return CustomException(
            type="tickets/info/invalid-min-quantity", status=400, title="Số lượng tối thiểu không hợp lệ.", detail="Số lượng yêu cầu nhỏ hơn số lượng tối thiểu cho phép."
        )

    @staticmethod
    def InvalidMaximumQuantity():
        return CustomException(
            type="tickets/info/invalid-max-quantity", status=400, title="Số lượng tối đa không hợp lệ.", detail="Số lượng yêu cầu vượt quá số lượng tối đa cho phép."
        )

    @staticmethod
    def InvalidCalculatePrice():
        return CustomException(type="tickets/info/invalid-price", status=400, title="Giá vé không hợp lệ.", detail="Giá vé không khớp với giá cung cấp.")

    @staticmethod
    def OwnerCannotBuyOwnTicket():
        return CustomException(type="tickets/purchase/owner-restriction", status=400, title="Hạn chế mua vé.", detail="Người tạo vé không thể mua vé của chính mình.")

    @staticmethod
    def InvalidSaleDates():
        return CustomException(type="tickets/info/invalid-sale-dates", status=400, title="Ngày bán vé không hợp lệ.", detail="Ngày bán vé phải nằm trong khoảng thời gian sự kiện.")