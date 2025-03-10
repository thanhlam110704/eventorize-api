from core.exceptions import ErrorCode as CoreErrorCode
from exceptions import CustomException


class ErrorCode(CoreErrorCode):
    @staticmethod
    def InvalidDateOfSale():
        return CustomException(
            type="tickets/info/invalid-date-of-sale", status=400, title="Invalid date of sale.", detail="The start date of the sale must be less than the end date of the sale."
        )

    @staticmethod
    def InvalidQuantity():
        return CustomException(type="tickets/info/invalid-quantity", status=400, title="Invalid quantity.", detail="The quantity must be between 1 and 100000.")

    @staticmethod
    def InvalidMaxQuantity():
        return CustomException(type="tickets/info/invalid-max", status=400, title="Invalid max per user.", detail="Max must be between 1 and 100.")

    @staticmethod
    def InvalidMinQuantity():
        return CustomException(type="tickets/info/invalid-min", status=400, title="Invalid min per user.", detail="Min must be between 1 and 100.")

    @staticmethod
    def InvalidMaxMin():
        return CustomException(type="tickets/info/invalid-max-min", status=400, title="Invalid min per user.", detail="Min must be less than or equal Max.")

    @staticmethod
    def InvalidPrice():
        return CustomException(type="tickets/info/invalid-price", status=400, title="Invalid price.", detail="The Price must be greater than or equal 0$")

    @staticmethod
    def InvalidEventId():
        return CustomException(type="tickets/info/invalid-event-id", status=400, title="Invalid Event ID", detail="The provided event ID does not match with the ticket's event ID.")

    @staticmethod
    def TicketNotYetOnSale():
        return CustomException(type="tickets/info/not-yet-on-sale", status=400, title="Ticket not yet on sale.", detail="The ticket is not yet available for sale.")

    @staticmethod
    def TicketExpired():
        return CustomException(type="tickets/info/ticket-expired", status=400, title="Ticket expired.", detail="The sale period for this ticket has ended.")

    @staticmethod
    def TicketSoldOut():
        return CustomException(type="tickets/info/sold-out", status=400, title="Ticket sold out.", detail="The ticket is sold out and no longer available.")

    @staticmethod
    def TicketNotEnough():
        return CustomException(type="tickets/info/not-enough", status=400, title="Not enough tickets.", detail="The available ticket quantity is less than the requested quantity.")

    @staticmethod
    def InvalidMiniumQuantity():
        return CustomException(
            type="tickets/info/invalid-min-quantity", status=400, title="Invalid minimum quantity.", detail="The requested quantity is less than the minimum quantity allowed per user."
        )

    @staticmethod
    def InvalidMaximumQuantity():
        return CustomException(
            type="tickets/info/invalid-max-quantity", status=400, title="Invalid maximum quantity.", detail="The requested quantity exceeds the maximum quantity allowed per user."
        )

    @staticmethod
    def InvalidCalculatePrice():
        return CustomException(type="tickets/info/invalid-price", status=400, title="Invalid price.", detail="The ticket price does not match the provided price.")
