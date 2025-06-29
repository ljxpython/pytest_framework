# 📋 基础用法指南

本指南将详细介绍 Pytest Framework 的基础功能和使用方法，帮助您快速掌握框架的核心特性。

## 🎯 学习目标

通过本指南，您将学会：
- 编写基础的接口测试用例
- 使用HTTP客户端发送请求
- 进行响应断言和验证
- 管理测试配置和环境
- 组织和运行测试用例

## 🚀 第一个测试用例

### 1. 创建测试文件

在 `tests/` 目录下创建您的测试文件：

```python
# tests/test_basic_api.py
import pytest
from src.client.base_client import BaseClient
from src.utils.assertion import assert_success_response
from src.utils.environment import get_base_url

class TestBasicAPI:
    """基础API测试类"""

    def setup_method(self):
        """每个测试方法执行前的设置"""
        base_url = get_base_url()
        self.client = BaseClient(base_url)

    def test_get_request(self):
        """测试GET请求"""
        response = self.client.get("/get")
        assert_success_response(response)

    def test_post_request(self):
        """测试POST请求"""
        data = {"name": "张三", "age": 25}
        response = self.client.post("/post", json=data)
        assert_success_response(response)
```

### 2. 运行测试

```bash
# 运行单个测试文件
pytest tests/test_basic_api.py -v

# 运行特定测试方法
pytest tests/test_basic_api.py::TestBasicAPI::test_get_request -v

# 运行所有测试
pytest -v
```

## 🌐 HTTP客户端使用

### 1. 基础客户端

```python
from src.client.base_client import BaseClient

# 创建客户端
client = BaseClient("https://api.example.com", timeout=30)

# GET请求
response = client.get("/users")
response = client.get("/users", params={"page": 1, "size": 10})

# POST请求
response = client.post("/users", json={"name": "张三"})
response = client.post("/users", data="raw data")

# PUT请求
response = client.put("/users/123", json={"name": "李四"})

# DELETE请求
response = client.delete("/users/123")

# 自定义请求头
response = client.get("/users", headers={"Authorization": "Bearer token"})
```

### 2. 会话管理

```python
# 客户端会自动管理会话和Cookie
client = BaseClient("https://api.example.com")

# 登录
login_response = client.post("/login", json={
    "username": "admin",
    "password": "password"
})

# 后续请求会自动携带登录后的Cookie
user_response = client.get("/profile")
```

### 3. 认证处理

```python
from src.client.base_auth import BearerAuth, BasicAuth

# Bearer Token认证
client.session.auth = BearerAuth("your-access-token")

# Basic认证
client.session.auth = BasicAuth("username", "password")

# 自定义认证头
client.session.headers.update({
    "Authorization": "Custom your-token",
    "X-API-Key": "your-api-key"
})
```

## ✅ 响应断言

### 1. 基础断言

```python
from src.utils.assertion import assert_response, assert_success_response

# 快速成功响应断言
assert_success_response(response)  # 默认期望200状态码
assert_success_response(response, 201)  # 期望201状态码

# 详细断言
response_data = response.json()
(assert_response(response_data)
 .assert_status_code(200, response.status_code)
 .assert_contains("success", response_data.get("message", "")))
```

### 2. JSON数据断言

```python
# 响应数据示例
response_data = {
    "code": 200,
    "message": "success",
    "data": {
        "user": {
            "id": 123,
            "name": "张三",
            "email": "zhangsan@example.com"
        },
        "permissions": ["read", "write"]
    }
}

# JSONPath断言
(assert_response(response_data)
 .assert_json_path("$.code", 200)
 .assert_json_path("$.data.user.name", "张三")
 .assert_json_path("$.data.permissions[0]", "read"))

# JMESPath断言
(assert_response(response_data)
 .assert_jmespath("data.user.id", 123)
 .assert_jmespath("data.permissions | length(@)", 2))
```

### 3. 高级断言

```python
# 包含断言
assert_response(response_data).assert_contains("张三")

# 正则表达式断言
assert_response(response_data).assert_regex_match(r"\d+", str(response_data["data"]["user"]["id"]))

# 列表长度断言
assert_response(response_data).assert_list_length(2, response_data["data"]["permissions"])

# 字典键断言
assert_response(response_data).assert_dict_has_keys(["id", "name", "email"], response_data["data"]["user"])

# 数值范围断言
assert_response(response_data).assert_value_in_range(100, 200, response_data["data"]["user"]["id"])
```

## ⚙️ 配置管理

### 1. 环境配置

编辑 `conf/settings.yaml`：

```yaml
# 开发环境
boe:
  API:
    base_url: "https://dev-api.example.com"
    timeout: 30
  DB:
    host: "dev-db.example.com"
    port: 3306
    database: "test_db"
  DEBUG: true
  LOG_LEVEL: "DEBUG"

# 测试环境
test:
  API:
    base_url: "https://test-api.example.com"
    timeout: 60
  DB:
    host: "test-db.example.com"
    port: 3306
    database: "test_db"
  DEBUG: false
  LOG_LEVEL: "INFO"

# 生产环境
prod:
  API:
    base_url: "https://api.example.com"
    timeout: 30
  DB:
    host: "prod-db.example.com"
    port: 3306
    database: "prod_db"
  DEBUG: false
  LOG_LEVEL: "WARNING"
```

### 2. 使用配置

