# 🎯 第一个测试

本指南将带您编写第一个接口测试用例，体验框架的核心功能。

## 🎯 学习目标

通过本指南，您将学会：
- 创建基础的测试文件和测试类
- 使用HTTP客户端发送请求
- 使用JMESPath进行响应断言
- 运行和查看测试结果

## 📝 编写第一个测试

### 1. 创建测试文件

在 `tests/` 目录下创建 `test_my_first_api.py`：

```python
"""
我的第一个API测试

演示框架基础功能的使用
"""

import pytest
from src.client.base_client import BaseClient
from src.utils.assertion import assert_api_response, assert_jmes
from src.utils.environment import get_base_url
from src.utils.jmespath_helper import jmes, CommonJMESPatterns


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
        params = {
            "name": "张三",
            "age": "25",
            "city": "北京"
        }
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
            "department": "技术部"
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

    def test_error_handling(self):
        """测试错误处理"""
        # 请求不存在的端点
        response = self.client.get("/status/404")

        # 验证404状态码
        assert response.status_code == 404

        # httpbin的404响应是HTML，不是JSON
        # 所以我们只验证状态码
        print(f"404响应状态码: {response.status_code}")

    def test_different_http_methods(self):
        """测试不同的HTTP方法"""
        test_data = {"test": "data"}

        # 测试PUT请求
        put_response = self.client.put("/put", json=test_data)
        assert put_response.status_code == 200

        put_data = put_response.json()
        assert jmes(put_data).get_value("json.test") == "data"

        # 测试PATCH请求
        patch_response = self.client.request("PATCH", "/patch", json=test_data)
        assert patch_response.status_code == 200

        patch_data = patch_response.json()
        assert jmes(patch_data).get_value("json.test") == "data"

        # 测试DELETE请求
        delete_response = self.client.delete("/delete")
        assert delete_response.status_code == 200


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
                        "active": True
                    },
                    {
                        "id": 2,
                        "name": "李四",
                        "email": "lisi@example.com",
                        "age": 30,
                        "department": "产品部",
                        "skills": ["产品设计", "用户研究"],
                        "active": True
                    },
                    {
                        "id": 3,
                        "name": "王五",
                        "email": "wangwu@example.com",
                        "age": 28,
                        "department": "技术部",
                        "skills": ["Python", "Go"],
                        "active": False
                    }
                ],
                "pagination": {
                    "total": 3,
                    "page": 1,
                    "size": 10
                }
            }
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
                    "status": "active"
                },
                "items": [
                    {"id": 1, "name": "商品1", "price": 99.99},
                    {"id": 2, "name": "商品2", "price": 199.99}
                ]
            }
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
        first_item = helper.get_value(CommonJMESPatterns.FIRST_ITEM.replace("data", "data.items"))
        assert first_item["name"] == "商品1"

        item_count = helper.count("data.items")
        assert item_count == 2
```

### 2. 运行测试

```bash
# 运行单个测试文件
pytest tests/test_my_first_api.py -v

# 运行特定测试方法
pytest tests/test_my_first_api.py::TestMyFirstAPI::test_simple_get_request -v

# 运行并显示详细输出
pytest tests/test_my_first_api.py -v -s
```

### 3. 预期输出

```
====================================================================== test session starts =======================================================================
platform darwin -- Python 3.12.3, pytest-8.4.1, pluggy-1.5.0 -- /Library/Frameworks/Python.framework/Versions/3.12/bin/python3
cachedir: .pytest_cache
rootdir: /Users/bytedance/PycharmProjects/my_best/pytest_framework
configfile: pytest.ini
plugins: allure-pytest-2.14.3, Faker-37.4.0, anyio-4.8.0, asyncio-1.0.0
collected 7 items

tests/test_my_first_api.py::TestMyFirstAPI::test_simple_get_request PASSED
tests/test_my_first_api.py::TestMyFirstAPI::test_get_with_parameters PASSED
tests/test_my_first_api.py::TestMyFirstAPI::test_post_with_json_data PASSED
tests/test_my_first_api.py::TestMyFirstAPI::test_response_headers PASSED
tests/test_my_first_api.py::TestMyFirstAPI::test_error_handling PASSED
tests/test_my_first_api.py::TestMyFirstAPI::test_different_http_methods PASSED
tests/test_my_first_api.py::TestAdvancedJMESPath::test_complex_json_response PASSED

======================================================================= 7 passed in 3.45s =======================================================================
```

## 🔍 代码解析

### 1. 测试类结构

