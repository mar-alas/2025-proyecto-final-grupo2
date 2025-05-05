import pytest
from io import StringIO
from unittest.mock import patch, Mock
from infraestructura.file_downloader import download_file_from_url

@patch("infraestructura.file_downloader.requests.get")
def test_download_file_success(mock_get):
    # Simula una respuesta exitosa
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "col1,col2\nval1,val2"
    mock_response.raise_for_status = Mock()

    mock_get.return_value = mock_response

    result = download_file_from_url("https://storage.googleapis.com/ccp-app-images/test.csv")

    assert isinstance(result, StringIO)
    assert result.getvalue() == "col1,col2\nval1,val2"

@patch("infraestructura.file_downloader.requests.get")
def test_download_file_failure(mock_get):
    # Simula un error en la petición
    mock_get.side_effect = Exception("No se pudo descargar el archivo.")

    with pytest.raises(Exception) as exc_info:
        download_file_from_url("https://storage.googleapis.com/ccp-app-images/test.csv")

    assert "No se pudo descargar el archivo." in str(exc_info.value)


@patch("infraestructura.file_downloader.requests.get")
def test_download_file_request_exception(mock_get):
    from requests.exceptions import HTTPError

    mock_get.side_effect = HTTPError("Error HTTP")

    with pytest.raises(Exception) as exc_info:
        download_file_from_url("https://storage.googleapis.com/ccp-app-images/test.csv")

    assert "No se pudo descargar el archivo." in str(exc_info.value)
