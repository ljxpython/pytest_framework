# 🔍 JMESPath查询指南

JMESPath是本框架的核心技术栈，提供强大而简洁的JSON数据查询能力。本指南将详细介绍JMESPath的使用方法和最佳实践。

## 🎯 为什么选择JMESPath

### 优势对比

| 特性 | JMESPath | JSONPath | 原生Python |
|------|----------|----------|-------------|
| **语法简洁** | ✅ 非常简洁 | ⚠️ 较复杂 | ❌ 冗长 |
| **性能** | ✅ 编译型，高性能 | ⚠️ 解释型 | ✅ 原生性能 |
| **功能强大** | ✅ 支持复杂查询 | ⚠️ 功能有限 | ✅ 功能完整 |
| **可读性** | ✅ 声明式，易读 | ⚠️ 一般 | ❌ 命令式 |
| **生态支持** | ✅ AWS等大厂使用 | ⚠️ 社区支持 | ✅ Python原生 |

### 实际对比示例

```python
# 查询活跃用户的姓名
data = {
    "users": [
        {"name": "张三", "status": "active"},
        {"name": "李四", "status": "inactive"},
        {"name": "王五", "status": "active"}
    ]
}

# JMESPath方式 - 简洁明了
active_names = jmespath.search("users[?status == 'active'].name", data)

# JSONPath方式 - 语法复杂
active_names = jsonpath.jsonpath(data, "$.users[?(@.status=='active')].name")

# 原生Python方式 - 代码冗长
active_names = [user["name"] for user in data["users"] if user["status"] == "active"]
```

## 📚 JMESPath基础语法

### 1. 基础访问

```python
data = {
    "name": "张三",
    "age": 25,
    "address": {
        "city": "北京",
        "district": "朝阳区"
    }
}

# 基础字段访问
name = jmespath.search("name", data)  # "张三"
age = jmespath.search("age", data)    # 25

# 嵌套字段访问
city = jmespath.search("address.city", data)  # "北京"
```

### 2. 数组操作

```python
data = {
    "users": [
        {"id": 1, "name": "张三", "age": 25},
        {"id": 2, "name": "李四", "age": 30},
        {"id": 3, "name": "王五", "age": 28}
    ]
}

# 数组索引
first_user = jmespath.search("users[0]", data)
last_user = jmespath.search("users[-1]", data)

# 数组切片
first_two = jmespath.search("users[:2]", data)
last_two = jmespath.search("users[-2:]", data)

# 提取字段
names = jmespath.search("users[].name", data)  # ["张三", "李四", "王五"]
ages = jmespath.search("users[].age", data)    # [25, 30, 28]
```

### 3. 条件过滤

```python
data = {
    "users": [
        {"name": "张三", "age": 25, "department": "技术部", "active": True},
        {"name": "李四", "age": 30, "department": "产品部", "active": True},
        {"name": "王五", "age": 28, "department": "技术部", "active": False}
    ]
}

# 简单条件
active_users = jmespath.search("users[?active]", data)
tech_users = jmespath.search("users[?department == '技术部']", data)

# 数值比较
young_users = jmespath.search("users[?age < `30`]", data)
senior_users = jmespath.search("users[?age >= `30`]", data)

# 复合条件
active_tech = jmespath.search("users[?active && department == '技术部']", data)
young_or_tech = jmespath.search("users[?age < `30` || department == '技术部']", data)
```

### 4. 投影和转换

```python
# 对象投影
user_info = jmespath.search("users[].{name: name, age: age}", data)
# 结果: [{"name": "张三", "age": 25}, {"name": "李四", "age": 30}, ...]

# 条件投影
active_info = jmespath.search("users[?active].{姓名: name, 年龄: age}", data)

# 管道操作
sorted_names = jmespath.search("users[].name | sort(@)", data)
# 结果: ["李四", "王五", "张三"]
```

## 🛠️ 框架中的JMESPath使用

### 1. 基础断言

