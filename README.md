# FastAPI File Validator

A simple, lightweight, and flexible decorator-based file validation library for FastAPI. Easily validate uploaded file extensions and file sizes before hitting your endpoint logic.

[![PyPI version](https://img.shields.io/pypi/v/fastapi-file-validator)](https://pypi.org/project/fastapi-file-validator/)
[![codecov](https://codecov.io/gh/Seungkyu-Han/fastapi-file-validator/graph/badge.svg?token=VQMH5631MD)](https://codecov.io/gh/Seungkyu-Han/fastapi-file-validator)
[![PyPI downloads](https://img.shields.io/pypi/dm/fastapi-file-validator)](https://pypi.org/project/fastapi-file-validator/)
[![license](https://img.shields.io/pypi/l/fastapi-file-validator)](https://pypi.org/project/fastapi-file-validator/)



---

## 🚀 Installation

Install via pip:

```bash
pip install fastapi-file-validator

```

Or install locally for development:

```bash
pip install -e .

```

---

## 📦 Usage

### 1. Validate File Extension

Ensure that the uploaded file matches specific allowed extensions. If the extension is invalid or missing, it automatically raises an `HTTP 415 Unsupported Media Type` or `HTTP 400 Bad Request`.

```python
from fastapi import FastAPI, UploadFile, File
from file_validator import file_extension_validator

app = FastAPI()

@app.post("/upload/image")
@file_extension_validator(file_arg_name="file", file_extensions={"jpg", "jpeg", "png"})
async def upload_image(file: UploadFile = File(...)):
    return {"filename": file.filename, "message": "Extension validated successfully!"}

```

---

### 2. Validate File Size

Restrict the maximum size of an uploaded file in Megabytes (MB). If the file exceeds the limit, it automatically raises an `HTTP 413 Content Too Large`.

```python
from fastapi import FastAPI, UploadFile, File
from file_validator import file_size_validator

app = FastAPI()

@app.post("/upload/large-file")
@file_size_validator(file_arg_name="file", max_size_mb=10)  # Limit to 10MB
async def upload_large_file(file: UploadFile = File(...)):
    return {"size": file.size, "message": "Size validated successfully!"}

```

---

## ⚙️ Configuration

### Exception Handling

The decorators raise standard FastAPI `HTTPException`s. You can expect the following responses when validation fails:

| Validator | Scenario | HTTP Status | Detail Message Example |
| --- | --- | --- | --- |
| `file_extension_validator` | Filename is empty | `400 Bad Request` | `"filename is empty"` |
| `file_extension_validator` | Invalid extension | `415 Unsupported Media Type` | `"exe type is unavailable"` |
| `file_size_validator` | File exceeds max size | `413 Content Too Large` | `"file size is bigger than 5MB"` |

---

## 📄 License

MIT License
