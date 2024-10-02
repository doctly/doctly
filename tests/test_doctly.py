import pytest
import responses
from unittest.mock import patch

from doctly import Client, DoctlyError

API_BASE_URL = "https://example.com/api/v1/documents/"


@pytest.fixture
def client():
    client = Client(api_key="test_api_key")
    client.base_url = "https://example.com"
    return client


@responses.activate
def test_to_markdown_success(client, tmp_path):
    # Mock the POST upload response
    responses.add(
        responses.POST,
        API_BASE_URL,
        json=[{"id": "12345", "status": "PENDING", "download_url": None}],
        status=200,
    )

    # Mock the GET status polling responses
    # First poll: status PROCESSING
    responses.add(
        responses.GET,
        f"{API_BASE_URL}12345",
        json={"id": "12345", "status": "PROCESSING", "download_url": None},
        status=200,
    )

    # Second poll: status COMPLETED with download_url
    responses.add(
        responses.GET,
        f"{API_BASE_URL}12345",
        json={
            "id": "12345",
            "status": "COMPLETED",
            "download_url": "https://example.com/downloads/12345.md",
        },
        status=200,
    )

    # Mock the GET markdown file download
    responses.add(
        responses.GET,
        "https://example.com/downloads/12345.md",
        body="# Sample Markdown",
        status=200,
    )

    # Path to a temporary PDF file
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    markdown = client.to_markdown(str(pdf_file))
    assert markdown == "# Sample Markdown"


@responses.activate
def test_to_markdown_upload_failure(client, tmp_path):
    # Mock the POST upload response with failure
    responses.add(
        responses.POST,
        API_BASE_URL,
        json={"detail": "File upload failed"},
        status=500
    )

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with pytest.raises(DoctlyError) as exc_info:
        client.to_markdown(str(pdf_file))

    assert "Error uploading file" in str(exc_info.value)


@responses.activate
def test_to_markdown_processing_failed(client, tmp_path):
    # Mock the POST upload response
    responses.add(
        responses.POST,
        API_BASE_URL,
        json=[{"id": "12345", "status": "PENDING", "download_url": None}],
        status=200,
    )

    # Mock the GET status polling response with FAILED status
    responses.add(
        responses.GET,
        f"{API_BASE_URL}12345",
        json={"id": "12345", "status": "FAILED", "download_url": None},
        status=200,
    )

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with pytest.raises(DoctlyError) as exc_info:
        client.to_markdown(str(pdf_file))

    assert "Document processing failed" in str(exc_info.value)


@responses.activate
def test_to_markdown_timeout(client, tmp_path):
    # Mock the POST upload response
    responses.add(
        responses.POST,
        API_BASE_URL,
        json=[{"id": "12345", "status": "PENDING", "download_url": None}],
        status=200,
    )

    # Mock the GET status polling responses always returning PENDING
    for _ in range(10):
        responses.add(
            responses.GET,
            f"{API_BASE_URL}12345",
            json={"id": "12345", "status": "PENDING", "download_url": None},
            status=200,
        )

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with patch("time.sleep", return_value=None):  # mock sleep
        with pytest.raises(DoctlyError) as exc_info:
            client.to_markdown(str(pdf_file), wait_time=0.1, timeout=0.3)

    assert "Processing timeout" in str(exc_info.value)


@responses.activate
def test_to_markdown_no_document_id(client, tmp_path):
    # Mock the POST upload response without 'id'
    responses.add(
        responses.POST,
        API_BASE_URL,
        json=[{"status": "PENDING", "download_url": None}],
        status=200,
    )

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with pytest.raises(DoctlyError) as exc_info:
        client.to_markdown(str(pdf_file))

    assert "No document ID returned from upload." in str(exc_info.value)


@responses.activate
def test_to_markdown_no_download_url(client, tmp_path):
    # Mock the POST upload response
    responses.add(
        responses.POST,
        API_BASE_URL,
        json=[{"id": "12345", "status": "PENDING", "download_url": None}],
        status=200,
    )

    # Mock the GET status polling responses with COMPLETED status but no
    # download_url
    responses.add(
        responses.GET,
        f"{API_BASE_URL}12345",
        json={
            "id": "12345",
            "status": "COMPLETED",
            "download_url": None
        },
        status=200,
    )

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with pytest.raises(DoctlyError) as exc_info:
        client.to_markdown(str(pdf_file))

    assert "No download URL returned from the server." in str(exc_info.value)


@responses.activate
def test_to_markdown_download_failure(client, tmp_path):
    # Mock the POST upload response
    responses.add(
        responses.POST,
        API_BASE_URL,
        json=[{"id": "12345", "status": "PENDING", "download_url": None}],
        status=200,
    )

    # Mock the GET status polling responses with COMPLETED status and
    #  valid download_url
    responses.add(
        responses.GET,
        f"{API_BASE_URL}12345",
        json={
            "id": "12345",
            "status": "COMPLETED",
            "download_url": "https://example.com/downloads/12345.md",
        },
        status=200,
    )

    # Mock the GET markdown file download with failure
    responses.add(
        responses.GET,
        "https://example.com/downloads/12345.md",
        json={"detail": "File not found"},
        status=404,
    )

    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_bytes(b"%PDF-1.4 sample content")

    with pytest.raises(DoctlyError) as exc_info:
        client.to_markdown(str(pdf_file))

    assert "Error downloading Markdown file" in str(exc_info.value)


def test_client_initialization():
    client = Client(api_key="test_api_key")
    assert client.api_key == "test_api_key"
    assert client.headers["Authorization"] == "Bearer test_api_key"
