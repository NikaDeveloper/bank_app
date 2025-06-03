import datetime
import functools


def log(filename=None):
    def my_decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            try:
                result = func(*args, **kwargs)
                log_message = f"[{time}] {func.__name__} ok"
                return result
            except Exception as e:
                error_type = type(e).__name__
                log_message = f"[{time}] {func.__name__} error: {error_type}. Inputs: {args}, {kwargs}"
                raise
            finally:
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

        return wrapper

    return my_decorator
