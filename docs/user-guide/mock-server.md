# 🎭 Mock服务器 - 你的专属演员

> "Mock服务器：当真实API还在开发中，我们已经在测试了！"

还在等后端API开发完成？还在为第三方服务不稳定而烦恼？Mock服务器让你摆脱依赖，想测什么就测什么！

## 🎯 为什么需要Mock服务器？

### 真实场景
你是不是遇到过这些尴尬：
- 😤 "后端API还没开发完，我的测试怎么写？"
- 🤦‍♂️ "第三方服务又挂了，测试全部失败..."
- 😱 "测试环境数据被污染了，怎么办？"
- 🙄 "想测试错误场景，但真实API不会出错"
- 😅 "网络太慢了，测试跑一次要半天"

有了Mock服务器，这些问题统统解决！

## 🚀 快速上手 - 5分钟搭建Mock服务

### 最简单的Mock

```python
from src.utils.mock_server import MockServer, create_mock_response

# 1. 创建Mock服务器
mock_server = MockServer(host="localhost", port=8888)

# 2. 添加Mock规则
mock_server.add_rule(
    "GET", "/api/hello",
    create_mock_response(200, {"message": "Hello, Mock World!"})
)

# 3. 启动服务器
mock_server.start()

# 4. 测试Mock服务
import requests
response = requests.get("http://localhost:8888/api/hello")
print(response.json())  # {"message": "Hello, Mock World!"}

# 5. 停止服务器
mock_server.stop()
```

### 在测试中使用Mock

```python
import pytest
from src.utils.mock_server import MockServer, create_mock_response

class TestWithMock:
    """使用Mock服务器的测试"""

    @pytest.fixture(scope="class")
    def mock_server(self):
        """Mock服务器fixture"""
        server = MockServer(host="localhost", port=9999)

        # 添加用户API的Mock
        server.add_rule(
            "GET", "/api/users/123",
            create_mock_response(200, {
                "id": 123,
                "name": "张三",
                "email": "zhangsan@example.com",
                "department": "技术部"
            })
        )

        # 添加用户列表的Mock
        server.add_rule(
            "GET", "/api/users",
            create_mock_response(200, {
                "code": 200,
                "data": {
                    "users": [
                        {"id": 123, "name": "张三"},
                        {"id": 124, "name": "李四"}
                    ],
                    "total": 2
                }
            })
        )

        server.start()
        yield server
        server.stop()

    def test_get_user(self, mock_server):
        """测试获取用户"""
        import requests
        response = requests.get(f"{mock_server.base_url}/api/users/123")

        assert response.status_code == 200
        assert response.json()["name"] == "张三"

    def test_get_user_list(self, mock_server):
        """测试获取用户列表"""
        import requests
        response = requests.get(f"{mock_server.base_url}/api/users")

        assert response.status_code == 200
        assert response.json()["data"]["total"] == 2
```

## 🎨 Mock规则配置 - 想怎么Mock就怎么Mock

### 基础Mock规则

```python
# 不同HTTP方法的Mock
mock_server = MockServer(port=8888)

# GET请求Mock
mock_server.add_rule(
    "GET", "/api/products",
    create_mock_response(200, {"products": ["iPhone", "iPad"]})
)

# POST请求Mock
mock_server.add_rule(
    "POST", "/api/products",
    create_mock_response(201, {"id": 1001, "message": "产品创建成功"})
)

# PUT请求Mock
mock_server.add_rule(
    "PUT", "/api/products/1001",
    create_mock_response(200, {"message": "产品更新成功"})
)

# DELETE请求Mock
mock_server.add_rule(
    "DELETE", "/api/products/1001",
    create_mock_response(204, {})  # 无内容响应
)
```

### 带参数的Mock规则

