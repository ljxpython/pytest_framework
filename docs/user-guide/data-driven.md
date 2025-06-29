# 📊 数据驱动测试 - 让数据为你打工

> "数据驱动测试：一套逻辑，千种场景！"

还在为每个测试场景写重复代码？还在手动构造测试数据？别累坏自己！数据驱动测试让你写一次逻辑，测试无数场景。

## 🎯 什么是数据驱动测试？

### 传统测试 vs 数据驱动测试

```python
# 😫 传统方式 - 重复到想哭
def test_create_user_zhang():
    response = client.post("/users", json={"name": "张三", "age": 25})
    assert response.status_code == 201

def test_create_user_li():
    response = client.post("/users", json={"name": "李四", "age": 30})
    assert response.status_code == 201

def test_create_user_wang():
    response = client.post("/users", json={"name": "王五", "age": 28})
    assert response.status_code == 201

# 😱 如果有100个用户要测试...你会疯掉的！

# 🎉 数据驱动方式 - 一次编写，处处运行
@pytest.mark.parametrize("user_data", load_test_data("users.json"))
def test_create_user(self, user_data):
    response = self.client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["name"] == user_data["name"]

# 一个测试方法，测试所有用户数据！
```

## 📁 数据源大全 - 想要什么格式都有

### 1. JSON数据 - 程序员的最爱

```json
// data/users.json
[
  {
    "name": "张三",
    "email": "zhangsan@example.com",
    "age": 25,
    "department": "技术部",
    "skills": ["Python", "Java"],
    "active": true
  },
  {
    "name": "李四",
    "email": "lisi@example.com",
    "age": 30,
    "department": "产品部",
    "skills": ["产品设计", "用户研究"],
    "active": true
  },
  {
    "name": "王五",
    "email": "wangwu@example.com",
    "age": 28,
    "department": "技术部",
    "skills": ["Python", "Go"],
    "active": false
  }
]
```

```python
# 使用JSON数据
from src.utils.data_driver import load_test_data

@pytest.mark.parametrize("user", load_test_data("users.json"))
def test_user_creation(self, user):
    """测试用户创建 - JSON数据驱动"""
    response = self.client.post("/users", json=user)

    assert response.status_code == 201
    assert response.json()["name"] == user["name"]
    assert response.json()["email"] == user["email"]
```

### 2. YAML数据 - 人类友好格式

```yaml
# data/test_scenarios.yaml
user_creation_tests:
  - name: "正常用户创建"
    description: "使用有效数据创建用户"
    input:
      name: "张三"
      email: "zhangsan@example.com"
      age: 25
    expected:
      status_code: 201
      response_contains: ["id", "name", "email"]

  - name: "邮箱格式错误"
    description: "使用无效邮箱格式"
    input:
      name: "李四"
      email: "invalid-email"
      age: 30
    expected:
      status_code: 400
      error_message: "邮箱格式无效"

login_tests:
  - scenario: "成功登录"
    username: "admin"
    password: "password123"
    expected_result: "success"

  - scenario: "密码错误"
    username: "admin"
    password: "wrong_password"
    expected_result: "failed"
```

```python
# 使用YAML数据
@pytest.mark.parametrize("test_case", load_test_data("test_scenarios.yaml")["user_creation_tests"])
def test_user_creation_scenarios(self, test_case):
    """测试用户创建场景 - YAML数据驱动"""
    print(f"🧪 测试场景: {test_case['name']}")

    response = self.client.post("/users", json=test_case["input"])

    # 验证状态码
    assert response.status_code == test_case["expected"]["status_code"]

    # 验证响应内容
    if "response_contains" in test_case["expected"]:
        for field in test_case["expected"]["response_contains"]:
            assert field in response.json()
```

### 3. Excel数据 - 产品经理的最爱

