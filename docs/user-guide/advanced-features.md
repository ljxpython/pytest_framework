# 🚀 高级特性

本指南介绍 Pytest Framework 的高级功能，帮助您构建更强大、更灵活的测试解决方案。

## 🎭 Mock服务器

### 1. 基础Mock服务

```python
from src.utils.mock_server import MockServer, create_mock_response

# 创建Mock服务器
mock_server = MockServer(host="localhost", port=8888)

# 添加简单Mock规则
mock_server.add_rule(
    "GET", "/api/users/123",
    create_mock_response(200, {
        "id": 123,
        "name": "张三",
        "email": "zhangsan@example.com"
    })
)

# 启动服务器
mock_server.start()

# 在测试中使用
response = requests.get("http://localhost:8888/api/users/123")
assert response.status_code == 200
assert response.json()["name"] == "张三"

# 停止服务器
mock_server.stop()
```

### 2. 高级Mock规则

```python
# 带查询参数的Mock
mock_server.add_rule(
    "GET", "/api/users",
    create_mock_response(200, {"users": []}),
    query_params={"page": "1", "size": "10"}
)

# 带请求体匹配的Mock
mock_server.add_rule(
    "POST", "/api/users",
    create_mock_response(201, {"id": 124, "message": "创建成功"}),
    request_body={"name": "新用户"}
)

# 模拟延迟响应
mock_server.add_rule(
    "GET", "/api/slow-endpoint",
    create_mock_response(200, {"data": "slow response"}, delay=2.0)
)

# 模拟错误响应
mock_server.add_rule(
    "GET", "/api/error",
    create_mock_response(500, {"error": "内部服务器错误"})
)
```

### 3. 动态Mock响应

```python
def dynamic_user_response(request):
    """动态生成用户响应"""
    user_id = request.path.split('/')[-1]
    return {
        "id": int(user_id),
        "name": f"用户{user_id}",
        "timestamp": time.time()
    }

# 使用动态响应
mock_server.add_dynamic_rule(
    "GET", "/api/users/{user_id}",
    dynamic_user_response
)
```

## ⚡ 性能测试

### 1. 负载测试

```python
from src.utils.performance import load_test, PerformanceMetrics

def api_request():
    """API请求函数"""
    return requests.get("https://api.example.com/users")

# 执行负载测试
metrics = load_test(
    request_func=api_request,
    concurrent_users=10,      # 并发用户数
    total_requests=100,       # 总请求数
)

# 验证性能指标
assert metrics.avg_response_time < 1.0  # 平均响应时间小于1秒
assert metrics.error_rate < 0.05        # 错误率小于5%
assert metrics.requests_per_second > 50 # QPS大于50

print(f"性能测试结果:")
print(f"  平均响应时间: {metrics.avg_response_time:.3f}s")
print(f"  95%响应时间: {metrics.p95_response_time:.3f}s")
print(f"  QPS: {metrics.requests_per_second:.2f}")
print(f"  错误率: {metrics.error_rate:.2%}")
```

### 2. 压力测试

```python
from src.utils.performance import stress_test

def create_user_request():
    """创建用户请求"""
    user_data = {
        "name": f"用户{random.randint(1000, 9999)}",
        "email": f"user{random.randint(1000, 9999)}@example.com"
    }
    return requests.post("https://api.example.com/users", json=user_data)

# 执行压力测试
metrics = stress_test(
    request_func=create_user_request,
    duration_seconds=60,      # 持续60秒
    concurrent_users=20,      # 20个并发用户
)

# 分析压力测试结果
print(f"压力测试结果:")
print(f"  总请求数: {metrics.total_requests}")
print(f"  成功请求数: {metrics.successful_requests}")
print(f"  失败请求数: {metrics.failed_requests}")
print(f"  平均QPS: {metrics.requests_per_second:.2f}")
```

### 3. 性能基准测试

```python
class TestAPIPerformance:
    """API性能基准测试"""

    @pytest.mark.performance
    def test_user_list_performance(self):
        """用户列表性能测试"""
        def get_users():
            return self.client.get("/api/users?page=1&size=20")

        metrics = load_test(get_users, concurrent_users=5, total_requests=50)

        # 性能基准
        assert metrics.avg_response_time < 0.5    # 平均响应时间 < 500ms
        assert metrics.p95_response_time < 1.0    # 95%响应时间 < 1s
        assert metrics.error_rate == 0            # 无错误

    @pytest.mark.performance
    def test_user_creation_performance(self):
        """用户创建性能测试"""
        def create_user():
            user_data = {"name": "性能测试用户", "email": "perf@example.com"}
            return self.client.post("/api/users", json=user_data)

        metrics = load_test(create_user, concurrent_users=3, total_requests=30)

        # 写操作性能基准
        assert metrics.avg_response_time < 2.0    # 平均响应时间 < 2s
        assert metrics.error_rate < 0.1           # 错误率 < 10%
```

