# ✅ 断言功能 - 让验证变得优雅

> "好的断言就像一个严格但友善的老师，既能发现问题，又能给出清晰的指导。"

还在写一堆 `assert response.json()["data"]["user"]["name"] == "张三"` 这样的断言？累不累？我们的增强断言让你告别繁琐，拥抱优雅！

## 🎯 为什么需要增强断言？

### 传统断言 vs 增强断言

```python
# 😫 传统断言 - 写到手抽筋
response = client.get("/api/users/123")
assert response.status_code == 200
assert response.json()["code"] == 200
assert response.json()["data"]["user"]["name"] == "张三"
assert response.json()["data"]["user"]["email"] == "zhangsan@example.com"
assert "id" in response.json()["data"]["user"]
assert isinstance(response.json()["data"]["user"]["age"], int)
assert 18 <= response.json()["data"]["user"]["age"] <= 65

# 😱 如果断言失败，错误信息还不清楚...

# 🎉 增强断言 - 优雅到飞起
from src.utils.assertion import assert_response

(assert_response(response.json())
 .assert_status_code(200, response.status_code)
 .assert_jmespath("code", 200)
 .assert_jmespath("data.user.name", "张三")
 .assert_jmespath("data.user.email", "zhangsan@example.com")
 .assert_jmespath_exists("data.user.id")
 .assert_jmespath_type("data.user.age", int)
 .assert_value_in_range(18, 65, response.json()["data"]["user"]["age"]))

# 链式调用，清晰明了，错误信息超详细！
```

## 🔍 JMESPath断言 - 核心技术栈

### 基础JMESPath断言

```python
from src.utils.assertion import assert_response
from src.utils.jmespath_helper import jmes

# 测试数据
api_response = {
    "code": 200,
    "message": "success",
    "data": {
        "user": {
            "id": 123,
            "name": "张三",
            "email": "zhangsan@example.com",
            "age": 25,
            "active": True,
            "tags": ["VIP", "技术"]
        },
        "permissions": ["read", "write", "admin"]
    }
}

# 基础断言
(assert_response(api_response)
 .assert_jmespath("code", 200)                    # 验证状态码
 .assert_jmespath("message", "success")           # 验证消息
 .assert_jmespath("data.user.name", "张三")       # 验证用户名
 .assert_jmespath("data.user.age", 25))           # 验证年龄
```

### 高级JMESPath断言

```python
# 存在性断言
(assert_response(api_response)
 .assert_jmespath_exists("data.user.id")          # 验证ID存在
 .assert_jmespath_exists("data.permissions")      # 验证权限存在
 .assert_jmespath_not_exists("data.user.password")) # 验证密码不存在

# 类型断言
(assert_response(api_response)
 .assert_jmespath_type("data.user.id", int)       # 验证ID是整数
 .assert_jmespath_type("data.user.name", str)     # 验证姓名是字符串
 .assert_jmespath_type("data.user.active", bool)  # 验证状态是布尔值
 .assert_jmespath_type("data.permissions", list)) # 验证权限是列表

# 长度断言
(assert_response(api_response)
 .assert_jmespath_length("data.permissions", 3)   # 验证权限数量
 .assert_jmespath_length("data.user.tags", 2))    # 验证标签数量

# 包含断言
(assert_response(api_response)
 .assert_jmespath_contains("data.permissions", "admin")  # 验证包含admin权限
 .assert_jmespath_contains("data.user.tags", "VIP"))     # 验证包含VIP标签
```

### 复杂JMESPath查询断言

```python
# 复杂的API响应
complex_response = {
    "code": 200,
    "data": {
        "users": [
            {"id": 1, "name": "张三", "age": 25, "department": "技术部", "active": True},
            {"id": 2, "name": "李四", "age": 30, "department": "产品部", "active": True},
            {"id": 3, "name": "王五", "age": 28, "department": "技术部", "active": False}
        ],
        "summary": {
            "total": 3,
            "active_count": 2,
            "departments": ["技术部", "产品部"]
        }
    }
}

# 使用JMESPath辅助器进行复杂断言
helper = jmes(complex_response)

# 验证活跃用户数量
active_users = helper.filter_by("data.users", "active == `true`")
assert len(active_users) == 2

# 验证技术部用户
tech_users = helper.filter_by("data.users", "department == '技术部'")
assert len(tech_users) == 2

# 验证年龄最大的用户
oldest_user = helper.sort_by("data.users", "age", reverse=True)[0]
assert oldest_user["name"] == "李四"

# 验证用户名列表
user_names = helper.get_list("data.users[].name")
assert "张三" in user_names
assert "李四" in user_names
assert "王五" in user_names

# 组合断言
(assert_response(complex_response)
 .assert_jmespath("data.summary.total", 3)
 .assert_jmespath("data.summary.active_count", len(active_users))
 .assert_jmespath_contains("data.summary.departments", "技术部"))
```

