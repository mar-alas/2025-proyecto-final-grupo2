import pytest
from unittest.mock import MagicMock

def ping(api_client):
    return api_client.get("/ping")


def test_ping():
    mock_api_client = MagicMock()
    mock_api_client.get.return_value = {"message": "Success"}

    response = ping(mock_api_client)

    assert response == {"message": "Success"}
    mock_api_client.get.assert_called_once_with("/ping")