```python
# 查询参数Mock
mock_server.add_rule(
    "GET", "/api/users",
    create_mock_response(200, {
        "users": [{"id": 1, "name": "张三"}],
        "page": 1,
        "size": 10
    }),
    query_params={"page": "1", "size": "10"}  # 匹配特定查询参数
)

# 不同参数返回不同结果
mock_server.add_rule(
    "GET", "/api/users",
    create_mock_response(200, {
        "users": [{"id": 2, "name": "李四"}],
        "page": 2,
        "size": 10
    }),
    query_params={"page": "2", "size": "10"}
)

# 请求体匹配Mock
mock_server.add_rule(
    "POST", "/api/login",
    create_mock_response(200, {
        "token": "admin_token_123",
        "user": {"id": 1, "name": "管理员", "role": "admin"}
    }),
    request_body={"username": "admin", "password": "admin123"}
)

mock_server.add_rule(
    "POST", "/api/login",
    create_mock_response(401, {
        "error": "用户名或密码错误"
    }),
    request_body={"username": "admin", "password": "wrong_password"}
)
```

### 请求头匹配Mock

```python
# 需要认证的API Mock
mock_server.add_rule(
    "GET", "/api/protected",
    create_mock_response(200, {"data": "机密信息"}),
    headers={"Authorization": "Bearer valid_token"}
)

mock_server.add_rule(
    "GET", "/api/protected",
    create_mock_response(401, {"error": "未授权访问"}),
    headers={}  # 没有Authorization头
)

# API版本控制Mock
mock_server.add_rule(
    "GET", "/api/users",
    create_mock_response(200, {"version": "v1", "users": []}),
    headers={"API-Version": "v1"}
)

mock_server.add_rule(
    "GET", "/api/users",
    create_mock_response(200, {"version": "v2", "users": [], "meta": {}}),
    headers={"API-Version": "v2"}
)
```

## 🎪 高级Mock功能

### 动态响应Mock

```python
import time
import random

def dynamic_user_response(request):
    """动态生成用户响应"""
    # 从URL中提取用户ID
    user_id = int(request.path.split('/')[-1])

    # 根据ID生成不同的用户数据
    users = {
        123: {"name": "张三", "department": "技术部"},
        124: {"name": "李四", "department": "产品部"},
        125: {"name": "王五", "department": "设计部"}
    }

    user = users.get(user_id, {"name": f"用户{user_id}", "department": "未知"})

    return {
        "id": user_id,
        "name": user["name"],
        "department": user["department"],
        "timestamp": time.time(),
        "random_number": random.randint(1, 1000)
    }

# 使用动态响应
mock_server.add_dynamic_rule(
    "GET", "/api/users/{user_id}",
    dynamic_user_response
)

# 测试动态响应
def test_dynamic_mock():
    response1 = requests.get("http://localhost:8888/api/users/123")
    response2 = requests.get("http://localhost:8888/api/users/124")

    assert response1.json()["name"] == "张三"
    assert response2.json()["name"] == "李四"
    assert response1.json()["timestamp"] != response2.json()["timestamp"]
```

### 延迟和错误模拟

```python
# 模拟慢速API
mock_server.add_rule(
    "GET", "/api/slow-endpoint",
    create_mock_response(200, {"data": "慢速响应"}, delay=3.0)  # 3秒延迟
)

# 模拟网络超时
mock_server.add_rule(
    "GET", "/api/timeout",
    create_mock_response(200, {"data": "超时响应"}, delay=30.0)  # 30秒延迟
)

# 模拟服务器错误
mock_server.add_rule(
    "GET", "/api/server-error",
    create_mock_response(500, {
        "error": "内部服务器错误",
        "message": "数据库连接失败"
    })
)

# 模拟随机错误
def random_error_response(request):
    """随机返回成功或错误"""
    if random.random() < 0.3:  # 30%概率出错
        return create_mock_response(500, {"error": "随机错误"})
    else:
        return create_mock_response(200, {"data": "成功响应"})

mock_server.add_dynamic_rule("GET", "/api/flaky", random_error_response)
```

### 状态管理Mock