```python
from src.utils.assertion import assert_response

response_data = {
    "code": 200,
    "message": "success",
    "data": {
        "user": {"id": 123, "name": "张三"}
    }
}

# 基础JMESPath断言
(assert_response(response_data)
 .assert_jmespath("code", 200)
 .assert_jmespath("message", "success")
 .assert_jmespath("data.user.name", "张三"))
```

### 2. 高级断言

```python
# 存在性断言
assert_response(response_data).assert_jmespath_exists("data.user")

# 类型断言
assert_response(response_data).assert_jmespath_type("data.user.id", int)

# 长度断言
assert_response(response_data).assert_jmespath_length("data.items", 5)

# 包含断言
assert_response(response_data).assert_jmespath_contains("data.tags", "重要")
```

### 3. JMESPath辅助器

```python
from src.utils.jmespath_helper import jmes

helper = jmes(response_data)

# 安全获取值（支持默认值）
user_name = helper.get_value("data.user.name", "未知用户")

# 获取列表（确保返回列表类型）
items = helper.get_list("data.items")

# 检查路径是否存在
has_user = helper.exists("data.user")

# 计算数量
item_count = helper.count("data.items")
```

## 🎨 高级查询技巧

### 1. 复杂条件查询

```python
data = {
    "products": [
        {"name": "iPhone", "price": 999, "category": "手机", "stock": 50, "rating": 4.5},
        {"name": "iPad", "price": 599, "category": "平板", "stock": 30, "rating": 4.3},
        {"name": "MacBook", "price": 1299, "category": "电脑", "stock": 20, "rating": 4.7},
        {"name": "AirPods", "price": 179, "category": "耳机", "stock": 100, "rating": 4.2}
    ]
}

helper = jmes(data)

# 价格在500-1000之间的产品
mid_price = helper.filter_by("products", "price >= `500` && price <= `1000`")

# 高评分且有库存的产品
good_products = helper.filter_by("products", "rating > `4.0` && stock > `0`")

# 手机或电脑类别的产品
tech_products = helper.filter_by("products", "category == '手机' || category == '电脑'")
```

### 2. 数据聚合和统计

```python
# 计算总库存
total_stock = jmespath.search("sum(products[].stock)", data)

# 平均价格
avg_price = jmespath.search("avg(products[].price)", data)

# 最高评分
max_rating = jmespath.search("max(products[].rating)", data)

# 最低价格的产品
cheapest = jmespath.search("products[?price == min(products[].price)] | [0]", data)
```

### 3. 排序和分组

```python
# 按价格排序
sorted_by_price = helper.sort_by("products", "price")
sorted_by_price_desc = helper.sort_by("products", "price", reverse=True)

# 按评分排序
sorted_by_rating = helper.sort_by("products", "rating", reverse=True)

# 按类别分组
grouped = helper.group_by("products", "category")
# 结果: {"手机": [...], "平板": [...], "电脑": [...], "耳机": [...]}
```

### 4. 字段提取和重构

```python
# 提取特定字段
product_summary = helper.extract_fields("products", ["name", "price", "rating"])

# 自定义字段映射
custom_format = jmespath.search("""
products[].{
    产品名称: name,
    价格: price,
    评分: rating,
    性价比: rating / (price / `100`)
}
""", data)
```

## 🔧 常用查询模式

### 1. API响应模式

```python
from src.utils.jmespath_helper import CommonJMESPatterns

# 标准API响应结构
api_response = {
    "code": 200,
    "message": "success",
    "data": {...}
}

helper = jmes(api_response)

# 使用预定义模式
code = helper.get_value(CommonJMESPatterns.API_CODE)
message = helper.get_value(CommonJMESPatterns.API_MESSAGE)
data = helper.get_value(CommonJMESPatterns.API_DATA)
```

### 2. 分页数据模式

```python
# 分页响应结构
page_response = {
    "code": 200,
    "data": {
        "items": [...],
        "total": 100,
        "page": 1,
        "size": 10
    }
}

helper = jmes(page_response)

# 分页信息查询
items = helper.get_list(CommonJMESPatterns.PAGE_ITEMS)
total = helper.get_value(CommonJMESPatterns.PAGE_TOTAL)
current_page = helper.get_value(CommonJMESPatterns.PAGE_CURRENT)
```

