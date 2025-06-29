# 💡 测试组织最佳实践

良好的测试组织是维护高质量测试套件的关键。本指南将介绍如何有效地组织和管理您的测试用例。

## 🎯 组织原则

### 1. 按功能模块组织

```
tests/
├── test_user/              # 用户模块
│   ├── test_user_auth.py      # 用户认证
│   ├── test_user_profile.py   # 用户资料
│   └── test_user_settings.py  # 用户设置
├── test_order/             # 订单模块
│   ├── test_order_create.py   # 订单创建
│   ├── test_order_query.py    # 订单查询
│   └── test_order_cancel.py   # 订单取消
└── test_payment/           # 支付模块
    ├── test_payment_process.py # 支付处理
    └── test_payment_refund.py  # 退款处理
```

### 2. 按测试类型分层

```
tests/
├── unit/                   # 单元测试
├── integration/            # 集成测试
├── e2e/                   # 端到端测试
├── performance/           # 性能测试
└── smoke/                 # 冒烟测试
```

### 3. 按环境和场景组织

```
tests/
├── scenarios/             # 业务场景测试
│   ├── user_journey/         # 用户旅程
│   ├── business_flow/        # 业务流程
│   └── edge_cases/           # 边界情况
├── regression/            # 回归测试
└── compatibility/         # 兼容性测试
```

## 📝 命名规范

### 1. 文件命名

```python
# 推荐的文件命名
test_user_authentication.py    # 功能明确
test_order_creation_flow.py    # 描述性强
test_payment_integration.py    # 易于理解

# 避免的文件命名
test_user.py                   # 过于宽泛
test_api.py                    # 不够具体
test_1.py                      # 无意义
```

### 2. 类命名

```python
# 推荐的类命名
class TestUserAuthentication:
    """用户认证相关测试"""
    pass

class TestOrderCreationWorkflow:
    """订单创建工作流测试"""
    pass

class TestPaymentGatewayIntegration:
    """支付网关集成测试"""
    pass

# 避免的类命名
class TestUser:               # 过于宽泛
class Test1:                  # 无意义
class UserTest:               # 不符合pytest约定
```

### 3. 方法命名

```python
class TestUserAuthentication:

    # 推荐的方法命名 - 描述性强
    def test_login_with_valid_credentials_should_return_success(self):
        """使用有效凭据登录应该返回成功"""
        pass

    def test_login_with_invalid_password_should_return_401(self):
        """使用无效密码登录应该返回401错误"""
        pass

    def test_login_with_expired_token_should_redirect_to_login(self):
        """使用过期令牌登录应该重定向到登录页面"""
        pass

    # 避免的方法命名
    def test_login(self):         # 不够具体
        pass

    def test_user_auth(self):     # 过于简略
        pass

    def test_case_1(self):        # 无意义
        pass
```

## 🏗️ 测试结构模式

### 1. AAA模式（Arrange-Act-Assert）

```python
def test_create_user_with_valid_data(self, api_client):
    """创建用户测试 - AAA模式"""

    # Arrange - 准备测试数据
    user_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    }

    # Act - 执行操作
    response = api_client.post("/users", json=user_data)

    # Assert - 验证结果
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "张三"
    assert response.json()["data"]["email"] == "zhangsan@example.com"
```

### 2. Given-When-Then模式

```python
def test_user_login_workflow(self, api_client):
    """用户登录工作流测试 - GWT模式"""

    # Given - 给定条件
    user_credentials = {
        "username": "testuser",
        "password": "testpass123"
    }

    # When - 当执行操作
    login_response = api_client.post("/auth/login", json=user_credentials)

    # Then - 那么应该
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

    # And - 并且
    token = login_response.json()["access_token"]
    profile_response = api_client.get(
        "/user/profile",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert profile_response.status_code == 200
```

### 3. 页面对象模式（适用于复杂API）

