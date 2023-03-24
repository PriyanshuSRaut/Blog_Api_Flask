from functools import wraps

# wrapper for checking if the user is logged in or not
def check_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

    