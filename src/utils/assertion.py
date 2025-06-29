"""
增强的断言工具模块

提供丰富的断言方法，支持接口测试中的各种验证场景
主要基于JMESPath进行JSON数据查询和验证
"""

import json
import re
from typing import Any, Dict, List, Optional, Union

import jmespath
from assertpy import assert_that
from jsonpath_ng import parse

from src.utils.log_moudle import logger


class EnhancedAssertion:
    """增强的断言类，提供丰富的断言方法"""

    def __init__(self, response_data: Any = None):
        """
        初始化断言对象

        Args:
            response_data: 响应数据，可以是字典、列表或字符串
        """
        self.response_data = response_data
        self.logger = logger

    def assert_status_code(
        self, expected_code: int, actual_code: int
    ) -> "EnhancedAssertion":
        """断言HTTP状态码"""
        assert_that(actual_code).is_equal_to(expected_code)
        self.logger.info(f"✓ 状态码断言通过: {actual_code}")
        return self

    def assert_response_time(
        self, max_time: float, actual_time: float
    ) -> "EnhancedAssertion":
        """断言响应时间"""
        assert_that(actual_time).is_less_than_or_equal_to(max_time)
        self.logger.info(f"✓ 响应时间断言通过: {actual_time}s <= {max_time}s")
        return self

    def assert_json_path(
        self, json_path: str, expected_value: Any
    ) -> "EnhancedAssertion":
        """使用JSONPath断言"""
        jsonpath_expr = parse(json_path)
        matches = jsonpath_expr.find(self.response_data)

        if not matches:
            raise AssertionError(f"JSONPath '{json_path}' 未找到匹配项")

        actual_value = matches[0].value
        assert_that(actual_value).is_equal_to(expected_value)
        self.logger.info(f"✓ JSONPath断言通过: {json_path} = {actual_value}")
        return self

    def assert_jmespath(
        self, jmes_path: str, expected_value: Any
    ) -> "EnhancedAssertion":
        """使用JMESPath断言 - 推荐的主要断言方法"""
        actual_value = jmespath.search(jmes_path, self.response_data)
        assert_that(actual_value).is_equal_to(expected_value)
        self.logger.info(f"✓ JMESPath断言通过: {jmes_path} = {actual_value}")
        return self

    def assert_jmespath_exists(self, jmes_path: str) -> "EnhancedAssertion":
        """断言JMESPath路径存在"""
        actual_value = jmespath.search(jmes_path, self.response_data)
        assert_that(actual_value).is_not_none()
        self.logger.info(f"✓ JMESPath路径存在: {jmes_path}")
        return self

    def assert_jmespath_not_exists(self, jmes_path: str) -> "EnhancedAssertion":
        """断言JMESPath路径不存在"""
        actual_value = jmespath.search(jmes_path, self.response_data)
        assert_that(actual_value).is_none()
        self.logger.info(f"✓ JMESPath路径不存在: {jmes_path}")
        return self

    def assert_jmespath_contains(
        self, jmes_path: str, expected_value: Any
    ) -> "EnhancedAssertion":
        """断言JMESPath查询结果包含指定值"""
        actual_value = jmespath.search(jmes_path, self.response_data)
        assert_that(actual_value).contains(expected_value)
        self.logger.info(
            f"✓ JMESPath包含断言通过: {jmes_path} contains {expected_value}"
        )
        return self

    def assert_jmespath_length(
        self, jmes_path: str, expected_length: int
    ) -> "EnhancedAssertion":
        """断言JMESPath查询结果的长度"""
        actual_value = jmespath.search(jmes_path, self.response_data)
        if actual_value is None:
            raise AssertionError(f"JMESPath '{jmes_path}' 返回None，无法检查长度")
        assert_that(actual_value).is_length(expected_length)
        self.logger.info(
            f"✓ JMESPath长度断言通过: {jmes_path} length = {expected_length}"
        )
        return self

    def assert_jmespath_type(
        self, jmes_path: str, expected_type: type
    ) -> "EnhancedAssertion":
        """断言JMESPath查询结果的类型"""
        actual_value = jmespath.search(jmes_path, self.response_data)
        assert_that(actual_value).is_instance_of(expected_type)
        self.logger.info(
            f"✓ JMESPath类型断言通过: {jmes_path} is {expected_type.__name__}"
        )
        return self

    def assert_contains(
        self, expected_value: Any, container: Any = None
    ) -> "EnhancedAssertion":
        """断言包含关系"""
        target = container if container is not None else self.response_data
        assert_that(target).contains(expected_value)
        self.logger.info(f"✓ 包含断言通过: {expected_value} in {type(target).__name__}")
        return self

    def assert_not_contains(
        self, unexpected_value: Any, container: Any = None
    ) -> "EnhancedAssertion":
        """断言不包含关系"""
        target = container if container is not None else self.response_data
        assert_that(target).does_not_contain(unexpected_value)
        self.logger.info(
            f"✓ 不包含断言通过: {unexpected_value} not in {type(target).__name__}"
        )
        return self

    def assert_regex_match(self, pattern: str, text: str = None) -> "EnhancedAssertion":
        """断言正则表达式匹配"""
        target = text if text is not None else str(self.response_data)
        assert_that(re.search(pattern, target)).is_not_none()
        self.logger.info(f"✓ 正则断言通过: '{pattern}' 匹配成功")
        return self

    def assert_schema(self, expected_schema: Dict) -> "EnhancedAssertion":
        """断言JSON Schema"""
        try:
            import jsonschema

            jsonschema.validate(self.response_data, expected_schema)
            self.logger.info("✓ JSON Schema断言通过")
        except ImportError:
            self.logger.warning("jsonschema库未安装，跳过schema验证")
        except jsonschema.ValidationError as e:
            raise AssertionError(f"JSON Schema验证失败: {e.message}")
        return self

    def assert_list_length(
        self, expected_length: int, target_list: List = None
    ) -> "EnhancedAssertion":
        """断言列表长度"""
        target = target_list if target_list is not None else self.response_data
        assert_that(target).is_length(expected_length)
        self.logger.info(f"✓ 列表长度断言通过: {len(target)} = {expected_length}")
        return self

    def assert_dict_has_keys(
        self, expected_keys: List[str], target_dict: Dict = None
    ) -> "EnhancedAssertion":
        """断言字典包含指定键"""
        target = target_dict if target_dict is not None else self.response_data
        for key in expected_keys:
            assert_that(target).contains_key(key)
        self.logger.info(f"✓ 字典键断言通过: {expected_keys}")
        return self

    def assert_value_in_range(
        self,
        min_val: Union[int, float],
        max_val: Union[int, float],
        actual_val: Union[int, float] = None,
    ) -> "EnhancedAssertion":
        """断言数值在指定范围内"""
        target = actual_val if actual_val is not None else self.response_data
        assert_that(target).is_between(min_val, max_val)
        self.logger.info(f"✓ 数值范围断言通过: {min_val} <= {target} <= {max_val}")
        return self


