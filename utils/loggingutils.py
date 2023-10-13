from functools import wraps

from rich import print


def logit():
    def logging_decorator(func):
        @wraps(func)
        def wrapped_function(*args, **kwargs):
            log_string = f"{func.__name__} was called"
            print(log_string)
            # Open the logfile and append
            return func(*args, **kwargs)

        return wrapped_function

    return logging_decorator