```python
# api_pages/user_api.py
class UserAPI:
    """用户API页面对象"""

    def __init__(self, client):
        self.client = client

    def create_user(self, user_data):
        """创建用户"""
        return self.client.post("/users", json=user_data)

    def get_user(self, user_id):
        """获取用户"""
        return self.client.get(f"/users/{user_id}")

    def update_user(self, user_id, user_data):
        """更新用户"""
        return self.client.put(f"/users/{user_id}", json=user_data)

    def delete_user(self, user_id):
        """删除用户"""
        return self.client.delete(f"/users/{user_id}")

# tests/test_user_crud.py
class TestUserCRUD:

    @pytest.fixture
    def user_api(self, api_client):
        return UserAPI(api_client)

    def test_user_lifecycle(self, user_api):
        """用户生命周期测试"""
        # 创建用户
        user_data = {"name": "张三", "email": "zhangsan@example.com"}
        create_response = user_api.create_user(user_data)
        assert create_response.status_code == 201

        user_id = create_response.json()["data"]["id"]

        # 获取用户
        get_response = user_api.get_user(user_id)
        assert get_response.status_code == 200

        # 更新用户
        update_data = {"name": "李四"}
        update_response = user_api.update_user(user_id, update_data)
        assert update_response.status_code == 200

        # 删除用户
        delete_response = user_api.delete_user(user_id)
        assert delete_response.status_code == 204
```

## 🏷️ 测试标记和分类

### 1. 功能标记

```python
import pytest

class TestUserAPI:

    @pytest.mark.smoke
    def test_user_login(self):
        """冒烟测试：用户登录"""
        pass

    @pytest.mark.regression
    def test_user_profile_update(self):
        """回归测试：用户资料更新"""
        pass

    @pytest.mark.integration
    def test_user_order_integration(self):
        """集成测试：用户订单集成"""
        pass

    @pytest.mark.performance
    def test_user_list_performance(self):
        """性能测试：用户列表性能"""
        pass
```

### 2. 优先级标记

```python
class TestCriticalFeatures:

    @pytest.mark.P0
    def test_critical_user_login(self):
        """P0级别：关键用户登录功能"""
        pass

    @pytest.mark.P1
    def test_important_user_registration(self):
        """P1级别：重要用户注册功能"""
        pass

    @pytest.mark.P2
    def test_normal_user_settings(self):
        """P2级别：普通用户设置功能"""
        pass
```

### 3. 环境标记

```python
class TestEnvironmentSpecific:

    @pytest.mark.dev_only
    def test_debug_endpoint(self):
        """仅在开发环境运行"""
        pass

    @pytest.mark.prod_safe
    def test_read_only_operation(self):
        """生产环境安全测试"""
        pass

    @pytest.mark.requires_external_service
    def test_third_party_integration(self):
        """需要外部服务的测试"""
        pass
```

## 📊 测试数据管理

### 1. 测试数据分离

```python
# data/test_users.py
TEST_USERS = {
    "valid_user": {
        "name": "张三",
        "email": "zhangsan@example.com",
        "age": 25
    },
    "admin_user": {
        "name": "管理员",
        "email": "admin@example.com",
        "role": "admin"
    },
    "invalid_user": {
        "name": "",
        "email": "invalid-email",
        "age": -1
    }
}

# tests/test_user_creation.py
from data.test_users import TEST_USERS

class TestUserCreation:

    def test_create_valid_user(self, api_client):
        user_data = TEST_USERS["valid_user"]
        response = api_client.post("/users", json=user_data)
        assert response.status_code == 201

    def test_create_invalid_user(self, api_client):
        user_data = TEST_USERS["invalid_user"]
        response = api_client.post("/users", json=user_data)
        assert response.status_code == 400
```

### 2. 动态测试数据

```python
from src.utils.data_driver import data_driver

class TestUserCreationWithDynamicData:

    @pytest.fixture
    def user_template(self):
        return {
            "name": "faker.name",
            "email": "faker.email",
            "phone": "faker.phone_number",
            "address": "faker.address"
        }

    def test_create_multiple_users(self, api_client, user_template):
        """创建多个用户测试"""
        test_users = data_driver.generate_test_data(user_template, count=5)

        for user_data in test_users:
            response = api_client.post("/users", json=user_data)
            assert response.status_code == 201

            # 清理数据
            user_id = response.json()["data"]["id"]
            api_client.delete(f"/users/{user_id}")
```

## 🔧 Fixture组织

### 1. 分层Fixture

