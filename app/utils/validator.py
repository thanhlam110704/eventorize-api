import re
from datetime import datetime
from bson import ObjectId

from .value import DataFormat


def check_object_id(_id: str) -> bool:
    """
    Checks if a given string is a valid ObjectId.

    Args:
        _id (str): The string to check.

    Returns:
        is_valid (bool): True if the string is a valid ObjectId, False otherwise.
    """
    if ObjectId.is_valid(_id):
        return True
    return False


def check_email(email):
    """
    Checks if a given string is a valid email address based on the defined regex pattern.

    Args:
        email (str): The email address to check.

    Returns:
        is_valid (bool): True if the email matches the regex pattern, False otherwise.
    """
    pattern = DataFormat.EMAIL_REGEX.value
    if re.match(pattern, email):
        return True
    return False


def check_phone(phone):
    """
    Checks if a given string is a valid phone number based on the defined regex pattern.

    Args:
        phone (str): The phone number to check.

    Returns:
        is_valid (bool): True if the phone number matches the regex pattern, False otherwise.
    """
    pattern = DataFormat.PHONE_REGEX.value
    if re.match(pattern, phone):
        return True
    return False

def is_expired(expiry_time: datetime) -> bool:
    """
    Check if an OTP has expired by comparing with current time.

    Args:
        expiry_time (Optional[datetime]): The expiry timestamp of the OTP.
            If None, considers the OTP as expired.

    Returns:
        bool: True if OTP has expired or expiry_time is None, False otherwise.
    """
    current_time = datetime.now()
    return current_time > expiry_time
