# Doctly

Doctly is a Python client library that provides a simple way to interact with the Doctly backend API. With Doctly, you can effortlessly upload PDF documents, process them to Markdown, and retrieve the converted content—all with just a few lines of code.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [Initialization](#initialization)
  - [Process PDF Documents](#process-pdf-documents)
  - [Customizing Polling Parameters](#customizing-polling-parameters)
  - [Accuracy Levels](#accuracy-levels)
  - [Error Handling](#error-handling)
- [API Reference](#api-reference)
  - [`Client` Class](#client-class)
  - [`Accuracy` Enum](#accuracy-enum)
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

# Process a PDF file
try:
    content = client.process('path/to/your/file.pdf')
    
    # Save the processed content to a file
    with open('output.md', 'w') as f:
        f.write(content)
    
    print("Processing successful! Content saved as 'output.md'")
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

### Process PDF Documents

The primary functionality of Doctly is to upload a PDF file, process it, and retrieve the converted content. Here's how to do it:

```python
try:
    content = client.process('path/to/your/file.pdf')
    
    # Optional: Save the content to a file
    with open('output.md', 'w') as f:
        f.write(content)
    
    print("Processing successful!")
except doctly.DoctlyError as e:
    print(f"An error occurred: {e}")
```

### Customizing Polling Parameters

Doctly handles the asynchronous nature of the backend API by polling the document status. You can customize the polling interval (`wait_time`) and the maximum waiting duration (`timeout`) as needed:

```python
content = client.process(
    'path/to/your/file.pdf',
    wait_time=10,  # Time in seconds between each status check
    timeout=600    # Maximum time in seconds to wait for processing
)
```

### Accuracy Levels

Doctly supports different accuracy levels for processing documents. You can specify the accuracy level using the `accuracy` parameter:

```python
from doctly import Accuracy

# Process with LITE accuracy (faster, default)
content_lite = client.process('path/to/your/file.pdf', accuracy=Accuracy.LITE)

# Process with Precistion ULTRA accuracy (more accurate but slower)
content_ultra = client.process('path/to/your/file.pdf', accuracy=Accuracy.ULTRA)
```

### Error Handling

Errors are handled with the `DoctlyError` exception. Catch this exception to handle any issues that arise during the upload, processing, or download processes:

```python
try:
    content = client.process('file.pdf')
except doctly.DoctlyError as e:
    print(f"Error: {e}")
    # Additional error handling logic
```

## API Reference

### `Client` Class

The `Client` class encapsulates all interactions with the Doctly backend API.

#### `__init__(api_key: str, base_url: str = "https://api.doctly.ai")`

- **Description**: Initializes the Doctly client with the provided API key and optional base URL.
- **Parameters**:
  - `api_key` (str): Your Doctly API key.
  - `base_url` (str, optional): The base URL for the Doctly API. Defaults to "https://api.doctly.ai".
- **Example**:

  ```python
  client = doctly.Client(api_key='YOUR_API_KEY')
  ```

#### `process(file_path: str, accuracy: Accuracy = Accuracy.LITE, wait_time: int = 5, timeout: int = 300, **kwargs) -> str`

- **Description**: Uploads a PDF file to the backend, polls for processing status, and returns the processed content.
- **Parameters**:
  - `file_path` (str): Path to the PDF file to upload.
  - `accuracy` (Accuracy, optional): Processing accuracy level (LITE or ULTRA). Defaults to `Accuracy.LITE`.
  - `wait_time` (int, optional): Time in seconds between each status check. Defaults to `5` seconds.
  - `timeout` (int, optional): Maximum time in seconds to wait for processing. Defaults to `300` seconds (5 minutes).
  - `**kwargs`: Additional parameters for future extensions.
- **Returns**:
  - `content` (str): The processed content.
- **Raises**:
  - `DoctlyError`: If there's an error during upload, processing, or download.
- **Example**:

  ```python
  content = client.process('document.pdf', accuracy=Accuracy.ULTRA)
  ```

### `Accuracy` Enum

An enumeration that defines the available accuracy levels for document processing.

- `Accuracy.LITE`: Precision - Faster processing with great accuracy.
- `Accuracy.ULTRA`: Precision Ultra - Extremly good accuracy, but may take longer. This process generates multiple versions for each page, picking the highest accuracy one.

#### Example Usage

```python
from doctly import Accuracy

# Process with ULTRA accuracy
content = client.process('file.pdf', accuracy=Accuracy.ULTRA)
```

### `DoctlyError` Exception

A custom exception class for handling errors specific to the Doctly library.

#### Example Usage

```python
try:
    content = client.process('file.pdf')
except doctly.DoctlyError as e:
    print(f"Doctly encountered an error: {e}")
```

## Contributing

Contributions are welcome! To contribute to Doctly, please follow these steps:
Please ensure that your code follows the project's coding standards and includes relevant tests.

## Contact

For any questions, issues, or feature requests, please open an issue on [GitHub](https://github.com/doctly/doctly/issues)