```python
from src.utils.environment import get_config, get_base_url, switch_environment

# 获取配置值
base_url = get_base_url()
timeout = get_config("API.timeout", 30)
debug_mode = get_config("DEBUG", False)

# 切换环境
switch_environment("test")

# 获取数据库配置
db_config = get_config("DB")
host = db_config.get("host")
port = db_config.get("port")
```

### 3. 敏感信息管理

创建 `conf/.secrets.yaml`（不要提交到版本控制）：

```yaml
boe:
  DB:
    user: "dev_user"
    password: "dev_password"
  API:
    secret_key: "dev_secret_key"

test:
  DB:
    user: "test_user"
    password: "test_password"
  API:
    secret_key: "test_secret_key"
```

## 📁 测试组织

### 1. 目录结构

```
tests/
├── conftest.py              # pytest配置和fixture
├── test_user/               # 用户模块测试
│   ├── __init__.py
│   ├── test_user_crud.py    # 用户CRUD测试
│   └── test_user_auth.py    # 用户认证测试
├── test_order/              # 订单模块测试
│   ├── __init__.py
│   ├── test_order_create.py # 订单创建测试
│   └── test_order_query.py  # 订单查询测试
└── test_integration/        # 集成测试
    ├── __init__.py
    └── test_workflow.py     # 业务流程测试
```

### 2. 测试分类

使用pytest标记对测试进行分类：

```python
import pytest

class TestUserAPI:

    @pytest.mark.smoke
    def test_user_login(self):
        """冒烟测试：用户登录"""
        pass

    @pytest.mark.regression
    def test_user_profile_update(self):
        """回归测试：用户信息更新"""
        pass

    @pytest.mark.slow
    def test_user_batch_import(self):
        """慢速测试：用户批量导入"""
        pass

    @pytest.mark.skip(reason="功能未实现")
    def test_user_export(self):
        """跳过测试：用户导出"""
        pass
```

### 3. 运行特定测试

```bash
# 运行冒烟测试
pytest -m smoke -v

# 运行回归测试
pytest -m regression -v

# 排除慢速测试
pytest -m "not slow" -v

# 运行特定模块
pytest tests/test_user/ -v

# 并行运行测试
pytest -n auto -v
```

## 🔧 Fixture使用

### 1. 基础Fixture

在 `tests/conftest.py` 中定义：

```python
import pytest
from src.client.base_client import BaseClient
from src.utils.environment import get_base_url

@pytest.fixture(scope="session")
def api_client():
    """API客户端fixture"""
    base_url = get_base_url()
    client = BaseClient(base_url)
    return client

@pytest.fixture(scope="function")
def test_user():
    """测试用户fixture"""
    return {
        "name": "测试用户",
        "email": "test@example.com",
        "age": 25
    }

@pytest.fixture(scope="class")
def authenticated_client(api_client):
    """已认证的客户端fixture"""
    # 执行登录
    login_response = api_client.post("/login", json={
        "username": "testuser",
        "password": "testpass"
    })
    assert login_response.status_code == 200
    return api_client
```

### 2. 使用Fixture

```python
class TestUserAPI:

    def test_get_users(self, api_client):
        """使用API客户端fixture"""
        response = api_client.get("/users")
        assert response.status_code == 200

    def test_create_user(self, authenticated_client, test_user):
        """使用多个fixture"""
        response = authenticated_client.post("/users", json=test_user)
        assert response.status_code == 201
```

## 📊 测试报告

### 1. 生成Allure报告

```bash
# 运行测试并生成Allure数据
pytest --alluredir=output/allure-result

# 生成HTML报告
allure generate output/allure-result -o output/allure-report --clean

# 启动报告服务器
allure serve output/allure-result
```

### 2. 增强报告信息

```python
import allure

class TestUserAPI:

    @allure.feature("用户管理")
    @allure.story("用户创建")
    @allure.title("创建新用户")
    @allure.description("测试创建新用户的API接口")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user(self, api_client):
        with allure.step("准备用户数据"):
            user_data = {"name": "张三", "email": "zhangsan@example.com"}

        with allure.step("发送创建用户请求"):
            response = api_client.post("/users", json=user_data)

        with allure.step("验证响应结果"):
            assert response.status_code == 201

        # 添加附件
        allure.attach(
            response.text,
            name="响应内容",
            attachment_type=allure.attachment_type.JSON
        )
```

## 🎯 最佳实践

### 1. 测试命名

```python
# 好的命名
def test_create_user_with_valid_data_should_return_201():
    pass

def test_get_user_with_invalid_id_should_return_404():
    pass

# 避免的命名
def test_user():
    pass

def test_api():
    pass
```

### 2. 断言组织

```python
# 推荐：使用链式断言
(assert_success_response(response, 201)
 .assert_json_path("$.data.id", user_id)
 .assert_json_path("$.data.name", expected_name)
 .assert_response_time(2.0, response.elapsed.total_seconds()))

# 避免：多个独立断言
assert response.status_code == 201
assert response.json()["data"]["id"] == user_id
assert response.json()["data"]["name"] == expected_name
```

### 3. 数据管理

```python
# 推荐：使用fixture管理测试数据
@pytest.fixture
def user_data():
    return {"name": "张三", "email": "zhangsan@example.com"}

# 推荐：测试后清理数据
def test_create_user(self, api_client, user_data):
    response = api_client.post("/users", json=user_data)
    user_id = response.json()["data"]["id"]

    # 测试逻辑...

    # 清理数据
    api_client.delete(f"/users/{user_id}")
```

---

**下一步**: [高级特性](./advanced-features.md) | [配置管理](./configuration.md)