```python
# data/user_test_cases.xlsx
# 表格内容：
# | 姓名 | 邮箱 | 年龄 | 部门 | 期望状态码 | 备注 |
# | 张三 | zhangsan@example.com | 25 | 技术部 | 201 | 正常用户 |
# | 李四 | invalid-email | 30 | 产品部 | 400 | 邮箱格式错误 |

from src.utils.data_driver import data_driver

@pytest.mark.parametrize("test_case", data_driver.load_excel("user_test_cases.xlsx", "用户测试"))
def test_user_from_excel(self, test_case):
    """测试用户创建 - Excel数据驱动"""
    user_data = {
        "name": test_case["姓名"],
        "email": test_case["邮箱"],
        "age": test_case["年龄"],
        "department": test_case["部门"]
    }

    response = self.client.post("/users", json=user_data)

    # 验证期望的状态码
    assert response.status_code == test_case["期望状态码"]

    print(f"✅ {test_case['备注']}: {test_case['姓名']} - {response.status_code}")
```

### 4. CSV数据 - 简单实用

```csv
# data/products.csv
name,price,category,stock,active
iPhone 15,999.99,手机,100,true
MacBook Pro,1999.99,电脑,50,true
AirPods,199.99,耳机,200,true
iPad,599.99,平板,80,false
```

```python
@pytest.mark.parametrize("product", data_driver.load_csv("products.csv"))
def test_product_creation(self, product):
    """测试商品创建 - CSV数据驱动"""
    response = self.client.post("/products", json=product)

    if product["active"] == "true":
        assert response.status_code == 201
        assert response.json()["name"] == product["name"]
    else:
        # 非活跃商品应该创建失败
        assert response.status_code == 400
```

## 🎲 动态数据生成 - 让Faker为你打工

### 基础数据生成

```python
from src.utils.data_driver import data_driver

# 定义数据模板
user_template = {
    "name": "faker.name",           # 随机姓名
    "email": "faker.email",         # 随机邮箱
    "phone": "faker.phone_number",  # 随机电话
    "address": "faker.address",     # 随机地址
    "age": 25,                      # 固定值
    "department": "技术部"           # 固定值
}

# 生成测试数据
test_users = data_driver.generate_test_data(user_template, count=10)

@pytest.mark.parametrize("user", test_users)
def test_dynamic_user_creation(self, user):
    """测试用户创建 - 动态数据生成"""
    response = self.client.post("/users", json=user)
    assert response.status_code == 201

    # 验证生成的数据格式
    assert "@" in user["email"]  # 邮箱包含@
    assert len(user["name"]) > 0  # 姓名不为空
    assert user["age"] == 25      # 固定值正确
```

### 高级数据生成

```python
# 复杂的数据模板
order_template = {
    "order_id": "faker.uuid4",
    "customer": {
        "name": "faker.name",
        "email": "faker.email",
        "phone": "faker.phone_number"
    },
    "items": [
        {
            "product_name": "faker.word",
            "quantity": "faker.random_int:1:10",
            "price": "faker.pyfloat:2:2:True:10:1000"
        }
    ],
    "shipping_address": {
        "street": "faker.street_address",
        "city": "faker.city",
        "postal_code": "faker.postcode"
    },
    "order_date": "faker.date_time_this_year",
    "status": "faker.random_element:pending,paid,shipped,delivered"
}

# 生成复杂订单数据
test_orders = data_driver.generate_test_data(order_template, count=5)

@pytest.mark.parametrize("order", test_orders)
def test_order_creation(self, order):
    """测试订单创建 - 复杂数据生成"""
    response = self.client.post("/orders", json=order)
    assert response.status_code == 201

    # 验证订单数据
    assert len(order["order_id"]) == 36  # UUID长度
    assert order["items"][0]["quantity"] >= 1
    assert order["items"][0]["price"] >= 10
```

### 中文数据生成

```python
# 中文数据模板
chinese_user_template = {
    "name": "faker.name:zh_CN",           # 中文姓名
    "company": "faker.company:zh_CN",     # 中文公司名
    "address": "faker.address:zh_CN",     # 中文地址
    "phone": "faker.phone_number:zh_CN",  # 中国手机号
    "id_card": "faker.ssn:zh_CN",         # 身份证号
    "email": "faker.email",               # 邮箱（英文）
    "age": "faker.random_int:18:65"       # 年龄范围
}

chinese_users = data_driver.generate_test_data(chinese_user_template, count=20)

@pytest.mark.parametrize("user", chinese_users)
def test_chinese_user_creation(self, user):
    """测试中文用户创建"""
    response = self.client.post("/users", json=user)
    assert response.status_code == 201

    # 验证中文数据
    assert len(user["name"]) >= 2  # 中文姓名至少2个字符
    assert user["phone"].startswith(("13", "14", "15", "16", "17", "18", "19"))
```

