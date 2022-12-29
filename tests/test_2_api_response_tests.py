import pytest
from utils import get_players


def test_get_players_validate_content_type():  # fails - bug #3
    """
    Test asserts that the response returns as JSON Content Type.
    """

    response = get_players(page_num=1)

    actual_content_type = response.headers['Content-Type']
    assert actual_content_type == 'application/json', \
        f'Expected Content type in response to be: application/json, but instead got: {actual_content_type}'


@pytest.mark.parametrize("page_num, expected_status_code", [
    pytest.param(1, 200),  # pass
    pytest.param(5, 200),  # pass
    pytest.param(None, 400),  # fails for 418 status - bug #4
    pytest.param(0, 400),  # fails for 418 status - bug #4
    pytest.param("x", 400),  # fails for 418 status - bug #4
    pytest.param("no_params", 400),  # fails for 418 status - bug #4
])
def test_get_players_page_num_param(page_num, expected_status_code):
    """
    Test checks the page parameter with different values (or no value).
    Asserts Valid value (positive number) is successful with expected_status_code (200).
    Asserts Invalid value (zero, character string, None, or no parameter at all) fails with expected_status_code (400).
    """

    response = get_players(page_num=page_num)

    assert response.status_code == expected_status_code, \
        f'Expected status_code: {expected_status_code}, but instead got: {response.status_code}'


@pytest.mark.parametrize("page_num, headers_data, is_negative, expected_error", [
    pytest.param(None, None, False, "Bad Request - missing page number param"),  # wrong error message - bug #5
    pytest.param(1, {'Authorization': 'bad token'}, True, "401 Unauthorized\n"),  # correct error message
])
def test_get_players_error_messages(page_num, headers_data, is_negative, expected_error):
    """
    Test asserts that failed responses (!=200) include the correct error message text.
    """

    response = get_players(page_num=page_num, headers_data=headers_data, is_negative=is_negative)

    assert response.text == expected_error, \
        f'Expected error message in response to be: {expected_error}, but instead got: {response.text}'