```python
class StatefulMockServer:
    """有状态的Mock服务器"""

    def __init__(self):
        self.users = {}
        self.next_id = 1
        self.call_count = {}

    def create_user(self, request):
        """创建用户"""
        user_data = request.json
        user_id = self.next_id
        self.next_id += 1

        self.users[user_id] = {
            "id": user_id,
            "name": user_data["name"],
            "email": user_data["email"],
            "created_at": time.time()
        }

        return create_mock_response(201, self.users[user_id])

    def get_user(self, request):
        """获取用户"""
        user_id = int(request.path.split('/')[-1])

        if user_id in self.users:
            return create_mock_response(200, self.users[user_id])
        else:
            return create_mock_response(404, {"error": "用户不存在"})

    def get_users(self, request):
        """获取用户列表"""
        return create_mock_response(200, {
            "users": list(self.users.values()),
            "total": len(self.users)
        })

    def delete_user(self, request):
        """删除用户"""
        user_id = int(request.path.split('/')[-1])

        if user_id in self.users:
            del self.users[user_id]
            return create_mock_response(204, {})
        else:
            return create_mock_response(404, {"error": "用户不存在"})

# 使用有状态Mock
stateful_mock = StatefulMockServer()

mock_server.add_dynamic_rule("POST", "/api/users", stateful_mock.create_user)
mock_server.add_dynamic_rule("GET", "/api/users/{user_id}", stateful_mock.get_user)
mock_server.add_dynamic_rule("GET", "/api/users", stateful_mock.get_users)
mock_server.add_dynamic_rule("DELETE", "/api/users/{user_id}", stateful_mock.delete_user)

# 测试有状态Mock
def test_stateful_mock():
    # 创建用户
    create_response = requests.post("http://localhost:8888/api/users", json={
        "name": "张三",
        "email": "zhangsan@example.com"
    })
    assert create_response.status_code == 201
    user_id = create_response.json()["id"]

    # 获取用户
    get_response = requests.get(f"http://localhost:8888/api/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["name"] == "张三"

    # 删除用户
    delete_response = requests.delete(f"http://localhost:8888/api/users/{user_id}")
    assert delete_response.status_code == 204

    # 再次获取应该404
    get_response2 = requests.get(f"http://localhost:8888/api/users/{user_id}")
    assert get_response2.status_code == 404
```

## 🎯 Mock场景设计

### 正常业务流程Mock

```python
def setup_normal_business_flow_mock(mock_server):
    """设置正常业务流程Mock"""

    # 1. 用户登录
    mock_server.add_rule(
        "POST", "/api/auth/login",
        create_mock_response(200, {
            "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh_token": "refresh_token_123",
            "user": {
                "id": 123,
                "name": "张三",
                "role": "user"
            }
        }),
        request_body={"username": "zhangsan", "password": "password123"}
    )

    # 2. 获取用户信息
    mock_server.add_rule(
        "GET", "/api/user/profile",
        create_mock_response(200, {
            "id": 123,
            "name": "张三",
            "email": "zhangsan@example.com",
            "balance": 1000.00
        }),
        headers={"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}
    )

    # 3. 获取商品列表
    mock_server.add_rule(
        "GET", "/api/products",
        create_mock_response(200, {
            "products": [
                {"id": 1001, "name": "iPhone 15", "price": 999.99, "stock": 50},
                {"id": 1002, "name": "MacBook Pro", "price": 1999.99, "stock": 30}
            ]
        })
    )

    # 4. 创建订单
    mock_server.add_rule(
        "POST", "/api/orders",
        create_mock_response(201, {
            "order_id": "ORD-2024-001",
            "user_id": 123,
            "items": [{"product_id": 1001, "quantity": 1, "price": 999.99}],
            "total_amount": 999.99,
            "status": "pending"
        })
    )

    # 5. 支付订单
    mock_server.add_rule(
        "POST", "/api/orders/ORD-2024-001/pay",
        create_mock_response(200, {
            "order_id": "ORD-2024-001",
            "payment_id": "PAY-2024-001",
            "status": "paid",
            "paid_at": "2024-01-01T12:00:00Z"
        })
    )

def test_complete_purchase_flow(mock_server):
    """测试完整购买流程"""
    setup_normal_business_flow_mock(mock_server)

    # 1. 登录
    login_response = requests.post(f"{mock_server.base_url}/api/auth/login", json={
        "username": "zhangsan",
        "password": "password123"
    })
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    # 2. 获取用户信息
    headers = {"Authorization": f"Bearer {token}"}
    profile_response = requests.get(f"{mock_server.base_url}/api/user/profile", headers=headers)
    assert profile_response.status_code == 200
    assert profile_response.json()["balance"] >= 999.99

    # 3. 浏览商品
    products_response = requests.get(f"{mock_server.base_url}/api/products")
    assert products_response.status_code == 200
    products = products_response.json()["products"]
    assert len(products) > 0

    # 4. 创建订单
    order_response = requests.post(f"{mock_server.base_url}/api/orders", json={
        "items": [{"product_id": 1001, "quantity": 1}]
    })
    assert order_response.status_code == 201
    order_id = order_response.json()["order_id"]

    # 5. 支付订单
    pay_response = requests.post(f"{mock_server.base_url}/api/orders/{order_id}/pay")
    assert pay_response.status_code == 200
    assert pay_response.json()["status"] == "paid"
```