```python
class TestMyFirstAPI:
    """测试类应该以Test开头"""

    def setup_method(self):
        """每个测试方法执行前都会调用"""
        # 初始化HTTP客户端
        self.client = BaseClient(base_url)

    def test_simple_get_request(self):
        """测试方法应该以test_开头"""
        # 测试逻辑
        pass
```

### 2. HTTP客户端使用

```python
# 创建客户端
client = BaseClient("https://httpbin.org")

# 发送GET请求
response = client.get("/get")
response = client.get("/get", params={"key": "value"})

# 发送POST请求
response = client.post("/post", json={"data": "value"})

# 其他HTTP方法
response = client.put("/put", json=data)
response = client.delete("/delete")
response = client.request("PATCH", "/patch", json=data)
```

### 3. JMESPath断言

```python
# 基础JMESPath查询
assert_jmes(response_data, "code", 200)
assert_jmes(response_data, "data.user.name", "张三")

# 使用JMESPath辅助器
helper = jmes(response_data)

# 检查路径是否存在
assert helper.exists("data.users")

# 获取值（支持默认值）
name = helper.get_value("data.user.name", "默认名称")

# 条件过滤
active_users = helper.filter_by("data.users", "active == `true`")

# 排序
sorted_users = helper.sort_by("data.users", "age")

# 计数
user_count = helper.count("data.users")
```

## 🎨 测试最佳实践

### 1. 测试命名

```python
# 好的测试命名 - 描述性强
def test_create_user_with_valid_data_should_return_201(self):
    pass

def test_get_user_with_invalid_id_should_return_404(self):
    pass

# 避免的命名 - 不够具体
def test_user(self):
    pass

def test_api(self):
    pass
```

### 2. 测试结构（AAA模式）

```python
def test_create_user(self):
    # Arrange - 准备测试数据
    user_data = {
        "name": "张三",
        "email": "zhangsan@example.com"
    }

    # Act - 执行操作
    response = self.client.post("/users", json=user_data)

    # Assert - 验证结果
    assert response.status_code == 201
    assert_jmes(response.json(), "data.name", "张三")
```

### 3. 断言组织

```python
# 推荐：使用JMESPath进行结构化断言
response_data = response.json()
helper = jmes(response_data)

assert response.status_code == 200
assert helper.get_value("code") == 200
assert helper.get_value("data.user.name") == "张三"
assert helper.exists("data.user.email")

# 避免：过多的独立断言
assert response.json()["code"] == 200
assert response.json()["data"]["user"]["name"] == "张三"
assert "email" in response.json()["data"]["user"]
```

## 🚀 进阶功能预览

### 1. 数据驱动测试

```python
from src.utils.data_driver import load_test_data

@pytest.mark.parametrize("user_data", load_test_data("test_users.json"))
def test_create_multiple_users(self, user_data):
    response = self.client.post("/users", json=user_data)
    assert response.status_code == 201
```

### 2. Mock服务器

```python
from src.utils.mock_server import MockServer, create_mock_response

@pytest.fixture
def mock_server(self):
    server = MockServer(port=8888)
    server.add_rule("GET", "/users/123",
                   create_mock_response(200, {"id": 123, "name": "张三"}))
    server.start()
    yield server
    server.stop()
```

### 3. 性能测试

```python
from src.utils.performance import load_test

def test_api_performance(self):
    def api_request():
        return self.client.get("/users")

    metrics = load_test(api_request, concurrent_users=10, total_requests=100)
    assert metrics.avg_response_time < 1.0
```

## 🎯 下一步

恭喜！您已经成功编写并运行了第一个测试。接下来您可以：

1. 📋 学习 [基础用法](../user-guide/basic-usage.md) 了解更多功能
2. 🔍 深入 [JMESPath查询](../user-guide/jmespath-guide.md) 掌握高级查询技巧
3. 📊 探索 [数据驱动测试](../user-guide/data-driven.md) 提升测试效率
4. 🎭 使用 [Mock服务器](../user-guide/mock-server.md) 模拟复杂场景
5. ⚡ 进行 [性能测试](../user-guide/performance.md) 监控API性能

## ❓ 常见问题

### Q: 为什么选择JMESPath而不是JSONPath？
A: JMESPath语法更简洁，功能更强大，支持复杂的查询和转换操作，是AWS等大型项目的首选JSON查询语言。

### Q: 如何处理认证？
A: 框架支持多种认证方式，详见 [认证指南](../user-guide/authentication.md)。

### Q: 如何组织大型测试项目？
A: 参考 [测试组织最佳实践](../best-practices/test-organization.md)。

---

**下一步**: [基础用法](../user-guide/basic-usage.md) | [JMESPath指南](../user-guide/jmespath-guide.md)
