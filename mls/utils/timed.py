import time

from functools import wraps

from django.http import HttpResponseBase

from rest_framework.response import Response


def timed(func=None, *, header: str = 'X-Duration', key: str = 'duration'):
    if func is None:
        def configured(wrapped):
            return timed(wrapped, header=header, key=key)

        return configured

    @wraps(func)
    def timer(*args, **kwargs):
        start = time.perf_counter()
        response = func(*args, **kwargs)
        end = time.perf_counter()
        duration = end - start

        if header and isinstance(response, HttpResponseBase):
            response[header] = duration

        if key and isinstance(response, Response) and isinstance(response.data, dict):
            response.data[key] = duration

        return response

    return timer
