"""
使用方式:
    from enums import TestEnum
    print(TestEnum.TEST_ENUM_VALUE)


"""

from enum import Enum


class TestEnum(Enum):
    """
    Enum for testing purposes
    """

    TEST_ENUM_VALUE = 1
    TEST_ENUM_VALUE_2 = 2