### 异常场景Mock

```python
def setup_error_scenarios_mock(mock_server):
    """设置异常场景Mock"""

    # 登录失败
    mock_server.add_rule(
        "POST", "/api/auth/login",
        create_mock_response(401, {"error": "用户名或密码错误"}),
        request_body={"username": "zhangsan", "password": "wrong_password"}
    )

    # 余额不足
    mock_server.add_rule(
        "GET", "/api/user/profile",
        create_mock_response(200, {
            "id": 124,
            "name": "李四",
            "email": "lisi@example.com",
            "balance": 10.00  # 余额不足
        }),
        headers={"Authorization": "Bearer poor_user_token"}
    )

    # 商品缺货
    mock_server.add_rule(
        "GET", "/api/products/1001",
        create_mock_response(200, {
            "id": 1001,
            "name": "iPhone 15",
            "price": 999.99,
            "stock": 0  # 缺货
        })
    )

    # 订单创建失败
    mock_server.add_rule(
        "POST", "/api/orders",
        create_mock_response(400, {
            "error": "商品库存不足",
            "details": {"product_id": 1001, "requested": 1, "available": 0}
        })
    )

    # 支付失败
    mock_server.add_rule(
        "POST", "/api/orders/ORD-2024-002/pay",
        create_mock_response(402, {
            "error": "余额不足",
            "required": 999.99,
            "available": 10.00
        })
    )

def test_error_scenarios(mock_server):
    """测试异常场景"""
    setup_error_scenarios_mock(mock_server)

    # 测试登录失败
    login_response = requests.post(f"{mock_server.base_url}/api/auth/login", json={
        "username": "zhangsan",
        "password": "wrong_password"
    })
    assert login_response.status_code == 401
    assert "错误" in login_response.json()["error"]

    # 测试余额不足
    profile_response = requests.get(f"{mock_server.base_url}/api/user/profile",
                                  headers={"Authorization": "Bearer poor_user_token"})
    assert profile_response.status_code == 200
    assert profile_response.json()["balance"] < 999.99

    # 测试商品缺货
    product_response = requests.get(f"{mock_server.base_url}/api/products/1001")
    assert product_response.status_code == 200
    assert product_response.json()["stock"] == 0
```

## 🔧 Mock服务器管理

### 配置文件驱动Mock

```python
# mock_config.yaml
mock_rules:
  - method: "GET"
    path: "/api/users"
    response:
      status_code: 200
      body:
        users: []
        total: 0

  - method: "POST"
    path: "/api/users"
    request_body:
      name: "张三"
    response:
      status_code: 201
      body:
        id: 123
        name: "张三"
        message: "用户创建成功"

def load_mock_from_config(mock_server, config_file):
    """从配置文件加载Mock规则"""
    import yaml

    with open(config_file, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    for rule in config['mock_rules']:
        mock_server.add_rule(
            rule['method'],
            rule['path'],
            create_mock_response(
                rule['response']['status_code'],
                rule['response']['body']
            ),
            request_body=rule.get('request_body'),
            query_params=rule.get('query_params'),
            headers=rule.get('headers')
        )

# 使用配置文件
mock_server = MockServer(port=8888)
load_mock_from_config(mock_server, "mock_config.yaml")
mock_server.start()
```

