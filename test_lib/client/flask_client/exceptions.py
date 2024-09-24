"""
使用方式:
try:
    # code
except FlaskClientException as e:
    # code

"""


class FlaskClientException(Exception):
    """Base class for exceptions in this module."""

    pass
