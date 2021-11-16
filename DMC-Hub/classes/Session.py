from typing import Callable
from functools import wraps
from requests import Session, Response
from functions.check_status_code import check_status_code
import urllib3 as urllib


def requests_decorator(func: Callable) -> Response:
    """The decorator for request methods.

    Arguements:
        func: Function to execute inside the wrapper

    Returns:
        A request response
    """

    @wraps(func)
    def wrapper_decorator(*args, **kwargs) -> Response:
        ignore_codes = []
        if "ignore_codes" in kwargs.keys():
            ignore_codes = kwargs["ignore_codes"]
            del kwargs["ignore_codes"]

        res = func(*args, **kwargs)
        check_status_code(res.status_code, ignore_codes)
        return res

    return wrapper_decorator


class SessionCustom(Session):
    """Custom Session class from Requests Session."""

    def __init__(self) -> None:
        super().__init__()

    # @requests_decorator
    # def get(self, *args, **kwargs):
    #     res = super().get(*args, **kwargs)
    #     return res

    # @requests_decorator
    # def post(self, *args, **kwargs):
    #     res = super().post(*args, **kwargs)
    #     return res

    @requests_decorator
    def request(self, *a, **kw):
        return super().request(*a, **kw)

# ses = SessionCustom()
# print(ses.get("https://jsonplaceholder.typicode.com/todoss/1").json())
