import os
from functools import wraps

from fastapi import HTTPException, status


def file_extension_validator(file_arg_name: str, file_extensions: set[str]):
    """
    A decorator that validates the file extension of an uploaded file. Ensures that the provided file has an allowed
    extension before executing the decorated function. Raises an HTTPException if the validation fails.

    :param file_arg_name: The name of the argument in the decorated function's signature that is expected to
        contain the file object.
    :param file_extensions: A set of allowed file extensions (case-insensitive) for the uploaded file.
    :return: The decorated function with added file extension validation logic.
    :rtype: Callable
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if file_arg_name in kwargs:
                file = kwargs.get(file_arg_name)
                if file and (hasattr(file, "filename")):

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
