import random
import string
import uuid
from datetime import datetime
from enum import Enum

class UserRoles(Enum):
    USER = "user"
    ADMIN = "admin"
    
class OrderBy(Enum):
    DECREASE = "desc"
    ASCENDING = "asc"
    
class DataFormat(Enum):
    DATE = r"%Y-%m-%d"
    DATE_TIME = r"%Y-%m-%d %H:%M:%S"
    EMAIL_REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,10}\b"
    PHONE_REGEX = r"^\d{10}$"

def generate_numeric_code(length: int = 8) -> str:
    """
    Generate a random numeric code consisting of digits (0-9).
    The code can start with the digit 0.

    Args:
        length (int): Length of the numeric code. Default is 8.

    Returns:
        str: Generated numeric code as a string.
    """
    if length < 1:
        raise ValueError("Length must be at least 1.")

    # Define character set (digits 0-9)
    digits = string.digits

    # Generate the numeric code
    numeric_code = "".join(random.choices(digits, k=length))
    return numeric_code


def get_current_date_time_by_format(format: str) -> str:
    """
    Returns the current date and/or time as a string based on the specified format.

    Args:
        format (str): A datetime format string (e.g., "%m/%Y", "%Y-%m-%d %H:%M:%S").

    Returns:
        str: The current date and/or time formatted as specified.

    Example Formats:
        - "%m/%Y" -> "01/2025"
        - "%Y-%m-%d" -> "2025-01-21"
        - "%H:%M:%S" -> "15:30:45"
        - "%d-%b-%Y %I:%M %p" -> "21-Jan-2025 03:30 PM"
    """
    try:
        return datetime.now().strftime(format)
    except ValueError as e:
        raise ValueError(f"Invalid datetime format: {format}. Error: {str(e)}")


def generate_uuid() -> str:
    """
    Generate a UUID4 string.

    Returns:
        str: A UUID4 string.
    """
    return str(uuid.uuid4())