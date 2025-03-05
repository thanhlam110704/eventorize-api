import pytest
from auth.services import AuthenticationServices


@pytest.fixture(scope="module")
def auth_service():
    return AuthenticationServices(service_name="authentication")


def test_exact_path_match(auth_service):
    assert auth_service.is_path_matching_pattern("/v1/events", "/v1/events") is True


def test_dynamic_segment_match(auth_service):
    assert auth_service.is_path_matching_pattern("/v1/events/{_id}", "/v1/events/12345") is True


def test_path_with_different_lengths(auth_service):
    assert auth_service.is_path_matching_pattern("/v1/events", "/v1/events/12345") is False


def test_mismatched_segments(auth_service):
    assert auth_service.is_path_matching_pattern("/v1/events/{_id}", "/v1/users/12345") is False


def test_multiple_dynamic_segments(auth_service):
    assert auth_service.is_path_matching_pattern("/v1/events/{event_id}/users/{user_id}", "/v1/events/12345/users/67890") is True


def test_static_and_dynamic_segments(auth_service):
    assert auth_service.is_path_matching_pattern("/v1/events/{event_id}/details", "/v1/events/12345/details") is True