## 🎨 链式断言 - 优雅的艺术

### 基础链式断言

```python
# 一气呵成的断言链
def test_user_api_complete_validation(self):
    """完整的用户API验证"""
    response = self.client.get("/api/users/123")

    (assert_response(response.json())
     .assert_status_code(200, response.status_code)     # HTTP状态码
     .assert_jmespath("code", 200)                      # 业务状态码
     .assert_jmespath("message", "success")             # 业务消息
     .assert_jmespath_exists("data.user")               # 用户数据存在
     .assert_jmespath_type("data.user.id", int)         # ID类型
     .assert_jmespath_type("data.user.name", str)       # 姓名类型
     .assert_jmespath("data.user.active", True)         # 用户状态
     .assert_response_time(2.0, response.elapsed.total_seconds()))  # 响应时间
```

### 条件链式断言

```python
def test_conditional_assertions(self):
    """条件断言示例"""
    response = self.client.get("/api/users/123")
    response_data = response.json()

    assertion = assert_response(response_data)

    # 基础断言
    assertion.assert_jmespath("code", 200)

    # 条件断言
    user_type = response_data.get("data", {}).get("user", {}).get("type")

    if user_type == "VIP":
        # VIP用户特殊验证
        (assertion
         .assert_jmespath_exists("data.user.vip_level")
         .assert_jmespath_exists("data.user.vip_benefits")
         .assert_jmespath_type("data.user.vip_level", int))

    elif user_type == "admin":
        # 管理员用户特殊验证
        (assertion
         .assert_jmespath_exists("data.user.permissions")
         .assert_jmespath_contains("data.user.permissions", "admin")
         .assert_jmespath_type("data.user.permissions", list))

    else:
        # 普通用户验证
        assertion.assert_jmespath("data.user.type", "normal")
```

## 🎯 专用断言方法

### HTTP响应断言

```python
from src.utils.assertion import assert_success_response, assert_error_response

def test_http_response_assertions(self):
    """HTTP响应专用断言"""

    # 成功响应断言
    success_response = self.client.get("/api/users")
    assert_success_response(success_response, 200)  # 期望200状态码

    # 创建成功断言
    create_response = self.client.post("/api/users", json={"name": "新用户"})
    assert_success_response(create_response, 201)   # 期望201状态码

    # 错误响应断言
    error_response = self.client.get("/api/users/999999")
    assert_error_response(error_response, 404)      # 期望404状态码

    # 验证错误响应
    bad_request = self.client.post("/api/users", json={"invalid": "data"})
    (assert_error_response(bad_request, 400)
     .assert_jmespath_exists("error.message")
     .assert_jmespath_exists("error.code"))
```

### 业务规则断言

```python
class BusinessAssertion:
    """业务规则断言类"""

    @staticmethod
    def assert_user_permission(user_data, required_permission):
        """验证用户权限"""
        permissions = user_data.get("permissions", [])
        if required_permission not in permissions:
            raise AssertionError(f"用户缺少权限: {required_permission}")
        return True

    @staticmethod
    def assert_order_amount(order_data, min_amount=0, max_amount=float('inf')):
        """验证订单金额"""
        amount = order_data.get("amount", 0)
        if not (min_amount <= amount <= max_amount):
            raise AssertionError(f"订单金额 {amount} 不在范围 [{min_amount}, {max_amount}] 内")
        return True

    @staticmethod
    def assert_business_hours(timestamp):
        """验证营业时间"""
        from datetime import datetime
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        hour = dt.hour
        if not (9 <= hour <= 18):
            raise AssertionError(f"时间 {hour}:00 不在营业时间内 (9:00-18:00)")
        return True

def test_business_rules(self):
    """业务规则测试"""
    response = self.client.get("/api/orders/123")
    order_data = response.json()["data"]["order"]

    # 使用业务断言
    BusinessAssertion.assert_order_amount(order_data, min_amount=10, max_amount=10000)
    BusinessAssertion.assert_business_hours(order_data["created_at"])

    # 结合链式断言
    (assert_response(response.json())
     .assert_jmespath("code", 200)
     .assert_jmespath_exists("data.order.id")
     .assert_jmespath_type("data.order.amount", (int, float)))
```

## 🔍 Schema验证 - 结构化验证

### JSON Schema断言