## 📊 数据驱动高级用法

### 1. 多数据源组合

```python
from src.utils.data_driver import data_driver

class TestDataCombination:
    """数据组合测试"""

    def test_user_with_multiple_data_sources(self):
        """使用多个数据源的测试"""
        # 从JSON加载基础用户数据
        base_users = data_driver.load_json("base_users.json")

        # 从Excel加载测试场景
        test_scenarios = data_driver.load_excel("test_scenarios.xlsx")

        # 生成动态数据
        dynamic_data = data_driver.generate_test_data({
            "timestamp": "faker.date_time",
            "session_id": "faker.uuid4"
        }, count=len(base_users))

        # 组合数据
        for i, user in enumerate(base_users):
            scenario = test_scenarios[i % len(test_scenarios)]
            dynamic = dynamic_data[i]

            # 合并数据进行测试
            test_data = {**user, **scenario, **dynamic}
            self._test_user_scenario(test_data)
```

### 2. 条件数据生成

```python
def generate_conditional_data():
    """根据条件生成测试数据"""

    # 定义数据生成规则
    rules = [
        {
            "condition": lambda: random.choice([True, False]),
            "template": {
                "user_type": "premium",
                "features": ["advanced_search", "export", "analytics"]
            }
        },
        {
            "condition": lambda: True,  # 默认条件
            "template": {
                "user_type": "basic",
                "features": ["basic_search"]
            }
        }
    ]

    # 生成数据
    test_data = []
    for _ in range(10):
        for rule in rules:
            if rule["condition"]():
                data = data_driver.generate_test_data(rule["template"], count=1)[0]
                test_data.append(data)
                break

    return test_data
```

### 3. 数据依赖管理

```python
class TestDataDependency:
    """数据依赖测试"""

    def test_user_order_workflow(self):
        """用户订单工作流测试（数据有依赖关系）"""

        # 1. 创建用户
        user_data = data_driver.generate_test_data({
            "name": "faker.name",
            "email": "faker.email"
        }, count=1)[0]

        user_response = self.client.post("/api/users", json=user_data)
        user_id = user_response.json()["data"]["id"]

        # 2. 使用用户ID创建订单
        order_data = {
            "user_id": user_id,  # 依赖于上一步的结果
            "items": [
                {"product_id": 1001, "quantity": 2}
            ]
        }

        order_response = self.client.post("/api/orders", json=order_data)
        order_id = order_response.json()["data"]["order_id"]

        # 3. 验证订单
        order_detail = self.client.get(f"/api/orders/{order_id}")
        assert order_detail.json()["data"]["user_id"] == user_id
```

## 🔐 高级认证和安全

### 1. 多种认证方式

```python
from src.client.base_auth import BearerAuth, BasicAuth, APIKeyAuth

class TestAuthentication:
    """认证测试"""

    def test_bearer_token_auth(self):
        """Bearer Token认证测试"""
        # 获取访问令牌
        login_response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })
        token = login_response.json()["access_token"]

        # 使用Bearer认证
        self.client.session.auth = BearerAuth(token)

        # 访问受保护的资源
        response = self.client.get("/api/protected")
        assert response.status_code == 200

    def test_api_key_auth(self):
        """API Key认证测试"""
        # 设置API Key
        self.client.session.headers.update({
            "X-API-Key": "your-api-key"
        })

        response = self.client.get("/api/data")
        assert response.status_code == 200

    def test_oauth2_flow(self):
        """OAuth2流程测试"""
        # 模拟OAuth2授权码流程
        auth_url = "https://auth.example.com/oauth/authorize"
        params = {
            "client_id": "your-client-id",
            "response_type": "code",
            "redirect_uri": "http://localhost:8080/callback"
        }

        # 这里通常需要模拟用户授权过程
        # 实际测试中可能需要使用Mock或预设的授权码
```

### 2. 会话管理

```python
class TestSessionManagement:
    """会话管理测试"""

    def test_session_persistence(self):
        """会话持久化测试"""
        # 登录获取会话
        login_response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass"
        })

        # 验证会话Cookie被设置
        assert "session_id" in self.client.session.cookies

        # 使用会话访问其他接口
        profile_response = self.client.get("/api/profile")
        assert profile_response.status_code == 200

        # 登出
        logout_response = self.client.post("/auth/logout")
        assert logout_response.status_code == 200

        # 验证会话失效
        profile_response = self.client.get("/api/profile")
        assert profile_response.status_code == 401
```

## 🔄 异步和并发测试

### 1. 异步HTTP客户端

