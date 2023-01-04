import json

import pytest

import exceptions
from services.api.response import safely_decode_response_json, raise_for_unexpected_status_code


@pytest.fixture
def mock_error_response():
    class MockResponse:
        def json(self):
            raise json.JSONDecodeError('msg', 'doc', 1)

    return MockResponse()


@pytest.fixture
def mock_success_response():
    class MockResponse:
        def json(self):
            return {'hello': 'world'}

    return MockResponse()


def test_response_json_unsuccessfully_decoding(mock_error_response):
    with pytest.raises(exceptions.ServerAPIError) as error:
        safely_decode_response_json(mock_error_response)
    assert error.value.args[0] == 'Unable to parse response JSON'


def test_response_json_successfully_decoding(mock_success_response):
    assert safely_decode_response_json(mock_success_response) == {'hello': 'world'}


@pytest.mark.parametrize(
    'status_code',
    [200, 400, 404, 500],
)
def test_raise_for_unexpected_status_code(status_code):
    with pytest.raises(exceptions.ServerAPIError) as error:
        raise_for_unexpected_status_code(status_code)
    assert error.value.args[0] == f'Unexpected status code "{status_code}"'
