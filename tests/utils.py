import json
from base64 import b64encode
from json import JSONDecodeError
import requests
import os

BASE_URL = os.environ.get('BASE_URL')
DEFAULT_USER = os.environ.get('DEFAULT_USER')
DEFAULT_PASS = os.environ.get('DEFAULT_PASS')


def create_headers(headers_data=None, is_negative=False):
    """
    Helper method to create header for the HTTP request.
    Per "headers_data" dict - create authorization token from "username" and "password",
    If they are not given (negative tests), insert the header_data as header.
    Returns the constructed header dict.
    """

    if headers_data is None:
        headers_data = {}
    if is_negative:
        headers = headers_data
    else:
        username = headers_data.get("username", DEFAULT_USER)
        password = headers_data.get("password", DEFAULT_PASS)
        token = create_basic_auth_token(username, password)
        headers = {'Authorization': token}

    return headers


def create_basic_auth_token(username, password):
    """
    Helper method to create a basic authentication token from "username" and "password".
    Returns token string
    """

    token = b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
    return f'Basic {token}'


def make_api_request(method, full_path, headers, body=None):
    """
    Helper method to send API HTTP request per method (get/put/delete/post),
    using the path provided, headers provided, and body (if necessary).
    Returns the HTTP response object
    """

    if method == 'get':
        response = requests.get(full_path, headers=headers)
    elif method == 'put':
        response = requests.put(full_path, data=body, headers=headers)
    elif method == 'delete':
        response = requests.delete(full_path, data=body, headers=headers)
    else:  # post
        response = requests.post(full_path, data=body, headers=headers)
    return response


def get_players(headers_data=None, page_num=None, is_negative=False):
    """
    Helper method to send GET API request to the specific '/players' endpoint,
    with or without page parameter given, and relevant headers.
    Returns the HTTP response object
    """

    headers = create_headers(headers_data, is_negative=is_negative)
    if page_num == "no_params":
        path = BASE_URL + f'/players'
    else:
        path = BASE_URL + f'/players?page={str(page_num)}'
    response = make_api_request(method='get', full_path=path, headers=headers)
    return response


def convert_response_content_to_json(response_obj):
    """
    Helper method to convert the 'content' text string from the HTTP response object, to JSON format.
    Returns the response JSON, or an invalid message if it can't be decoded.
    """

    decoded_response = response_obj.content.decode('utf-8')
    try:
        json_response = json.loads(decoded_response)
    except JSONDecodeError:
        json_response = f"Invalid JSON returned"

    return json_response

