import re
from typing import Annotated

from pydantic.functional_validators import AfterValidator

from .exceptions import ErrorCode as PermissionErrorCode


def check_scope_format(scope: str) -> str:
    """
    Checks if the input string is in the format 'module.action'.

    This function verifies whether a given string follows the pattern where
    two sequences of alphanumeric characters are separated by a colon (.).
    Each sequence must contain at least one character.

    Args:
        s (str): The input string to check.

    Returns:
        str: The input string if the string matches the format 'module.action', Error otherwise.
    """
    pattern = r"^\w+\.\w+$"
    is_valid = bool(re.match(pattern, scope))
    if not is_valid:
        raise PermissionErrorCode.InvalidScopeFormat(scope=scope)
    return scope


ScopeStr = Annotated[str, AfterValidator(check_scope_format)]


def check_api_path_format(path: str) -> str:
    """
    Checks if the input API path follows the format '/vX/module/...', where X is an integer,
    followed by any number of sub-paths, but the path must not end with a trailing slash.

    Args:
        path (str): The API path to check.

    Returns:
        str: The input string if the path matches the format '/vX/module/...', False otherwise.
    """
    pattern = r"^/v\d+/[^/]+(?:/[^/]+)*$"
    is_valid = bool(re.match(pattern, path))
    if not is_valid:
        raise PermissionErrorCode.InvalidApiPathFormat(path=path)
    return path


ApiPathStr = Annotated[str, AfterValidator(check_api_path_format)]
