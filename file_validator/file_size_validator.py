from fastapi import UploadFile, HTTPException, status
from functools import wraps


def file_size_validator(file_arg_name: str, max_size_mb: int):
    max_size_bytes = max_size_mb * 1024 * 1024

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if file_arg_name in kwargs:
                file_arg = kwargs.get(file_arg_name)

                if not isinstance(file_arg, UploadFile):
                    return await func(*args, **kwargs)

                file: UploadFile = file_arg

                file_size: int | None = file.size

                if not file_size:
                    return await func(*args, **kwargs)

                if file_size > max_size_bytes:
                    raise HTTPException(
                        status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                        detail=f"file size is bigger than {max_size_mb}MB",
                    )

            return await func(*args, **kwargs)

        return wrapper

    return decorator