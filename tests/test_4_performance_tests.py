from threading import Thread
import pytest
from datetime import datetime
from utils import get_players


@pytest.mark.first
def test_get_players_response_time_per_page(num_of_requests=200):
    """
    Test sends requests to the server for all page param values (up until "num_of_requests"),
    and calculates for each request how long (in seconds & milliseconds) it took to get a response.
    It prints all the times, and then the average time for all the requests.
    Test will fail if a request takes longer than 1 second to get a response.
    """

    milliseconds_list = []
    error_list = []
    for i in range(1, num_of_requests+1):

        before_timestamp = datetime.now()
        response = get_players(page_num=i)
        after_timestamp = datetime.now()
        delta = after_timestamp - before_timestamp
        seconds_time_diff = delta.total_seconds()
        seconds_time_diff = round(seconds_time_diff, ndigits=4)
        milliseconds_time_diff = round(seconds_time_diff * 1000, ndigits=4)
        print(f"\nFor page {i} - Got a response in: {milliseconds_time_diff} milliseconds (or {seconds_time_diff} seconds).")
        milliseconds_list.append(milliseconds_time_diff)
        if seconds_time_diff > 1:
            error_list.append(f'\nFor page {i} - Expected response in less than 1 second. Got it after {seconds_time_diff} seconds')

    average_time = round(sum(milliseconds_list) / num_of_requests, ndigits=4)
    print(f"\nAverage response time for {num_of_requests} requests is: {average_time} milliseconds.")

    assert not error_list, f'\n{error_list}'


@pytest.mark.second
def test_get_players_response_time_for_same_page(num_of_requests=200):
    """
    Test sends requests to the server for same page param value (up until "num_of_requests"),
    and calculates for each request how long (in seconds & milliseconds) it took to get a response.
    It prints all the times, and then prints the average time for all the requests.
    Test will fail if a request takes longer than 1 second to get a response.
    """

    milliseconds_list = []
    error_list = []
    for i in range(1, num_of_requests+1):

        before_timestamp = datetime.now()
        response = get_players(page_num=1)
        after_timestamp = datetime.now()
        delta = after_timestamp - before_timestamp
        seconds_time_diff = delta.total_seconds()
        seconds_time_diff = round(seconds_time_diff, ndigits=4)
        milliseconds_time_diff = round(seconds_time_diff * 1000, ndigits=4)
        print(
            f"\nGot a response in: {milliseconds_time_diff} milliseconds (or {seconds_time_diff} seconds).")
        milliseconds_list.append(milliseconds_time_diff)
        if seconds_time_diff > 1:
            error_list.append(
                f'\nExpected response in less than 1 second. Got it after {seconds_time_diff} seconds')

    average_time = round(sum(milliseconds_list) / num_of_requests, ndigits=4)
    print(f"\nAverage response time for {num_of_requests} requests is: {average_time} milliseconds.")

    assert not error_list, f'\n{error_list}'


@pytest.mark.last  # test should run last as it currently crashes the app
def test_get_players_multiple_threads(num_of_requests=10, num_of_threads=10):
    """
    Test sends requests to the server (per "num_of_requests"), in parallel multiple threads (per "num_of_threads").
    Asserts all responses are successful (200).
    """

    responses_list = []
    threads = []
    fail_count = 0
    before_timestamp = datetime.now()

    for i in range(num_of_requests):
        for j in range(num_of_threads):
            thread = Thread(target=lambda: responses_list.append(get_players(page_num=1)))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

    after_timestamp = datetime.now()

    for response in responses_list:
        if response.status_code != 200:
            fail_count += 1

    assert fail_count == 0, f'Expected all requests to succeed. {fail_count} out of {num_of_requests} failed'
    print(f"\nAll {num_of_requests} requests were successful.\n"
          f"Started at: {before_timestamp}\n"
          f"Finished at: {after_timestamp}")


