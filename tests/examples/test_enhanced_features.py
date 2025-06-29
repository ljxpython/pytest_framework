"""
增强功能示例测试

展示框架新增功能的使用方法
"""

import pytest
import requests

from src.client.base_client import BaseClient
from src.utils.assertion import (
    assert_api_response,
    assert_jmes,
    assert_response,
    assert_success_response,
)
from src.utils.data_driver import data_driver, load_test_data
from src.utils.environment import get_base_url, get_config
from src.utils.jmespath_helper import CommonJMESPatterns, jmes, quick_search
from src.utils.mock_server import MockServer, create_mock_response
from src.utils.performance import load_test, stress_test


class TestEnhancedAssertion:
    """增强断言功能测试"""

    def test_json_path_assertion(self):
        """测试JSONPath断言"""
        response_data = {
            "code": 200,
            "message": "success",
            "data": {
                "user": {"id": 123, "name": "张三", "email": "zhangsan@example.com"},
                "items": [{"id": 1, "name": "商品1"}, {"id": 2, "name": "商品2"}],
            },
        }

        # 使用JSONPath断言
        (
            assert_response(response_data)
            .assert_json_path("$.code", 200)
            .assert_json_path("$.data.user.name", "张三")
            .assert_json_path("$.data.items[0].id", 1)
        )

    def test_jmespath_assertion(self):
        """测试JMESPath断言 - 主推技术栈"""
        response_data = {
            "code": 200,
            "message": "success",
            "data": {
                "users": [
                    {
                        "id": 1,
                        "name": "张三",
                        "age": 25,
                        "city": "北京",
                        "status": "active",
                    },
                    {
                        "id": 2,
                        "name": "李四",
                        "age": 30,
                        "city": "上海",
                        "status": "active",
                    },
                    {
                        "id": 3,
                        "name": "王五",
                        "age": 22,
                        "city": "广州",
                        "status": "inactive",
                    },
                ],
                "total": 3,
                "page": 1,
            },
        }

        # 使用JMESPath断言 - 基础查询
        (
            assert_response(response_data)
            .assert_jmespath("code", 200)
            .assert_jmespath("data.users[0].name", "张三")
            .assert_jmespath("data.users[?age > `28`].name | [0]", "李四")
            .assert_jmespath("data.total", 3)
        )

        # 使用JMESPath断言 - 高级查询
        (
            assert_response(response_data)
            .assert_jmespath_exists("data.users")
            .assert_jmespath_length("data.users", 3)
            .assert_jmespath_type("data.users", list)
            .assert_jmespath_contains("data.users[].status", "active")
        )

        # 使用JMESPath辅助器
        helper = jmes(response_data)

        # 查询活跃用户
        active_users = helper.filter_by("data.users", "status == 'active'")
        assert len(active_users) == 2

        # 按年龄排序
        sorted_users = helper.sort_by("data.users", "age")
        assert sorted_users[0]["age"] == 22

        # 提取用户名
        user_names = helper.get_list("data.users[].name")
        assert "张三" in user_names

        # 查找特定用户
        user = helper.find_first("data.users", "name == '张三'")
        assert user["id"] == 1

    def test_schema_assertion(self):
        """测试JSON Schema断言"""
        response_data = {
            "id": 123,
            "name": "测试用户",
            "email": "test@example.com",
            "age": 25,
        }

        schema = {
            "type": "object",
            "properties": {
                "id": {"type": "integer"},
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "age": {"type": "integer", "minimum": 0},
            },
            "required": ["id", "name", "email"],
        }

        # 使用Schema断言
        assert_response(response_data).assert_schema(schema)


class TestDataDriver:
    """数据驱动测试"""

    def test_generate_test_data(self):
        """测试数据生成"""
        template = {
            "name": "faker.name",
            "email": "faker.email",
            "phone": "faker.phone_number",
            "address": "faker.address",
            "age": 25,
            "city": "北京",
        }

        # 生成测试数据
        test_data = data_driver.generate_test_data(template, count=3)

        assert len(test_data) == 3
        for data in test_data:
            assert "name" in data
            assert "email" in data
            assert data["age"] == 25
            assert data["city"] == "北京"

    @pytest.mark.parametrize(
        "user_data",
        [
            {"name": "张三", "age": 25, "email": "zhangsan@example.com"},
            {"name": "李四", "age": 30, "email": "lisi@example.com"},
            {"name": "王五", "age": 28, "email": "wangwu@example.com"},
        ],
    )
    def test_parametrized_user_creation(self, user_data):
        """参数化用户创建测试"""
        # 模拟用户创建API调用
        assert user_data["name"] is not None
        assert user_data["age"] > 0
        assert "@" in user_data["email"]


