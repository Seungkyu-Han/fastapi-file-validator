from typing import Any

import pytest
from fastapi import HTTPException, status
from unittest.mock import Mock

from file_validator import file_size_validator


@file_size_validator(
    file_arg_name="file",
    max_size_mb=2,
)
async def dummy_endpoint(file: Any):
    return "success"


@pytest.mark.asyncio
async def test_file_size_validator_success():
    # given
    mocked_file = Mock()
    mocked_file.size = 1 * 1024 * 1024

    # when
    result = await dummy_endpoint(file=mocked_file)

    # then
    assert result == "success"


@pytest.mark.asyncio
async def test_file_size_validator_exactly_max_size():
    # given
    mocked_file = Mock()
    mocked_file.size = 2 * 1024 * 1024

    # when
    result = await dummy_endpoint(file=mocked_file)

    # then
    assert result == "success"


@pytest.mark.asyncio
async def test_file_size_validator_too_large():
    # given
    mocked_file = Mock()
    mocked_file.size = int(2.1 * 1024 * 1024)

    # when
    with pytest.raises(HTTPException) as exc_info:
        await dummy_endpoint(file=mocked_file)

    # then
    assert exc_info.value.status_code == status.HTTP_413_CONTENT_TOO_LARGE
    assert exc_info.value.detail == "file size is bigger than 2MB"


@pytest.mark.asyncio
async def test_file_size_validator_zero_or_none_size():
    # given
    mocked_file = Mock()
    mocked_file.size = 0

    mock_file_none = Mock()
    mock_file_none.size = None

    # when
    result_zero = await dummy_endpoint(file=mocked_file)
    result_none = await dummy_endpoint(file=mock_file_none)

    # then
    assert result_none == "success"
    assert result_zero == "success"


@pytest.mark.asyncio
async def test_file_size_validator_missing_size_attribute():
    # given
    mocked_file = Mock(spec=[])

    # when
    result = await dummy_endpoint(file=mocked_file)

    assert result == "success"