```python
import asyncio
import aiohttp
from src.client.async_client import AsyncClient

class TestAsyncAPI:
    """异步API测试"""

    async def test_async_requests(self):
        """异步请求测试"""
        async with AsyncClient("https://api.example.com") as client:
            # 并发发送多个请求
            tasks = [
                client.get(f"/api/users/{i}")
                for i in range(1, 11)
            ]

            responses = await asyncio.gather(*tasks)

            # 验证所有响应
            for response in responses:
                assert response.status == 200

    async def test_async_performance(self):
        """异步性能测试"""
        start_time = time.time()

        async with AsyncClient("https://api.example.com") as client:
            tasks = [client.get("/api/users") for _ in range(100)]
            await asyncio.gather(*tasks)

        end_time = time.time()
        total_time = end_time - start_time

        # 异步请求应该比同步快很多
        assert total_time < 10  # 100个请求在10秒内完成
```

### 2. 并发测试场景

```python
import threading
from concurrent.futures import ThreadPoolExecutor

class TestConcurrency:
    """并发测试"""

    def test_concurrent_user_creation(self):
        """并发用户创建测试"""
        def create_user(user_id):
            user_data = {
                "name": f"用户{user_id}",
                "email": f"user{user_id}@example.com"
            }
            response = self.client.post("/api/users", json=user_data)
            return response.status_code == 201

        # 使用线程池并发创建用户
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [
                executor.submit(create_user, i)
                for i in range(1, 21)
            ]

            results = [future.result() for future in futures]

        # 验证所有用户都创建成功
        assert all(results)

    def test_race_condition(self):
        """竞态条件测试"""
        # 测试并发访问同一资源时的行为
        resource_id = "shared-resource-123"

        def access_resource():
            response = self.client.get(f"/api/resources/{resource_id}")
            return response.status_code

        # 并发访问
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(access_resource) for _ in range(10)]
            status_codes = [future.result() for future in futures]

        # 验证没有出现意外的错误
        assert all(code in [200, 404] for code in status_codes)
```

## 🧪 测试环境隔离

### 1. 数据库隔离

```python
import pytest
from src.utils.database import DatabaseManager

class TestDatabaseIsolation:
    """数据库隔离测试"""

    @pytest.fixture(autouse=True)
    def setup_test_database(self):
        """为每个测试设置独立的数据库"""
        # 创建测试数据库
        self.db = DatabaseManager.create_test_database()

        # 初始化测试数据
        self.db.execute_script("test_data_setup.sql")

        yield

        # 清理测试数据库
        self.db.drop_test_database()

    def test_user_operations(self):
        """用户操作测试（使用隔离的数据库）"""
        # 测试逻辑，不会影响其他测试
        pass
```

### 2. 服务隔离

```python
class TestServiceIsolation:
    """服务隔离测试"""

    @pytest.fixture
    def isolated_service(self):
        """启动隔离的服务实例"""
        # 启动测试服务
        service = TestService(port=random.randint(8000, 9000))
        service.start()

        yield service

        # 停止测试服务
        service.stop()

    def test_with_isolated_service(self, isolated_service):
        """使用隔离服务的测试"""
        client = BaseClient(f"http://localhost:{isolated_service.port}")
        response = client.get("/health")
        assert response.status_code == 200
```

## 📈 监控和观测

### 1. 测试指标收集

```python
from src.utils.metrics import MetricsCollector

class TestMetrics:
    """测试指标收集"""

    def setup_method(self):
        self.metrics = MetricsCollector()

    def test_api_with_metrics(self):
        """带指标收集的API测试"""
        start_time = time.time()

        response = self.client.get("/api/users")

        end_time = time.time()
        response_time = end_time - start_time

        # 记录指标
        self.metrics.record_response_time("get_users", response_time)
        self.metrics.increment_counter("api_calls")

        if response.status_code == 200:
            self.metrics.increment_counter("api_success")
        else:
            self.metrics.increment_counter("api_error")

        assert response.status_code == 200

    def teardown_method(self):
        """输出测试指标"""
        print(f"测试指标: {self.metrics.get_summary()}")
```

### 2. 分布式追踪

```python
from src.utils.tracing import TracingContext

class TestDistributedTracing:
    """分布式追踪测试"""

    def test_with_tracing(self):
        """带追踪的测试"""
        with TracingContext("user_creation_test") as trace:
            # 添加追踪信息
            trace.add_tag("test_type", "integration")
            trace.add_tag("user_type", "premium")

            # 执行测试
            response = self.client.post("/api/users", json={
                "name": "追踪测试用户"
            })

            # 记录追踪事件
            trace.log_event("user_created", {
                "user_id": response.json().get("id"),
                "status_code": response.status_code
            })

            assert response.status_code == 201
```

---

**下一步**: [配置管理](./configuration.md) | [性能测试](./performance.md)