class TestMockServer:
    """Mock服务器测试"""

    @pytest.fixture(scope="class")
    def mock_server(self):
        """Mock服务器fixture"""
        server = MockServer(host="localhost", port=9999)

        # 添加Mock规则
        server.add_rule(
            "GET",
            "/api/users/123",
            create_mock_response(
                200, {"id": 123, "name": "张三", "email": "zhangsan@example.com"}
            ),
        )

        server.add_rule(
            "POST",
            "/api/users",
            create_mock_response(201, {"id": 124, "message": "用户创建成功"}),
        )

        server.add_rule(
            "GET",
            "/api/error",
            create_mock_response(500, {"error": "内部服务器错误"}, delay=0.5),
        )

        server.start()
        yield server
        server.stop()

    def test_mock_get_user(self, mock_server):
        """测试Mock GET请求"""
        response = requests.get(f"{mock_server.base_url}/api/users/123")

        assert_success_response(response, 200)
        data = response.json()
        assert data["id"] == 123
        assert data["name"] == "张三"

    def test_mock_create_user(self, mock_server):
        """测试Mock POST请求"""
        user_data = {"name": "新用户", "email": "newuser@example.com"}
        response = requests.post(f"{mock_server.base_url}/api/users", json=user_data)

        assert_success_response(response, 201)
        data = response.json()
        assert data["message"] == "用户创建成功"

    def test_mock_error_response(self, mock_server):
        """测试Mock错误响应"""
        response = requests.get(f"{mock_server.base_url}/api/error")

        assert response.status_code == 500
        data = response.json()
        assert "error" in data


class TestPerformance:
    """性能测试"""

    def simple_request(self):
        """简单的HTTP请求函数"""
        response = requests.get("https://httpbin.org/delay/0.1")
        return response

    @pytest.mark.performance
    def test_load_testing(self):
        """负载测试示例"""
        # 执行负载测试：10个并发用户，总共50个请求
        metrics = load_test(self.simple_request, concurrent_users=5, total_requests=20)

        # 验证性能指标
        assert metrics.total_requests == 20
        assert metrics.error_rate < 0.1  # 错误率小于10%
        assert metrics.avg_response_time < 2.0  # 平均响应时间小于2秒

        print(f"性能测试结果: {metrics.to_dict()}")

    @pytest.mark.performance
    @pytest.mark.slow
    def test_stress_testing(self):
        """压力测试示例"""
        # 执行压力测试：5个并发用户，持续10秒
        metrics = stress_test(
            self.simple_request, duration_seconds=10, concurrent_users=3
        )

        # 验证性能指标
        assert metrics.requests_per_second > 0
        assert metrics.error_rate < 0.2  # 错误率小于20%

        print(f"压力测试结果: {metrics.to_dict()}")


class TestEnvironmentConfig:
    """环境配置测试"""

    def test_get_config_values(self):
        """测试获取配置值"""
        # 获取基础URL
        base_url = get_base_url()
        assert isinstance(base_url, str)

        # 获取自定义配置
        debug_mode = get_config("DEBUG", False)
        assert isinstance(debug_mode, bool)

        # 获取数据库配置
        db_config = get_config("DB", {})
        assert isinstance(db_config, dict)

    def test_api_client_with_config(self):
        """测试使用配置的API客户端"""
        base_url = get_base_url() or "https://httpbin.org"
        client = BaseClient(base_url)

        # 发送测试请求
        response = client.get("/get")
        assert response.status_code == 200


@pytest.mark.integration
class TestIntegratedWorkflow:
    """集成工作流测试"""

    def test_complete_api_testing_workflow(self):
        """完整的API测试工作流"""
        # 1. 生成测试数据
        user_template = {"name": "faker.name", "email": "faker.email", "age": 25}
        test_users = data_driver.generate_test_data(user_template, count=2)

        # 2. 使用环境配置
        base_url = get_base_url() or "https://httpbin.org"
        client = BaseClient(base_url)

        # 3. 执行API测试
        for user in test_users:
            response = client.post("/post", json=user)

            # 4. 使用增强断言验证响应
            (
                assert_success_response(response, 200)
                .assert_json_path("$.json.name", user["name"])
                .assert_json_path("$.json.email", user["email"])
                .assert_json_path("$.json.age", user["age"])
            )

        print("集成测试工作流执行成功！")
