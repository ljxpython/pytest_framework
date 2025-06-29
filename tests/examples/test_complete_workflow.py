"""
完整工作流示例测试

展示框架所有功能的综合使用示例
"""

import time

import pytest
import requests

from src.client.base_client import BaseClient
from src.utils.assertion import assert_response, assert_success_response
from src.utils.data_driver import data_driver, load_test_data
from src.utils.environment import get_base_url, get_config
from src.utils.mock_server import MockServer, create_mock_response
from src.utils.performance import load_test, stress_test


class TestCompleteWorkflow:
    """完整工作流测试类"""

    @pytest.fixture(scope="class")
    def mock_server(self):
        """Mock服务器fixture"""
        server = MockServer(host="localhost", port=9998)

        # 用户相关Mock规则
        server.add_rule(
            "POST",
            "/api/users",
            create_mock_response(
                201,
                {
                    "code": 201,
                    "message": "用户创建成功",
                    "data": {
                        "id": 1001,
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "created_at": "2024-01-01T00:00:00Z",
                    },
                },
            ),
        )

        server.add_rule(
            "GET",
            "/api/users/1001",
            create_mock_response(
                200,
                {
                    "code": 200,
                    "message": "success",
                    "data": {
                        "id": 1001,
                        "name": "张三",
                        "email": "zhangsan@example.com",
                        "status": "active",
                        "created_at": "2024-01-01T00:00:00Z",
                    },
                },
            ),
        )

        server.add_rule(
            "PUT",
            "/api/users/1001",
            create_mock_response(
                200,
                {
                    "code": 200,
                    "message": "用户更新成功",
                    "data": {
                        "id": 1001,
                        "name": "张三更新",
                        "email": "zhangsan_updated@example.com",
                        "status": "active",
                        "updated_at": "2024-01-01T01:00:00Z",
                    },
                },
            ),
        )

        server.add_rule("DELETE", "/api/users/1001", create_mock_response(204, {}))

        # 订单相关Mock规则
        server.add_rule(
            "POST",
            "/api/orders",
            create_mock_response(
                201,
                {
                    "code": 201,
                    "message": "订单创建成功",
                    "data": {
                        "order_id": "ORD-2024-001",
                        "user_id": 1001,
                        "total_amount": 299.99,
                        "status": "pending",
                        "items": [{"product_id": 2001, "quantity": 2, "price": 149.99}],
                    },
                },
            ),
        )

        server.start()
        yield server
        server.stop()

    @pytest.fixture
    def api_client(self, mock_server):
        """API客户端fixture"""
        return BaseClient(mock_server.base_url)

    @pytest.fixture
    def test_users_data(self):
        """测试用户数据fixture"""
        return load_test_data("test_users.json")

    def test_user_lifecycle_workflow(self, api_client):
        """用户生命周期工作流测试"""

        # 1. 创建用户
        user_data = {"name": "张三", "email": "zhangsan@example.com", "age": 25}

        create_response = api_client.post("/api/users", json=user_data)

        # 使用增强断言验证创建响应
        (
            assert_success_response(create_response, 201)
            .assert_json_path("$.code", 201)
            .assert_json_path("$.data.name", "张三")
            .assert_json_path("$.data.email", "zhangsan@example.com")
            .assert_dict_has_keys(
                ["id", "name", "email"], create_response.json()["data"]
            )
        )

        user_id = create_response.json()["data"]["id"]

        # 2. 获取用户信息
        get_response = api_client.get(f"/api/users/{user_id}")

        (
            assert_success_response(get_response)
            .assert_json_path("$.data.id", user_id)
            .assert_json_path("$.data.status", "active")
            .assert_contains("created_at", get_response.json()["data"])
        )

        # 3. 更新用户信息
        update_data = {"name": "张三更新", "email": "zhangsan_updated@example.com"}

        update_response = api_client.put(f"/api/users/{user_id}", json=update_data)

        (
            assert_success_response(update_response)
            .assert_json_path("$.data.name", "张三更新")
            .assert_json_path("$.data.email", "zhangsan_updated@example.com")
            .assert_contains("updated_at", update_response.json()["data"])
        )

        # 4. 删除用户
        delete_response = api_client.delete(f"/api/users/{user_id}")
        assert delete_response.status_code == 204

    @pytest.mark.parametrize("user_data", load_test_data("test_users.json")[:3])
    def test_data_driven_user_creation(self, api_client, user_data):
        """数据驱动的用户创建测试"""

        # 使用测试数据创建用户
        response = api_client.post("/api/users", json=user_data)

        # 验证响应
        (
            assert_success_response(response, 201)
            .assert_json_path("$.code", 201)
            .assert_json_path("$.message", "用户创建成功")
            .assert_dict_has_keys(["id", "name", "email"], response.json()["data"])
        )

    def test_generated_test_data(self, api_client):
        """使用生成的测试数据"""

        # 定义数据模板
        user_template = {
            "name": "faker.name",
            "email": "faker.email",
            "phone": "faker.phone_number",
            "age": 25,
            "city": "北京",
        }

        # 生成测试数据
        test_users = data_driver.generate_test_data(user_template, count=3)

        for user_data in test_users:
            response = api_client.post("/api/users", json=user_data)

            (
                assert_success_response(response, 201)
                .assert_json_path("$.code", 201)
                .assert_contains("用户创建成功", response.json()["message"])
            )

    def test_business_workflow_integration(self, api_client):
        """业务工作流集成测试"""

        # 1. 创建用户
        user_data = {"name": "业务用户", "email": "business@example.com"}
        user_response = api_client.post("/api/users", json=user_data)
        user_id = user_response.json()["data"]["id"]

        # 2. 创建订单
        order_data = {
            "user_id": user_id,
            "items": [{"product_id": 2001, "quantity": 2, "price": 149.99}],
            "shipping_address": {"street": "测试街道123号", "city": "北京市"},
        }

        order_response = api_client.post("/api/orders", json=order_data)

        # 验证订单创建
        (
            assert_success_response(order_response, 201)
            .assert_json_path("$.data.user_id", user_id)
            .assert_json_path("$.data.total_amount", 299.99)
            .assert_json_path("$.data.status", "pending")
            .assert_list_length(1, order_response.json()["data"]["items"])
        )

        order_id = order_response.json()["data"]["order_id"]

        # 3. 验证订单信息
        assert order_id.startswith("ORD-")
        assert len(order_response.json()["data"]["items"]) == 1

    @pytest.mark.performance
    def test_api_performance(self, api_client):
        """API性能测试"""

        def create_user_request():
            """创建用户请求函数"""
            user_data = {
                "name": "性能测试用户",
                "email": f"perf_test_{int(time.time() * 1000)}@example.com",
            }
            return api_client.post("/api/users", json=user_data)

        # 负载测试
        metrics = load_test(create_user_request, concurrent_users=5, total_requests=20)

        # 验证性能指标
        assert metrics.total_requests == 20
        assert metrics.successful_requests >= 18  # 允许少量失败
        assert metrics.error_rate <= 0.1  # 错误率不超过10%
        assert metrics.avg_response_time <= 3.0  # 平均响应时间不超过3秒

        print(f"性能测试结果:")
        print(f"  总请求数: {metrics.total_requests}")
        print(f"  成功请求数: {metrics.successful_requests}")
        print(f"  平均响应时间: {metrics.avg_response_time:.3f}s")
        print(f"  QPS: {metrics.requests_per_second:.2f}")
        print(f"  错误率: {metrics.error_rate:.2%}")

    def test_complex_json_assertion(self, api_client):
        """复杂JSON断言测试"""

        # 创建用户
        response = api_client.post(
            "/api/users", json={"name": "复杂断言测试", "email": "complex@example.com"}
        )

        response_data = response.json()

        # 复杂断言组合
        (
            assert_response(response_data)
            .assert_json_path("$.code", 201)
            .assert_jmespath("data.id", 1001)
            .assert_regex_match(
                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z",
                response_data["data"]["created_at"],
            )
            .assert_value_in_range(1000, 2000, response_data["data"]["id"])
            .assert_dict_has_keys(["code", "message", "data"], response_data)
            .assert_contains("成功", response_data["message"])
        )

    def test_error_handling(self, api_client):
        """错误处理测试"""

        # 测试不存在的用户
        response = api_client.get("/api/users/99999")

        # 这里Mock服务器会返回404，但我们的Mock规则没有定义这个路径
        # 所以会返回默认的404响应
        assert response.status_code == 404

        error_data = response.json()
        assert "error" in error_data
        assert error_data["error"] == "Not Found"

    def test_environment_configuration(self):
        """环境配置测试"""

        # 测试配置获取
        base_url = get_base_url()
        assert isinstance(base_url, str)

        # 测试默认值
        timeout = get_config("API.timeout", 30)
        assert isinstance(timeout, int)
        assert timeout > 0

        # 测试调试模式
        debug_mode = get_config("DEBUG", False)
        assert isinstance(debug_mode, bool)

    @pytest.mark.integration
    def test_full_integration_scenario(self, api_client):
        """完整集成场景测试"""

        # 模拟完整的用户注册到下单流程

        # 1. 用户注册
        registration_data = {
            "name": "集成测试用户",
            "email": "integration@example.com",
            "password": "test123456",
        }

        register_response = api_client.post("/api/users", json=registration_data)
        assert_success_response(register_response, 201)

        user_id = register_response.json()["data"]["id"]

        # 2. 用户登录（模拟）
        # 在实际场景中，这里会有登录逻辑

        # 3. 浏览商品（模拟）
        # 在实际场景中，这里会有商品查询逻辑

        # 4. 创建订单
        order_data = {
            "user_id": user_id,
            "items": [{"product_id": 2001, "quantity": 1, "price": 149.99}],
        }

        order_response = api_client.post("/api/orders", json=order_data)
        assert_success_response(order_response, 201)

        # 5. 验证整个流程
        order_data = order_response.json()["data"]
        assert order_data["user_id"] == user_id
        assert order_data["status"] == "pending"
        assert len(order_data["items"]) == 1

        print("✅ 完整集成场景测试通过！")
        print(f"   用户ID: {user_id}")
        print(f"   订单ID: {order_data['order_id']}")
        print(f"   订单金额: {order_data['total_amount']}")


