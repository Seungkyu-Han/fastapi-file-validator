from typing import Any

import pytest
from fastapi import HTTPException, status
from unittest.mock import Mock

from file_validator import file_extension_validator


@file_extension_validator(
    file_arg_name="file",
    file_extensions={"jpg", "png"},
)
async def dummy_endpoint(file: Any):
    return "success"


@pytest.mark.asyncio
async def test_file_extension_validator_success():
    # given
    mocked_file = Mock()
    mocked_file.filename = "image.png"

    # when
    result = await dummy_endpoint(file=mocked_file)

    # then
    assert result == "success"


@pytest.mark.asyncio
async def test_file_extension_validator_case_insensitive():
    # given
    mocked_file = Mock()
    mocked_file.filename = "IMAGE.JPG"

    # when
    result = await dummy_endpoint(file=mocked_file)

    # then
    assert result == "success"


@pytest.mark.asyncio
async def test_file_extension_validator_empty_filename():
    # given
    mocked_file = Mock()
    mocked_file.filename = ""

    # when
    with pytest.raises(HTTPException) as exc_info:
        await dummy_endpoint(file=mocked_file)

    # then
    assert exc_info.value.status_code == status.HTTP_400_BAD_REQUEST
    assert exc_info.value.detail == "filename is empty"


@pytest.mark.asyncio
async def test_file_extension_validator_unsupported_type():
    # given
    mocked_file = Mock()
    mocked_file.filename = "document.pdf"

    # when
    with pytest.raises(HTTPException) as exc_info:
        await dummy_endpoint(file=mocked_file)

    # then
    assert exc_info.value.status_code == status.HTTP_415_UNSUPPORTED_MEDIA_TYPE
    assert exc_info.value.detail == "pdf type is unavailable"
