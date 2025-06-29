"""
JMESPath辅助工具模块

提供JMESPath查询的便捷方法和常用查询模式
"""

from typing import Any, Dict, List, Optional, Union

import jmespath

from src.utils.log_moudle import logger


class JMESPathHelper:
    """JMESPath查询辅助类"""

    def __init__(self, data: Any):
        """
        初始化JMESPath辅助器

        Args:
            data: 要查询的数据
        """
        self.data = data
        self.logger = logger

    def search(self, path: str) -> Any:
        """
        执行JMESPath查询

        Args:
            path: JMESPath查询路径

        Returns:
            查询结果
        """
        try:
            result = jmespath.search(path, self.data)
            self.logger.debug(f"JMESPath查询: {path} -> {result}")
            return result
        except Exception as e:
            self.logger.error(f"JMESPath查询失败: {path}, 错误: {e}")
            raise

    def exists(self, path: str) -> bool:
        """
        检查路径是否存在

        Args:
            path: JMESPath查询路径

        Returns:
            是否存在
        """
        result = self.search(path)
        return result is not None

    def get_value(self, path: str, default: Any = None) -> Any:
        """
        获取值，支持默认值

        Args:
            path: JMESPath查询路径
            default: 默认值

        Returns:
            查询结果或默认值
        """
        result = self.search(path)
        return result if result is not None else default

    def get_list(self, path: str) -> List[Any]:
        """
        获取列表结果

        Args:
            path: JMESPath查询路径

        Returns:
            列表结果
        """
        result = self.search(path)
        if result is None:
            return []
        if not isinstance(result, list):
            return [result]
        return result

    def get_dict(self, path: str) -> Dict[str, Any]:
        """
        获取字典结果

        Args:
            path: JMESPath查询路径

        Returns:
            字典结果
        """
        result = self.search(path)
        if result is None:
            return {}
        if not isinstance(result, dict):
            raise ValueError(f"JMESPath查询结果不是字典类型: {type(result)}")
        return result

    def count(self, path: str) -> int:
        """
        计算查询结果的数量

        Args:
            path: JMESPath查询路径

        Returns:
            数量
        """
        result = self.search(path)
        if result is None:
            return 0
        if isinstance(result, (list, dict, str)):
            return len(result)
        return 1

    def filter_by(self, list_path: str, condition: str) -> List[Any]:
        """
        根据条件过滤列表

        Args:
            list_path: 列表的JMESPath路径
            condition: 过滤条件

        Returns:
            过滤后的列表
        """
        filter_path = f"{list_path}[?{condition}]"
        return self.get_list(filter_path)

    def sort_by(
        self, list_path: str, sort_key: str, reverse: bool = False
    ) -> List[Any]:
        """
        根据键排序列表

        Args:
            list_path: 列表的JMESPath路径
            sort_key: 排序键
            reverse: 是否逆序

        Returns:
            排序后的列表
        """
        if reverse:
            sort_path = f"reverse(sort_by({list_path}, &{sort_key}))"
        else:
            sort_path = f"sort_by({list_path}, &{sort_key})"
        return self.get_list(sort_path)

    def group_by(self, list_path: str, group_key: str) -> Dict[str, List[Any]]:
        """
        根据键分组列表

        Args:
            list_path: 列表的JMESPath路径
            group_key: 分组键

        Returns:
            分组后的字典
        """
        items = self.get_list(list_path)
        groups = {}

        for item in items:
            if isinstance(item, dict) and group_key in item:
                key = str(item[group_key])
                if key not in groups:
                    groups[key] = []
                groups[key].append(item)

        return groups

    def extract_fields(self, list_path: str, fields: List[str]) -> List[Dict[str, Any]]:
        """
        从列表中提取指定字段

        Args:
            list_path: 列表的JMESPath路径
            fields: 要提取的字段列表

        Returns:
            提取字段后的列表
        """
        field_expr = "{" + ", ".join([f"{field}: {field}" for field in fields]) + "}"
        extract_path = f"{list_path}[].{field_expr}"
        return self.get_list(extract_path)

    def find_first(self, list_path: str, condition: str) -> Optional[Any]:
        """
        查找第一个匹配条件的元素

        Args:
            list_path: 列表的JMESPath路径
            condition: 查找条件

        Returns:
            第一个匹配的元素或None
        """
        find_path = f"{list_path}[?{condition}] | [0]"
        return self.search(find_path)

    def validate_structure(self, required_paths: List[str]) -> Dict[str, bool]:
        """
        验证数据结构是否包含必需的路径

        Args:
            required_paths: 必需的路径列表

        Returns:
            验证结果字典
        """
        results = {}
        for path in required_paths:
            results[path] = self.exists(path)
        return results


# 常用JMESPath查询模式
class CommonJMESPatterns:
    """常用JMESPath查询模式"""

    # API响应相关
    API_CODE = "code"
    API_MESSAGE = "message"
    API_DATA = "data"
    API_SUCCESS = "code == `200`"
    API_ERROR = "code != `200`"

    # 分页相关
    PAGE_TOTAL = "data.total"
    PAGE_SIZE = "data.size"
    PAGE_CURRENT = "data.current"
    PAGE_ITEMS = "data.items"

    # 用户相关
    USER_ID = "data.user.id"
    USER_NAME = "data.user.name"
    USER_EMAIL = "data.user.email"
    USER_STATUS = "data.user.status"

    # 列表操作
    FIRST_ITEM = "data[0]"
    LAST_ITEM = "data[-1]"
    ITEM_COUNT = "length(data)"

    # 条件查询
    ACTIVE_USERS = "data[?status == 'active']"
    ADMIN_USERS = "data[?role == 'admin']"
    RECENT_ITEMS = "data[?created_at > '2024-01-01']"

    @staticmethod
    def get_user_by_id(user_id: int) -> str:
        """根据ID查找用户"""
        return f"data[?id == `{user_id}`] | [0]"

    @staticmethod
    def get_items_by_status(status: str) -> str:
        """根据状态查找项目"""
        return f"data[?status == '{status}']"

    @staticmethod
    def get_field_values(field: str) -> str:
        """获取所有项目的指定字段值"""
        return f"data[].{field}"

    @staticmethod
    def sort_by_field(field: str, reverse: bool = False) -> str:
        """根据字段排序"""
        if reverse:
            return f"reverse(sort_by(data, &{field}))"
        return f"sort_by(data, &{field})"


def jmes(data: Any) -> JMESPathHelper:
    """创建JMESPath辅助器的便捷函数"""
    return JMESPathHelper(data)


def quick_search(data: Any, path: str, default: Any = None) -> Any:
    """快速JMESPath查询的便捷函数"""
    return JMESPathHelper(data).get_value(path, default)


def quick_exists(data: Any, path: str) -> bool:
    """快速检查路径是否存在的便捷函数"""
    return JMESPathHelper(data).exists(path)


def quick_count(data: Any, path: str) -> int:
    """快速计算数量的便捷函数"""
    return JMESPathHelper(data).count(path)