```python
import jsonschema
from src.utils.assertion import assert_response

# 定义用户响应的Schema
USER_RESPONSE_SCHEMA = {
    "type": "object",
    "properties": {
        "code": {"type": "integer", "enum": [200]},
        "message": {"type": "string"},
        "data": {
            "type": "object",
            "properties": {
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "minimum": 1},
                        "name": {"type": "string", "minLength": 1},
                        "email": {"type": "string", "format": "email"},
                        "age": {"type": "integer", "minimum": 0, "maximum": 150},
                        "active": {"type": "boolean"},
                        "tags": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["id", "name", "email", "active"]
                }
            },
            "required": ["user"]
        }
    },
    "required": ["code", "message", "data"]
}

def test_schema_validation(self):
    """Schema验证测试"""
    response = self.client.get("/api/users/123")

    # 使用Schema断言
    (assert_response(response.json())
     .assert_schema(USER_RESPONSE_SCHEMA)
     .assert_jmespath("data.user.name", "张三"))
```

### 自定义Schema验证

```python
class CustomSchemaValidator:
    """自定义Schema验证器"""

    @staticmethod
    def validate_api_response_structure(data):
        """验证API响应结构"""
        required_fields = ["code", "message", "data"]
        for field in required_fields:
            if field not in data:
                raise AssertionError(f"响应缺少必需字段: {field}")

        # 验证状态码
        if not isinstance(data["code"], int):
            raise AssertionError("状态码必须是整数")

        # 验证消息
        if not isinstance(data["message"], str):
            raise AssertionError("消息必须是字符串")

        return True

    @staticmethod
    def validate_pagination_structure(data):
        """验证分页结构"""
        pagination_fields = ["total", "page", "size", "items"]
        for field in pagination_fields:
            if field not in data:
                raise AssertionError(f"分页数据缺少字段: {field}")

        # 验证数值字段
        for field in ["total", "page", "size"]:
            if not isinstance(data[field], int) or data[field] < 0:
                raise AssertionError(f"{field} 必须是非负整数")

        # 验证items是列表
        if not isinstance(data["items"], list):
            raise AssertionError("items 必须是列表")

        return True

def test_custom_schema_validation(self):
    """自定义Schema验证测试"""
    response = self.client.get("/api/users?page=1&size=10")
    response_data = response.json()

    # 使用自定义验证器
    CustomSchemaValidator.validate_api_response_structure(response_data)
    CustomSchemaValidator.validate_pagination_structure(response_data["data"])

    # 结合其他断言
    (assert_response(response_data)
     .assert_jmespath("code", 200)
     .assert_jmespath_type("data.items", list)
     .assert_jmespath_length("data.items", response_data["data"]["size"]))
```

## 🎪 高级断言技巧

### 模糊匹配断言

```python
import re
from src.utils.assertion import assert_response

def test_fuzzy_matching(self):
    """模糊匹配断言"""
    response = self.client.get("/api/users/123")
    response_data = response.json()

    # 正则表达式断言
    (assert_response(response_data)
     .assert_regex_match(r"\d+", str(response_data["data"]["user"]["id"]))  # ID是数字
     .assert_regex_match(r"[\w\.-]+@[\w\.-]+\.\w+", response_data["data"]["user"]["email"])  # 邮箱格式
     .assert_regex_match(r"^[\u4e00-\u9fa5]+$", response_data["data"]["user"]["name"]))  # 中文姓名

def test_partial_matching(self):
    """部分匹配断言"""
    response = self.client.get("/api/search?q=张")
    response_data = response.json()

    # 验证搜索结果都包含"张"
    users = response_data["data"]["users"]
    for user in users:
        assert "张" in user["name"], f"用户 {user['name']} 不包含搜索关键字"

    # 使用JMESPath验证
    helper = jmes(response_data)
    user_names = helper.get_list("data.users[].name")
    for name in user_names:
        assert "张" in name
```

### 性能断言

```python
import time
from src.utils.assertion import assert_response

def test_performance_assertions(self):
    """性能断言测试"""
    start_time = time.time()
    response = self.client.get("/api/users")
    end_time = time.time()

    response_time = end_time - start_time

    # 响应时间断言
    (assert_response(response.json())
     .assert_jmespath("code", 200)
     .assert_response_time(2.0, response_time))  # 响应时间小于2秒

    # 数据量断言
    users = response.json()["data"]["users"]
    assert len(users) <= 100, "单次返回用户数量不应超过100"

    # 内存使用断言（需要额外工具）
    import psutil
    process = psutil.Process()
    memory_usage = process.memory_info().rss / 1024 / 1024  # MB
    assert memory_usage < 500, f"内存使用过高: {memory_usage}MB"
```

### 批量断言

