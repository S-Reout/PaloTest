import pytest
from datetime import datetime
from utils import get_players


def test_get_players_stress(num_of_requests=5000):
    """
    Test sends many consecutive requests to the server (per "num_of_requests"),
    and asserts all responses were successful (200). Also prints timestamps of start and finish.
    """

    responses_list = []
    fail_count = 0
    before_timestamp = datetime.now()
    for i in range(num_of_requests):
        response = get_players(page_num=1)
        responses_list.append(response)
    after_timestamp = datetime.now()

    for response in responses_list:
        if response.status_code != 200:
            fail_count += 1

    assert fail_count == 0, f'Expected all requests to succeed. {fail_count} out of {num_of_requests} failed'
    print(f"\nAll {num_of_requests} requests were successful.\n"
          f"Started at: {before_timestamp}\n"
          f"Finished at: {after_timestamp}")


def test_get_players_performance(num_of_requests=10):
    """
    Test sends several requests to the server (per "num_of_requests"),
    and calculates for each request how long (in seconds & milliseconds) it took to get a response.
    It prints all the times, and then prints the average time for all the requests.
    """

    milliseconds_list = []
    for i in range(num_of_requests):

        before_timestamp = datetime.now()
        response = get_players(page_num=1)
        after_timestamp = datetime.now()
        delta = after_timestamp - before_timestamp
        seconds_time_diff = delta.total_seconds()
        milliseconds_time_diff = round(seconds_time_diff * 1000, ndigits=4)

        assert seconds_time_diff < 1, f'Expected response in less than 1 second. Got it after {seconds_time_diff} seconds.'
        print(f"\nFor request number {i+1} - Got a response in: {milliseconds_time_diff} milliseconds (or {seconds_time_diff} seconds).")
        milliseconds_list.append(milliseconds_time_diff)

    average_time = round(sum(milliseconds_list) / num_of_requests, ndigits=4)
    print(f"\nAvergare response time for {num_of_requests} requests is: {average_time} milliseconds.")