## 🎪 数据组合和关联

### 数据依赖处理

```python
class TestUserOrderWorkflow:
    """用户订单工作流测试 - 数据有依赖关系"""

    def test_complete_user_journey(self):
        """完整的用户旅程测试"""

        # 1. 生成用户数据
        user_template = {
            "name": "faker.name",
            "email": "faker.email",
            "phone": "faker.phone_number"
        }
        user_data = data_driver.generate_test_data(user_template, count=1)[0]

        # 2. 创建用户
        user_response = self.client.post("/users", json=user_data)
        assert user_response.status_code == 201
        user_id = user_response.json()["id"]

        # 3. 生成订单数据（依赖用户ID）
        order_data = {
            "user_id": user_id,  # 使用刚创建的用户ID
            "items": [
                {
                    "product_id": 1001,
                    "quantity": 2,
                    "price": 99.99
                }
            ],
            "total_amount": 199.98
        }

        # 4. 创建订单
        order_response = self.client.post("/orders", json=order_data)
        assert order_response.status_code == 201

        # 5. 验证订单关联
        order_id = order_response.json()["id"]
        order_detail = self.client.get(f"/orders/{order_id}")
        assert order_detail.json()["user_id"] == user_id
```

### 批量数据生成

```python
def generate_related_test_data():
    """生成相关联的测试数据"""

    # 生成公司数据
    companies = data_driver.generate_test_data({
        "name": "faker.company",
        "industry": "faker.random_element:IT,金融,教育,医疗",
        "size": "faker.random_element:小型,中型,大型"
    }, count=5)

    # 为每个公司生成员工数据
    all_employees = []
    for company in companies:
        employees = data_driver.generate_test_data({
            "name": "faker.name",
            "email": "faker.email",
            "position": "faker.job",
            "company_name": company["name"],  # 关联公司
            "salary": "faker.random_int:5000:50000"
        }, count=random.randint(3, 8))

        all_employees.extend(employees)

    return companies, all_employees

@pytest.mark.parametrize("employee", generate_related_test_data()[1])
def test_employee_creation(self, employee):
    """测试员工创建 - 关联公司数据"""
    response = self.client.post("/employees", json=employee)
    assert response.status_code == 201
    assert response.json()["company_name"] == employee["company_name"]
```

## 🎯 数据过滤和选择

### 条件数据过滤

```python
# 加载所有用户数据
all_users = load_test_data("users.json")

# 过滤活跃用户
active_users = [user for user in all_users if user.get("active", True)]

# 过滤技术部员工
tech_users = [user for user in all_users if user.get("department") == "技术部"]

# 过滤年龄范围
young_users = [user for user in all_users if 20 <= user.get("age", 0) <= 30]

@pytest.mark.parametrize("user", active_users)
def test_active_user_features(self, user):
    """测试活跃用户功能"""
    response = self.client.get(f"/users/{user['id']}/features")
    assert response.status_code == 200
    assert response.json()["active"] == True

@pytest.mark.parametrize("user", tech_users)
def test_tech_user_permissions(self, user):
    """测试技术部用户权限"""
    response = self.client.get(f"/users/{user['id']}/permissions")
    assert response.status_code == 200
    assert "code_access" in response.json()["permissions"]
```

### 数据分组测试

```python
from itertools import groupby

# 按部门分组测试
all_users = load_test_data("users.json")
users_by_dept = {}
for dept, users in groupby(all_users, key=lambda x: x["department"]):
    users_by_dept[dept] = list(users)

class TestDepartmentFeatures:
    """按部门测试功能"""

    @pytest.mark.parametrize("user", users_by_dept.get("技术部", []))
    def test_tech_department_features(self, user):
        """测试技术部专属功能"""
        response = self.client.get(f"/tech/features",
                                 headers={"User-ID": str(user["id"])})
        assert response.status_code == 200

    @pytest.mark.parametrize("user", users_by_dept.get("产品部", []))
    def test_product_department_features(self, user):
        """测试产品部专属功能"""
        response = self.client.get(f"/product/features",
                                 headers={"User-ID": str(user["id"])})
        assert response.status_code == 200
```

