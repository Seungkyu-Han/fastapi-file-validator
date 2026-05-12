import os

from fastapi import UploadFile, HTTPException, status
from functools import wraps


def file_extension_validator(file_arg_name: str, file_extensions: set[str]):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if file_arg_name in kwargs:

                file_arg = kwargs.get(file_arg_name)

                if not isinstance(file_arg, UploadFile):
                    return await func(*args, **kwargs)

                file: UploadFile = file_arg

                filename: str | None = file.filename

                if not filename:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"filename is empty",
                    )

                _, ext = os.path.splitext(filename)

                file_extension = ext[1:].lower()

                if file_extension not in file_extensions:
                    raise HTTPException(
                        status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                        detail=f"{file_extension} type is unavailable",
                    )

            return await func(*args, **kwargs)

        return wrapper

    return decorator