### 3. 用户数据模式

```python
# 用户响应结构
user_response = {
    "code": 200,
    "data": {
        "user": {
            "id": 123,
            "name": "张三",
            "email": "zhangsan@example.com",
            "profile": {...}
        }
    }
}

helper = jmes(user_response)

# 用户信息查询
user_id = helper.get_value(CommonJMESPatterns.USER_ID)
user_name = helper.get_value(CommonJMESPatterns.USER_NAME)
user_email = helper.get_value(CommonJMESPatterns.USER_EMAIL)
```

## 🎯 性能优化

### 1. 表达式编译

```python
# 频繁使用的查询应该预编译
compiled_expr = jmespath.compile("data.users[?active].name")

# 重复使用编译后的表达式
for response in responses:
    active_names = compiled_expr.search(response)
```

### 2. 查询优化

```python
# 优化前：多次查询
users = jmespath.search("data.users", response)
active_users = [u for u in users if u.get("active")]
names = [u["name"] for u in active_users]

# 优化后：单次查询
names = jmespath.search("data.users[?active].name", response)
```

### 3. 缓存策略

```python
class CachedJMESHelper:
    def __init__(self, data):
        self.data = data
        self._cache = {}

    def search(self, path):
        if path not in self._cache:
            self._cache[path] = jmespath.search(path, self.data)
        return self._cache[path]
```

## 🐛 常见问题和解决方案

### 1. 路径不存在

```python
# 问题：路径不存在时返回None
result = jmespath.search("data.nonexistent", response)  # None

# 解决：使用默认值
result = helper.get_value("data.nonexistent", "默认值")
```

### 2. 类型错误

```python
# 问题：期望列表但得到单个值
items = jmespath.search("data.item", response)  # 可能是单个对象

# 解决：确保返回列表
items = helper.get_list("data.item")  # 总是返回列表
```

### 3. 复杂条件

```python
# 问题：复杂条件难以表达
# 查找年龄在25-35之间且技能包含Python的技术部员工

# 解决：分步查询或使用辅助方法
tech_users = helper.filter_by("users", "department == '技术部'")
python_users = [u for u in tech_users
                if 25 <= u.get("age", 0) <= 35
                and "Python" in u.get("skills", [])]
```

## 📝 最佳实践

### 1. 查询复用

```python
# 定义常用查询
class APIQueries:
    SUCCESS_CODE = "code"
    ERROR_MESSAGE = "error.message"
    USER_LIST = "data.users"
    ACTIVE_USERS = "data.users[?status == 'active']"

    @staticmethod
    def user_by_id(user_id):
        return f"data.users[?id == `{user_id}`] | [0]"
```

### 2. 错误处理

```python
def safe_jmespath_search(data, path, default=None):
    """安全的JMESPath查询"""
    try:
        result = jmespath.search(path, data)
        return result if result is not None else default
    except Exception as e:
        logger.warning(f"JMESPath查询失败: {path}, 错误: {e}")
        return default
```

### 3. 测试验证

```python
def test_jmespath_queries():
    """测试JMESPath查询的正确性"""
    test_data = {
        "users": [
            {"id": 1, "name": "张三", "active": True},
            {"id": 2, "name": "李四", "active": False}
        ]
    }

    # 验证查询结果
    active_users = jmespath.search("users[?active]", test_data)
    assert len(active_users) == 1
    assert active_users[0]["name"] == "张三"
```

## 🔗 参考资源

- [JMESPath官方文档](https://jmespath.org/)
- [JMESPath教程](https://jmespath.org/tutorial.html)
- [JMESPath在线测试](https://jmespath.org/)
- [AWS CLI中的JMESPath](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html#cli-usage-output-format-json)

---

**下一步**: [数据驱动测试](./data-driven.md) | [Mock服务器](./mock-server.md)