## 🎨 数据模板进阶技巧

### 自定义数据生成器

```python
from faker import Faker
import random

fake = Faker('zh_CN')

def custom_data_generators():
    """自定义数据生成器"""

    def generate_chinese_mobile():
        """生成中国手机号"""
        prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                   '150', '151', '152', '153', '155', '156', '157', '158', '159',
                   '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
        prefix = random.choice(prefixes)
        suffix = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        return prefix + suffix

    def generate_realistic_email(name):
        """根据姓名生成真实的邮箱"""
        domains = ['qq.com', '163.com', '126.com', 'gmail.com', 'hotmail.com']
        # 简单的拼音转换（实际项目中可以用pypinyin）
        name_pinyin = name.lower().replace(' ', '')
        domain = random.choice(domains)
        return f"{name_pinyin}{random.randint(1, 999)}@{domain}"

    def generate_id_card():
        """生成身份证号"""
        return fake.ssn()

    return {
        "mobile": generate_chinese_mobile,
        "realistic_email": generate_realistic_email,
        "id_card": generate_id_card
    }

# 使用自定义生成器
generators = custom_data_generators()

realistic_user_template = {
    "name": "faker.name:zh_CN",
    "mobile": generators["mobile"],
    "id_card": generators["id_card"],
    "age": "faker.random_int:18:65",
    "city": "faker.city:zh_CN"
}

# 生成真实的用户数据
realistic_users = []
for i in range(10):
    user = {}
    for key, value in realistic_user_template.items():
        if callable(value):
            user[key] = value()
        elif isinstance(value, str) and value.startswith("faker."):
            # 处理faker表达式
            user[key] = fake.name()  # 简化处理
        else:
            user[key] = value

    # 生成基于姓名的邮箱
    user["email"] = generators["realistic_email"](user["name"])
    realistic_users.append(user)

@pytest.mark.parametrize("user", realistic_users)
def test_realistic_user_data(self, user):
    """测试真实用户数据"""
    response = self.client.post("/users", json=user)
    assert response.status_code == 201

    # 验证数据真实性
    assert len(user["mobile"]) == 11
    assert user["mobile"].startswith(('13', '15', '18'))
    assert '@' in user["email"]
```

## 💡 数据驱动最佳实践

### 1. 数据文件组织

```
data/
├── users/              # 用户相关数据
│   ├── normal_users.json
│   ├── vip_users.json
│   └── invalid_users.json
├── products/           # 商品相关数据
│   ├── electronics.csv
│   ├── books.yaml
│   └── clothing.xlsx
├── scenarios/          # 测试场景数据
│   ├── happy_path.yaml
│   ├── edge_cases.json
│   └── error_cases.yaml
└── templates/          # 数据模板
    ├── user_template.py
    └── order_template.py
```

### 2. 数据版本管理

```python
# data/version_info.yaml
version: "1.2.0"
last_updated: "2024-01-15"
changes:
  - "添加VIP用户测试数据"
  - "更新商品价格信息"
  - "修复邮箱格式问题"

compatibility:
  min_framework_version: "1.0.0"
  max_framework_version: "2.0.0"
```

### 3. 数据清理策略

```python
@pytest.fixture(autouse=True)
def data_cleanup():
    """自动数据清理"""
    created_resources = []

    yield created_resources

    # 测试结束后清理创建的数据
    for resource in created_resources:
        try:
            if resource["type"] == "user":
                client.delete(f"/users/{resource['id']}")
            elif resource["type"] == "order":
                client.delete(f"/orders/{resource['id']}")
        except Exception as e:
            logger.warning(f"清理资源失败: {e}")
```

## 🎯 总结

数据驱动测试让你的测试变得：
- 🎯 **高效** - 一套逻辑测试多种场景
- 🔄 **可维护** - 数据和逻辑分离
- 🎲 **灵活** - 支持多种数据源和生成方式
- 🎪 **真实** - 使用真实或接近真实的数据
- 🧹 **干净** - 自动化数据清理

记住：**好的测试数据是测试成功的一半！**

现在就开始用数据驱动测试，让你的测试覆盖更多场景，发现更多问题！

---

**小贴士**: 数据文件记得加到版本控制里，但敏感数据要小心处理哦！