### Mock服务器监控

```python
class MockServerMonitor:
    """Mock服务器监控器"""

    def __init__(self, mock_server):
        self.mock_server = mock_server
        self.request_log = []
        self.call_stats = {}

    def log_request(self, request):
        """记录请求"""
        self.request_log.append({
            "method": request.method,
            "path": request.path,
            "timestamp": time.time(),
            "headers": dict(request.headers),
            "body": request.body
        })

        # 统计调用次数
        key = f"{request.method} {request.path}"
        self.call_stats[key] = self.call_stats.get(key, 0) + 1

    def get_call_count(self, method, path):
        """获取调用次数"""
        key = f"{method} {path}"
        return self.call_stats.get(key, 0)

    def get_request_history(self):
        """获取请求历史"""
        return self.request_log

    def reset_stats(self):
        """重置统计"""
        self.request_log.clear()
        self.call_stats.clear()

# 使用监控器
monitor = MockServerMonitor(mock_server)

def test_with_monitoring(mock_server):
    """带监控的测试"""
    # 发送一些请求
    requests.get(f"{mock_server.base_url}/api/users")
    requests.get(f"{mock_server.base_url}/api/users")
    requests.post(f"{mock_server.base_url}/api/users", json={"name": "张三"})

    # 检查调用统计
    assert monitor.get_call_count("GET", "/api/users") == 2
    assert monitor.get_call_count("POST", "/api/users") == 1

    # 检查请求历史
    history = monitor.get_request_history()
    assert len(history) == 3
```

## 💡 Mock最佳实践

### 1. Mock数据真实性

```python
# ✅ 好的Mock数据 - 接近真实
good_mock_data = {
    "id": 123,
    "name": "张三",
    "email": "zhangsan@example.com",
    "phone": "13800138000",
    "created_at": "2024-01-01T12:00:00Z",
    "updated_at": "2024-01-01T12:00:00Z"
}

# ❌ 不好的Mock数据 - 过于简单
bad_mock_data = {
    "id": 1,
    "name": "test",
    "email": "test@test.com"
}
```

### 2. Mock规则组织

```python
class MockRuleManager:
    """Mock规则管理器"""

    def __init__(self, mock_server):
        self.mock_server = mock_server

    def setup_user_rules(self):
        """设置用户相关规则"""
        # 用户相关的所有Mock规则
        pass

    def setup_order_rules(self):
        """设置订单相关规则"""
        # 订单相关的所有Mock规则
        pass

    def setup_payment_rules(self):
        """设置支付相关规则"""
        # 支付相关的所有Mock规则
        pass

    def setup_all_rules(self):
        """设置所有规则"""
        self.setup_user_rules()
        self.setup_order_rules()
        self.setup_payment_rules()
```

### 3. Mock环境隔离

```python
@pytest.fixture(scope="function")
def isolated_mock_server():
    """每个测试使用独立的Mock服务器"""
    import socket

    # 获取可用端口
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        port = s.getsockname()[1]

    server = MockServer(port=port)
    server.start()

    yield server

    server.stop()
```

## 🎯 总结

Mock服务器让你的测试变得：
- 🎭 **独立** - 不依赖外部服务
- 🚀 **快速** - 本地响应，速度飞快
- 🎪 **灵活** - 想测什么场景都可以
- 🛡️ **稳定** - 不会因为外部服务问题而失败
- 🎯 **精确** - 可以模拟各种边界情况

记住：**好的Mock不是为了偷懒，而是为了更好地测试！**

现在就开始使用Mock服务器，让你的测试摆脱外部依赖，想测什么就测什么！

---

**小贴士**: Mock数据要尽量接近真实数据，这样测试才更有意义！