def assert_response(response_data: Any = None) -> EnhancedAssertion:
    """创建断言对象的便捷函数"""
    return EnhancedAssertion(response_data)


# 常用断言的快捷函数
def assert_success_response(response, expected_code: int = 200):
    """断言成功响应的快捷函数"""
    return assert_response(
        response.json() if hasattr(response, "json") else response
    ).assert_status_code(
        expected_code,
        response.status_code if hasattr(response, "status_code") else expected_code,
    )


def assert_error_response(response, expected_code: int = 400):
    """断言错误响应的快捷函数"""
    return assert_response(
        response.json() if hasattr(response, "json") else response
    ).assert_status_code(
        expected_code,
        response.status_code if hasattr(response, "status_code") else expected_code,
    )


# JMESPath专用断言函数
def assert_jmes(data: Any, path: str, expected_value: Any = None):
    """JMESPath断言的便捷函数"""
    assertion = assert_response(data)
    if expected_value is not None:
        return assertion.assert_jmespath(path, expected_value)
    else:
        return assertion.assert_jmespath_exists(path)


def assert_api_response(response, success_path: str = "code", success_value: Any = 200):
    """API响应断言的便捷函数，基于JMESPath"""
    response_data = response.json() if hasattr(response, "json") else response
    return (
        assert_response(response_data)
        .assert_status_code(
            success_value if hasattr(response, "status_code") else 200,
            response.status_code if hasattr(response, "status_code") else 200,
        )
        .assert_jmespath(success_path, success_value)
    )