```python
def test_batch_assertions(self):
    """批量断言测试"""
    # 获取用户列表
    response = self.client.get("/api/users")
    users = response.json()["data"]["users"]

    # 批量验证每个用户的数据结构
    for i, user in enumerate(users):
        try:
            (assert_response({"user": user})
             .assert_jmespath_exists("user.id")
             .assert_jmespath_exists("user.name")
             .assert_jmespath_exists("user.email")
             .assert_jmespath_type("user.id", int)
             .assert_jmespath_type("user.name", str)
             .assert_regex_match(r"[\w\.-]+@[\w\.-]+\.\w+", user["email"]))
        except AssertionError as e:
            raise AssertionError(f"第 {i+1} 个用户数据验证失败: {e}")

    print(f"✅ 批量验证通过，共验证 {len(users)} 个用户")
```

## 💡 断言最佳实践

### 1. 断言粒度控制

```python
# ✅ 好的断言 - 粒度适中
def test_user_creation_good(self):
    response = self.client.post("/users", json={"name": "张三"})

    (assert_success_response(response, 201)
     .assert_jmespath("data.user.name", "张三")
     .assert_jmespath_exists("data.user.id")
     .assert_jmespath_type("data.user.created_at", str))

# ❌ 过细的断言 - 太啰嗦
def test_user_creation_too_detailed(self):
    response = self.client.post("/users", json={"name": "张三"})

    assert response.status_code == 201
    assert response.headers["Content-Type"] == "application/json"
    assert "data" in response.json()
    assert "user" in response.json()["data"]
    assert "id" in response.json()["data"]["user"]
    assert "name" in response.json()["data"]["user"]
    # ... 太多了！

# ❌ 过粗的断言 - 不够具体
def test_user_creation_too_broad(self):
    response = self.client.post("/users", json={"name": "张三"})
    assert response.status_code == 201  # 只验证状态码，不够！
```

### 2. 错误信息优化

```python
class EnhancedAssertion:
    """增强断言类 - 提供更好的错误信息"""

    def assert_jmespath_with_context(self, path, expected, actual_data):
        """带上下文的JMESPath断言"""
        actual = jmespath.search(path, actual_data)
        if actual != expected:
            context = {
                "path": path,
                "expected": expected,
                "actual": actual,
                "data_snippet": self._get_data_snippet(actual_data, path)
            }
            raise AssertionError(f"JMESPath断言失败:\n{json.dumps(context, indent=2, ensure_ascii=False)}")

    def _get_data_snippet(self, data, path):
        """获取相关数据片段"""
        # 简化实现，实际可以更智能
        return str(data)[:200] + "..." if len(str(data)) > 200 else str(data)
```

### 3. 断言复用

```python
class CommonAssertions:
    """通用断言集合"""

    @staticmethod
    def assert_api_success(response_data):
        """标准API成功响应断言"""
        return (assert_response(response_data)
                .assert_jmespath("code", 200)
                .assert_jmespath("message", "success")
                .assert_jmespath_exists("data"))

    @staticmethod
    def assert_user_data_structure(user_data):
        """用户数据结构断言"""
        return (assert_response({"user": user_data})
                .assert_jmespath_exists("user.id")
                .assert_jmespath_exists("user.name")
                .assert_jmespath_exists("user.email")
                .assert_jmespath_type("user.id", int))

    @staticmethod
    def assert_pagination_data(pagination_data):
        """分页数据断言"""
        return (assert_response(pagination_data)
                .assert_jmespath_exists("total")
                .assert_jmespath_exists("page")
                .assert_jmespath_exists("size")
                .assert_jmespath_exists("items")
                .assert_jmespath_type("items", list))

# 使用通用断言
def test_with_common_assertions(self):
    response = self.client.get("/api/users")
    response_data = response.json()

    # 使用通用断言
    CommonAssertions.assert_api_success(response_data)
    CommonAssertions.assert_pagination_data(response_data["data"])

    # 验证每个用户数据
    for user in response_data["data"]["items"]:
        CommonAssertions.assert_user_data_structure(user)
```

## 🎯 总结

增强断言让你的测试验证变得：
- 🎨 **优雅** - 链式调用，代码简洁
- 🔍 **强大** - JMESPath查询，功能丰富
- 🎯 **精确** - 多种断言类型，验证全面
- 🛡️ **可靠** - 详细错误信息，问题定位快
- 🔄 **可复用** - 通用断言，减少重复代码

记住：**好的断言不仅能发现问题，还能清楚地告诉你问题在哪里！**

现在就开始使用增强断言，让你的测试验证更加优雅和强大！

---

**小贴士**: 断言失败时，仔细看错误信息，它会告诉你很多有用的调试信息！
