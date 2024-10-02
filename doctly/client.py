import requests
import time


class DoctlyError(Exception):
    """Custom exception for Doctly errors."""

    pass


class Client:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.doctly.ai"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
        }

    def to_markdown(self, file_path, wait_time=5, timeout=300):
        """
        Uploads a PDF file to the backend, waits for processing, and downloads
        the resulting Markdown content.

        Parameters:
        - file_path (str): Path to the PDF file to upload.
        - wait_time (int): Time in seconds to wait between polling the status.
        - timeout (int): Maximum time in seconds to wait for processing to
        complete.

        Returns:
        - markdown_content (str): The content of the Markdown file.

        Raises:
        - DoctlyError: If there is any error during processing.
        """

        # Endpoint URLs
        upload_url = f"{self.base_url}/api/v1/documents/"

        # Upload the file
        with open(file_path, "rb") as f:
            files = {"files": (file_path, f)}
            response = requests.post(
                upload_url,
                files=files,
                headers=self.headers
            )

        if response.status_code != 200:
            raise DoctlyError(f"Error uploading file: {response.text}")

        # The API returns a list of DocumentPublic objects
        documents = response.json()
        if not documents:
            raise DoctlyError("No document returned from upload.")

        document = documents[0]
        document_id = document.get("id")
        status = document.get("status")

        if not document_id:
            raise DoctlyError("No document ID returned from upload.")

        # Poll for status
        status_url = f"{self.base_url}/api/v1/documents/{document_id}"
        start_time = time.time()

        while status != "COMPLETED":
            if status == "FAILED":
                raise DoctlyError(
                    f"Document processing failed with status: {status}"
                )

            if time.time() - start_time > timeout:
                raise DoctlyError("Processing timeout.")

            time.sleep(wait_time)
            # Get the document status
            response = requests.get(status_url, headers=self.headers)
            if response.status_code != 200:
                raise DoctlyError(f"Error checking status: {response.text}")

            document = response.json()
            status = document.get("status")

        download_url = document.get("download_url")
        if not download_url:
            raise DoctlyError("No download URL returned from the server.")

        # Download the Markdown file
        response = requests.get(download_url)
        if response.status_code != 200:
            raise DoctlyError(
                f"Error downloading Markdown file: {response.text}"
            )

        markdown_content = response.text
        return markdown_content
