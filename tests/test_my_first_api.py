"""
我的第一个API测试

演示框架基础功能的使用，特别是JMESPath功能
"""

import pytest

from src.client.base_client import BaseClient
from src.utils.assertion import assert_api_response, assert_jmes
from src.utils.environment import get_base_url
from src.utils.jmespath_helper import CommonJMESPatterns, jmes


class TestMyFirstAPI:
    """我的第一个API测试类"""

    def setup_method(self):
        """每个测试方法执行前的设置"""
        # 获取基础URL（从配置文件读取）
        base_url = get_base_url() or "https://httpbin.org"
        self.client = BaseClient(base_url)

    def test_simple_get_request(self):
        """测试简单的GET请求"""
        # 发送GET请求
        response = self.client.get("/get")

        # 使用JMESPath断言验证响应
        response_data = response.json()

        # 基础断言
        assert response.status_code == 200
        assert_jmes(response_data, "url", "https://httpbin.org/get")

        # 验证响应结构
        helper = jmes(response_data)
        assert helper.exists("headers")
        assert helper.exists("origin")
        assert helper.get_value("args", {}) == {}

    def test_get_with_parameters(self):
        """测试带参数的GET请求"""
        # 发送带查询参数的GET请求
        params = {"name": "张三", "age": "25", "city": "北京"}
        response = self.client.get("/get", params=params)

        # 使用JMESPath验证参数
        response_data = response.json()
        helper = jmes(response_data)

        # 验证参数正确传递
        assert helper.get_value("args.name") == "张三"
        assert helper.get_value("args.age") == "25"
        assert helper.get_value("args.city") == "北京"

        # 验证参数数量
        args_count = helper.count("args")
        assert args_count == 3

    def test_post_with_json_data(self):
        """测试POST请求发送JSON数据"""
        # 准备用户数据
        user_data = {
            "name": "李四",
            "email": "lisi@example.com",
            "age": 30,
            "department": "技术部",
        }

        # 发送POST请求
        response = self.client.post("/post", json=user_data)

        # 验证响应
        response_data = response.json()
        helper = jmes(response_data)

        # 验证状态码
        assert response.status_code == 200

        # 验证请求数据被正确接收
        assert helper.get_value("json.name") == "李四"
        assert helper.get_value("json.email") == "lisi@example.com"
        assert helper.get_value("json.age") == 30

        # 验证Content-Type
        content_type = helper.get_value("headers.Content-Type")
        assert "application/json" in content_type

    def test_response_headers(self):
        """测试响应头验证"""
        response = self.client.get("/get")
        response_data = response.json()
        helper = jmes(response_data)

        # 验证常见响应头
        headers = helper.get_dict("headers")

        assert "User-Agent" in headers
        assert "Accept" in headers
        assert "Host" in headers

        # 验证自定义User-Agent
        user_agent = headers.get("User-Agent", "")
        assert "LiJiaXin/QA/" in user_agent


class TestAdvancedJMESPath:
    """高级JMESPath查询测试"""

    def setup_method(self):
        """测试前置设置"""
        self.client = BaseClient("https://httpbin.org")

    def test_complex_json_response(self):
        """测试复杂JSON响应的JMESPath查询"""
        # 模拟复杂的API响应数据
        complex_data = {
            "code": 200,
            "message": "success",
            "data": {
                "users": [
                    {
                        "id": 1,
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "age": 25,
                        "department": "技术部",
                        "skills": ["Python", "Java", "JavaScript"],
                        "active": True,
                    },
                    {
                        "id": 2,
                        "name": "李四",
                        "email": "lisi@example.com",
                        "age": 30,
                        "department": "产品部",
                        "skills": ["产品设计", "用户研究"],
                        "active": True,
                    },
                    {
                        "id": 3,
                        "name": "王五",
                        "email": "wangwu@example.com",
                        "age": 28,
                        "department": "技术部",
                        "skills": ["Python", "Go"],
                        "active": False,
                    },
                ],
                "pagination": {"total": 3, "page": 1, "size": 10},
            },
        }

        helper = jmes(complex_data)

        # 基础查询
        assert helper.get_value("code") == 200
        assert helper.get_value("data.pagination.total") == 3

        # 数组查询
        first_user = helper.get_value("data.users[0].name")
        assert first_user == "张三"

        # 条件过滤
        tech_users = helper.filter_by("data.users", "department == '技术部'")
        assert len(tech_users) == 2

        # 活跃用户
        active_users = helper.filter_by("data.users", "active == `true`")
        assert len(active_users) == 2

        # 技能查询
        python_users = helper.filter_by("data.users", "contains(skills, 'Python')")
        assert len(python_users) == 2

        # 排序
        sorted_by_age = helper.sort_by("data.users", "age")
        assert sorted_by_age[0]["age"] == 25
        assert sorted_by_age[-1]["age"] == 30

        # 字段提取
        user_names = helper.get_list("data.users[].name")
        assert "张三" in user_names
        assert "李四" in user_names
        assert "王五" in user_names

        # 分组
        groups = helper.group_by("data.users", "department")
        assert "技术部" in groups
        assert "产品部" in groups
        assert len(groups["技术部"]) == 2
        assert len(groups["产品部"]) == 1

    def test_jmespath_patterns(self):
        """测试常用JMESPath模式"""
        # 模拟API响应
        api_response = {
            "code": 200,
            "message": "操作成功",
            "data": {
                "user": {
                    "id": 123,
                    "name": "测试用户",
                    "email": "test@example.com",
                    "status": "active",
                },
                "items": [
                    {"id": 1, "name": "商品1", "price": 99.99},
                    {"id": 2, "name": "商品2", "price": 199.99},
                ],
            },
        }

        helper = jmes(api_response)

        # 使用常用模式
        assert helper.get_value(CommonJMESPatterns.API_CODE) == 200
        assert helper.get_value(CommonJMESPatterns.API_MESSAGE) == "操作成功"
        assert helper.exists(CommonJMESPatterns.API_DATA)

        # 用户相关模式
        assert helper.get_value(CommonJMESPatterns.USER_ID) == 123
        assert helper.get_value(CommonJMESPatterns.USER_NAME) == "测试用户"
        assert helper.get_value(CommonJMESPatterns.USER_EMAIL) == "test@example.com"
        assert helper.get_value(CommonJMESPatterns.USER_STATUS) == "active"

        # 列表操作模式
        first_item = helper.get_value(
            CommonJMESPatterns.FIRST_ITEM.replace("data", "data.items")
        )
        assert first_item["name"] == "商品1"

        item_count = helper.count("data.items")
        assert item_count == 2