@pytest.mark.slow
class TestAdvancedFeatures:
    """高级功能测试类"""

    def test_schema_validation(self, api_client):
        """JSON Schema验证测试"""

        # 定义用户响应的Schema
        user_schema = {
            "type": "object",
            "properties": {
                "code": {"type": "integer"},
                "message": {"type": "string"},
                "data": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "name": {"type": "string"},
                        "email": {"type": "string", "format": "email"},
                        "created_at": {"type": "string"},
                    },
                    "required": ["id", "name", "email"],
                },
            },
            "required": ["code", "message", "data"],
        }

        # 创建用户并验证Schema
        user_data = {"name": "Schema测试", "email": "schema@example.com"}
        response = api_client.post("/api/users", json=user_data)

        # 使用Schema断言
        assert_response(response.json()).assert_schema(user_schema)

    def test_response_time_monitoring(self, api_client):
        """响应时间监控测试"""

        start_time = time.time()
        response = api_client.post(
            "/api/users",
            json={"name": "响应时间测试", "email": "response_time@example.com"},
        )
        end_time = time.time()

        response_time = end_time - start_time

        # 验证响应时间
        (
            assert_success_response(response, 201).assert_response_time(
                5.0, response_time
            )
        )  # 响应时间应小于5秒

        print(f"API响应时间: {response_time:.3f}秒")
