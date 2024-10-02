# Doctly

Doctly is a Python client library that provides a simple way to interact with the Doctly backend API. With Doctly, you can effortlessly upload PDF documents, convert them to Markdown, and retrieve the converted files—all with just a few lines of code.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Convert PDF to Markdown](#convert-pdf-to-markdown)
  - [Customizing Polling Parameters](#customizing-polling-parameters)
  - [Error Handling](#error-handling)
- [API Reference](#api-reference)
  - [`Client` Class](#client-class)
  - [`DoctlyError` Exception](#doctlyerror-exception)
- [Contributing](#contributing)
- [Contact](#contact)

## Installation

Doctly can be easily installed using `pip`. Run the following command in your terminal:

```bash
pip install doctly
```

## Quick Start

Here's a quick example to get you started with Doctly:

```python
import doctly

# Initialize the Doctly client with your API key
client = doctly.Client(api_key='YOUR_API_KEY')

# Convert a PDF file to Markdown
try:
    markdown_content = client.to_markdown('path/to/your/file.pdf')
    
    # Save the Markdown content to a file
    with open('output.md', 'w') as f:
        f.write(markdown_content)
    
    print("Conversion successful! Markdown file saved as 'output.md'")
except doctly.DoctlyError as e:
    print(f"An error occurred: {e}")
```

## Usage

### Initialization

To begin using Doctly, initialize the `Client` class with your API key:

```python
import doctly

# Replace 'YOUR_API_KEY' with your actual API key
client = doctly.Client(api_key='YOUR_API_KEY')
```

### Convert PDF to Markdown

The primary functionality of Doctly is to upload a PDF file, convert it to Markdown, and retrieve the converted content. Here's how to do it:

```python
try:
    markdown_content = client.to_markdown('path/to/your/file.pdf')
    
    # Optional: Save the Markdown content to a file
    with open('output.md', 'w') as f:
        f.write(markdown_content)
    
    print("Conversion successful!")
except doctly.DoctlyError as e:
    print(f"An error occurred: {e}")
```

### Customizing Polling Parameters

Doctly handles the asynchronous nature of the backend API by polling the document status. You can customize the polling interval (`wait_time`) and the maximum waiting duration (`timeout`) as needed:

```python
markdown_content = client.to_markdown(
    'path/to/your/file.pdf',
    wait_time=10,  # Time in seconds between each status check
    timeout=600     # Maximum time in seconds to wait for processing
)
```

### Error Handling

Errors are handled with the `DoctlyError` exception. Catch this exception to handle any issues that arise during the upload, conversion, or download processes:

```python
try:
    markdown_content = client.to_markdown('file.pdf')
except doctly.DoctlyError as e:
    print(f"Error: {e}")
    # Additional error handling logic
```

## API Reference

### `Client` Class

The `Client` class encapsulates all interactions with the Doctly backend API.

#### `__init__(api_key: str)`

- **Description**: Initializes the Doctly client with the provided API key and optional base URL.
- **Parameters**:
  - `api_key` (str): Your Doctly API key.
- **Example**:

  ```python
  client = doctly.Client(api_key='YOUR_API_KEY')
  ```

#### `to_markdown(file_path: str, wait_time: int = 5, timeout: int = 300) -> str`

- **Description**: Uploads a PDF file to the backend, polls for processing status, and returns the converted Markdown content.
- **Parameters**:
  - `file_path` (str): Path to the PDF file to upload.
  - `wait_time` (int, optional): Time in seconds between each status check. Defaults to `5` seconds.
  - `timeout` (int, optional): Maximum time in seconds to wait for processing. Defaults to `300` seconds (5 minutes).
- **Returns**:
  - `markdown_content` (str): The content of the converted Markdown file.
- **Raises**:
  - `DoctlyError`: If there's an error during upload, processing, or download.
- **Example**:

  ```python
  markdown = client.to_markdown('document.pdf')
  ```

### `DoctlyError` Exception

A custom exception class for handling errors specific to the Doctly library.

#### Example Usage

```python
try:
    markdown_content = client.to_markdown('file.pdf')
except doctly.DoctlyError as e:
    print(f"Doctly encountered an error: {e}")
```

## Contributing

Contributions are welcome! To contribute to Doctly, please follow these steps:
Please ensure that your code follows the project's coding standards and includes relevant tests.

## Contact

For any questions, issues, or feature requests, please open an issue on [GitHub](https://github.com/doctly/doctly/issues)