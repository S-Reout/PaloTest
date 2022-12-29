import pytest
from utils import get_players, convert_response_content_to_json


@pytest.mark.parametrize("page_num", [
    pytest.param(1),  # fails - bug #5
    pytest.param(5),  # fails - bug #5
])
def test_get_players_validate_data_consistency(page_num):
    """
    Test checks that when entering the same request with same page parameter, the data returned is the same.
    If the data is different for identical requests, data is not consistent.
    """

    response1 = get_players(page_num=page_num)
    assert response1.status_code == 200, \
        f'Expected status_code: 200, but instead got: {response1.status_code}'
    content1 = convert_response_content_to_json(response1)

    response2 = get_players(page_num=page_num)
    assert response2.status_code == 200, \
        f'Expected status_code: 200, but instead got: {response2.status_code}'
    content2 = convert_response_content_to_json(response2)

    assert content1 == content2, f'Data retrieved for same page request is inconsistent.\n' \
                                 f'Expected first response content to be the same as second response content.\n' \
                                 f'Expected (first response): {content1}\n' \
                                 f'Actual (second response): {content2}'


@pytest.mark.parametrize("page_num", [
    pytest.param("2"),  # fails - bug #7
    pytest.param("13"),  # fails - bug #7
])
def test_get_players_validate_amount_of_records(page_num):
    """
    Test asserts that each page request brings the indented amount of entries (50)
    """

    response = get_players(page_num=page_num)
    assert response.status_code == 200, \
        f'Expected status_code: 200, but instead got: {response.status_code}'
    content = convert_response_content_to_json(response)

    assert len(content) == 50, f"Expected 50 items to be returned for each page, instead got: {len(content)}"


@pytest.mark.parametrize("page_num", [
    pytest.param(1),  # pass
    pytest.param(5),  # pass
    pytest.param(12),  # pass
    pytest.param(30),  # fails since data ends on certain page number - bug #8
    pytest.param(84),  # fails since data ends on certain page number - bug #8
])
def test_get_players_validate_ids_in_pages(page_num):
    """
    Test asserts that for each page , the IDs of the records start at the expected ID.
    If not - prints that the page data doesn't exist (page number too high)
    If yes - asserts that all the IDs in the page are as expected (incrementing by 1)
    """

    response = get_players(page_num=page_num)
    assert response.status_code == 200, \
        f'Expected status_code: 200, but instead got: {response.status_code}'
    content = convert_response_content_to_json(response)

    first_id = 0 if page_num == "1" else (page_num - 1) * 50
    id_counter = first_id
    error_list = []

    assert content[0]['ID'] == first_id, f"\nExpected for page {page_num}, that the first ID would be: " \
                                         f"{first_id}, but got ID: {content[0]['ID']}. " \
                                         f"\nPage {page_num} doesn't exist. Data ends on page {page_num - 1}, " \
                                         f"so results returned for page 1. " \
                                         f"\nPage parameter should be higher."
    for player in content:
        if player['ID'] != id_counter:
            error_list.append(f"\nExpected ID to be: {id_counter} but got ID: {player['ID']}")
        id_counter += 1

    assert not error_list, f"{error_list}"


def test_get_players_validate_end_of_pages(check_pages=500):  # fails since data ends on certain page number - bug #8
    """
    Test asserts that using all possible valid values of the page parameter (up to 'check_pages')
    returns a valid page. If not, it means we've reached the final page, and the page beyond it doesn't exist.
    """

    for page_num in range(1, check_pages):
        response = get_players(page_num=page_num)
        assert response.status_code == 200, \
            f'Expected status_code: 200, but instead got: {response.status_code}'
        content = convert_response_content_to_json(response)
        first_id = 0 if page_num == 1 else (page_num - 1) * 50
        assert content[0]['ID'] == first_id, f"\nExpected for page {page_num}, that the first ID would be: " \
                                             f"{first_id}, but got ID: {content[0]['ID']}. " \
                                             f"\nPage {page_num} doesn't exist. Data ends on page {page_num - 1}, " \
                                             f"so results returned for page 1. " \
                                             f"\nPage parameter should be higher."


@pytest.mark.parametrize("page_num, expected_status_code", [
    pytest.param("1", 200),  # fails for invalid data - bug #9
    pytest.param("9", 200),  # fails for invalid data - bug #9
    pytest.param("10", 200),  # fails for invalid data - bug #9
])
def test_get_players_validate_names(page_num, expected_status_code):
    """
    Test asserts that for every page returned, each player record with an ID also has a name value.
    If not, it prints a list of all players that are missing a name (by their ID).
    """

    response = get_players(page_num=page_num)

    assert response.status_code == expected_status_code, \
        f'Expected status_code: {expected_status_code}, but instead got: {response.status_code}'

    content = convert_response_content_to_json(response)

    ids_with_missing_names = []

    for player in content:
        if player["Name"] in ["", "null"]:
            ids_with_missing_names.append(player["ID"])

    assert not ids_with_missing_names, f"\nThe page content has missing data.\n" \
                                       f"The following player IDs do not have a Name value: {ids_with_missing_names}"



