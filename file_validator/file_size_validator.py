from functools import wraps

from fastapi import HTTPException, status


def file_size_validator(file_arg_name: str, max_size_mb: int):
    """
    Decorator to validate the size of a file passed as a keyword argument to an asynchronous function. The decorator
    checks if the file's size exceeds the specified maximum size in megabytes and raises an HTTPException if the
    limit is exceeded.

    :param file_arg_name: The name of the keyword argument representing the file in the decorated function.
    :param max_size_mb: The maximum file size allowed in megabytes.
    :return: A decorator function that validates the file's size against the specified limit.
    :rtype: Callable
    """
    max_size_bytes = max_size_mb * 1024 * 1024

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if file_arg_name in kwargs:
                file = kwargs.get(file_arg_name)

                if file and (hasattr(file, "size")):
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
