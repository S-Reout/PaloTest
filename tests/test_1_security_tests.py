import pytest
from utils import get_players


@pytest.mark.parametrize("headers_data, is_negative, expected_status_code, expected_reason", [
    pytest.param(None, False, 200, "OK"),  # pass
    pytest.param({"username": "baduser", "password": "badpass"}, False, 401, "Unauthorized"),  # pass
    pytest.param({"password": "badpass"}, False, 401, "Unauthorized"),  # fails - bug #1
    pytest.param({"username": "baduser"}, False, 401, "Unauthorized"),  # fails  - bug #2
    pytest.param({'Authorization': 'bad token'}, True, 401, "Unauthorized"),  # pass
    pytest.param({'Authorization': ''}, True, 401, "Unauthorized"),  # pass
    pytest.param({'some_key': 'some_value'}, True, 401, "Unauthorized"),  # pass
    pytest.param({}, True, 401, "Unauthorized"),  # pass
])
def test_get_players_authorization(headers_data, is_negative, expected_status_code, expected_reason):
    """
    Test validates the basic authorization header using different headers and different credentials.
    Asserts a valid header with correct credentials is successful (200).
    Asserts a valid header with incorrect credentials or an invalid header fails authorization (401).
    """

    response = get_players(page_num=1, headers_data=headers_data, is_negative=is_negative)

    assert response.status_code == expected_status_code, \
        f'Expected status_code: {expected_status_code}, but instead got: {response.status_code}'

    assert response.reason == expected_reason, \
        f'Expected reason in response to be: {expected_reason}, but instead got: {response.reason}'