```python
# conftest.py - 根级别
@pytest.fixture(scope="session")
def api_client():
    """全局API客户端"""
    return BaseClient(get_base_url())

# tests/test_user/conftest.py - 模块级别
@pytest.fixture(scope="module")
def user_api(api_client):
    """用户API客户端"""
    return UserAPI(api_client)

@pytest.fixture
def test_user():
    """测试用户数据"""
    return {"name": "测试用户", "email": "test@example.com"}

# tests/test_user/test_user_auth.py - 测试级别
@pytest.fixture
def authenticated_user(user_api, test_user):
    """已认证的测试用户"""
    # 创建用户
    create_response = user_api.create_user(test_user)
    user_id = create_response.json()["data"]["id"]

    # 登录用户
    login_response = user_api.login(test_user["email"], "password")
    token = login_response.json()["access_token"]

    yield {"user_id": user_id, "token": token}

    # 清理
    user_api.delete_user(user_id)
```

### 2. 参数化Fixture

```python
@pytest.fixture(params=["admin", "user", "guest"])
def user_role(request):
    """参数化用户角色"""
    return request.param

@pytest.fixture
def user_with_role(user_role):
    """根据角色创建用户"""
    users = {
        "admin": {"name": "管理员", "role": "admin"},
        "user": {"name": "普通用户", "role": "user"},
        "guest": {"name": "访客", "role": "guest"}
    }
    return users[user_role]

def test_access_control(api_client, user_with_role):
    """访问控制测试"""
    # 测试不同角色的访问权限
    pass
```

## 📈 测试执行策略

### 1. 测试分组执行

```bash
# 按标记执行
pytest -m smoke                    # 冒烟测试
pytest -m "smoke or regression"    # 冒烟或回归测试
pytest -m "not slow"              # 排除慢速测试

# 按目录执行
pytest tests/test_user/            # 用户模块测试
pytest tests/integration/          # 集成测试

# 按优先级执行
pytest -m P0                       # 最高优先级
pytest -m "P0 or P1"              # 高优先级
```

### 2. 并行执行

```bash
# 自动检测CPU核心数
pytest -n auto

# 指定进程数
pytest -n 4

# 按测试文件分发
pytest --dist=loadfile -n 4

# 按测试方法分发
pytest --dist=loadscope -n 4
```

### 3. 失败重试

```bash
# 失败重试
pytest --reruns 3

# 重试延迟
pytest --reruns 3 --reruns-delay 1

# 仅重试特定异常
pytest --reruns 3 --only-rerun AssertionError
```

## 🎯 质量保证

### 1. 代码覆盖率

```bash
# 安装coverage插件
pip install pytest-cov

# 运行带覆盖率的测试
pytest --cov=src --cov-report=html

# 设置覆盖率阈值
pytest --cov=src --cov-fail-under=80
```

### 2. 测试质量检查

```python
# 测试方法应该有文档字符串
def test_user_creation(self):
    """
    测试用户创建功能

    验证：
    1. 使用有效数据创建用户成功
    2. 返回正确的用户信息
    3. 用户ID为正整数
    """
    pass

# 测试应该有明确的断言
def test_api_response(self, api_client):
    response = api_client.get("/users")

    # 好的断言 - 明确具体
    assert response.status_code == 200
    assert isinstance(response.json()["data"], list)
    assert len(response.json()["data"]) > 0

    # 避免的断言 - 过于宽泛
    assert response  # 不够具体
    assert response.json()  # 没有验证内容
```

### 3. 测试维护

```python
# 定期清理无用测试
@pytest.mark.skip(reason="功能已废弃")
def test_deprecated_feature(self):
    pass

# 更新过时的测试
def test_updated_api_endpoint(self, api_client):
    """更新后的API端点测试"""
    # 使用新的API端点
    response = api_client.get("/v2/users")
    assert response.status_code == 200

# 重构重复代码
def _create_test_user(self, api_client, user_data=None):
    """创建测试用户的辅助方法"""
    if user_data is None:
        user_data = {"name": "测试用户", "email": "test@example.com"}

    response = api_client.post("/users", json=user_data)
    assert response.status_code == 201
    return response.json()["data"]["id"]
```

---

**下一步**: [高级特性](../user-guide/advanced-features.md) | [性能测试](../user-guide/performance.md)
