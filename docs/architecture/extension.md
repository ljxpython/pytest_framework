# 🔌 扩展机制 - 让框架为你所用

> "好的框架不是限制你，而是给你无限可能。"

想象一下，你有一个超级灵活的乐高积木盒，可以搭建任何你想要的东西。这就是我们框架的扩展机制！

## 🎯 为什么要扩展？

### 真实场景
你是不是遇到过这些情况：
- 😤 "这个断言方法不够用，我需要验证特殊的业务规则"
- 🤔 "我们公司有自己的认证方式，框架不支持"
- 😅 "测试数据需要从我们的内部系统获取"
- 🙄 "报告格式不符合老板的要求"

别担心！我们的扩展机制就是为了解决这些"个性化需求"而生的。

## 🛠️ 扩展点大揭秘

### 1. 自定义断言 - 让验证更贴心

还在为复杂的业务规则验证发愁？来看看这个：

```python
from src.utils.assertion import EnhancedAssertion

class BusinessAssertion(EnhancedAssertion):
    """业务专用断言 - 老板再也不用担心我的验证了"""

    def assert_user_permission(self, user_data, required_permission):
        """验证用户权限 - 比保安还严格"""
        permissions = user_data.get("permissions", [])
        if required_permission not in permissions:
            raise AssertionError(f"用户缺少权限: {required_permission}")
        self.logger.info(f"✅ 权限验证通过: {required_permission}")
        return self

    def assert_money_format(self, amount):
        """验证金额格式 - 财务部门的最爱"""
        import re
        if not re.match(r'^\d+\.\d{2}$', str(amount)):
            raise AssertionError(f"金额格式错误: {amount}")
        self.logger.info(f"💰 金额格式正确: {amount}")
        return self

    def assert_business_rule(self, data, rule_name):
        """验证业务规则 - 你的规则你做主"""
        rules = {
            "vip_discount": lambda d: d.get("discount", 0) >= 0.1,
            "order_limit": lambda d: d.get("amount", 0) <= 10000,
            "working_hours": lambda d: 9 <= int(d.get("hour", 0)) <= 18
        }

        if rule_name not in rules:
            raise AssertionError(f"未知业务规则: {rule_name}")

        if not rules[rule_name](data):
            raise AssertionError(f"业务规则验证失败: {rule_name}")

        self.logger.info(f"🎯 业务规则验证通过: {rule_name}")
        return self

# 使用起来超级爽
def test_vip_user_order():
    response = client.post("/orders", json=order_data)

    (BusinessAssertion(response.json())
     .assert_jmespath("code", 200)
     .assert_user_permission(response.json()["user"], "place_order")
     .assert_money_format(response.json()["amount"])
     .assert_business_rule(response.json(), "vip_discount"))
```

### 2. 自定义数据源 - 数据哪里都能来

公司有特殊的数据存储？没问题！

```python
from src.utils.data_driver import DataDriver

class CompanyDataDriver(DataDriver):
    """公司专用数据驱动器 - 连接一切数据源"""

    def load_from_crm(self, customer_type="vip"):
        """从CRM系统加载客户数据"""
        # 这里连接你们的CRM系统
        crm_api = CRMClient(api_key="your-secret-key")
        customers = crm_api.get_customers(type=customer_type)

        return [
            {
                "name": customer.name,
                "email": customer.email,
                "level": customer.vip_level,
                "credit": customer.credit_score
            }
            for customer in customers
        ]

    def load_from_redis(self, pattern="test:*"):
        """从Redis缓存加载数据"""
        import redis
        r = redis.Redis(host='localhost', port=6379, db=0)

        keys = r.keys(pattern)
        return [
            {
                "key": key.decode(),
                "value": r.get(key).decode(),
                "ttl": r.ttl(key)
            }
            for key in keys
        ]

    def generate_realistic_orders(self, count=10):
        """生成真实的订单数据 - 比faker更懂业务"""
        import random
        from datetime import datetime, timedelta

        products = ["iPhone 15", "MacBook Pro", "AirPods", "iPad"]
        statuses = ["pending", "paid", "shipped", "delivered"]

        orders = []
        for i in range(count):
            order_date = datetime.now() - timedelta(days=random.randint(0, 30))
            orders.append({
                "order_id": f"ORD-{order_date.strftime('%Y%m%d')}-{i:04d}",
                "product": random.choice(products),
                "quantity": random.randint(1, 5),
                "price": round(random.uniform(99, 2999), 2),
                "status": random.choice(statuses),
                "order_date": order_date.isoformat(),
                "customer_id": f"CUST-{random.randint(1000, 9999)}"
            })

        return orders

# 使用示例
@pytest.mark.parametrize("customer", CompanyDataDriver().load_from_crm("premium"))
def test_premium_customer_workflow(customer):
    """测试高级客户工作流 - 用真实数据测试"""
    # 使用真实的客户数据进行测试
    response = client.post("/orders", json={
        "customer_id": customer["id"],
        "items": [{"product": "premium_service", "quantity": 1}]
    })

    assert response.status_code == 201
```

### 3. 自定义认证 - 安全你说了算

```python
from src.client.base_auth import AuthStrategy

class WeChatAuth(AuthStrategy):
    """微信认证 - 因为我们就是这么潮"""

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.access_token = None

    def authenticate(self, client):
        """微信认证流程"""
        # 获取access_token
        auth_response = client.post("/wechat/auth", json={
            "app_id": self.app_id,
            "app_secret": self.app_secret
        })

        self.access_token = auth_response.json()["access_token"]

        # 设置认证头
        client.session.headers.update({
            "Authorization": f"WeChat {self.access_token}",
            "X-App-ID": self.app_id
        })

class CompanySSO(AuthStrategy):
    """公司单点登录 - 一次登录，处处通行"""

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def authenticate(self, client):
        """SSO认证流程"""
        # 第一步：获取SSO票据
        sso_response = client.post("/sso/login", json={
            "username": self.username,
            "password": self.password
        })

        ticket = sso_response.json()["ticket"]

        # 第二步：用票据换取访问令牌
        token_response = client.post("/sso/exchange", json={
            "ticket": ticket,
            "service": "api-testing"
        })

        access_token = token_response.json()["access_token"]

        # 设置认证信息
        client.session.headers.update({
            "Authorization": f"Bearer {access_token}",
            "X-SSO-User": self.username
        })

# 使用起来就是这么简单
def test_with_wechat_auth():
    client = BaseClient("https://api.example.com")
    auth = WeChatAuth("your-app-id", "your-app-secret")
    auth.authenticate(client)

    response = client.get("/user/profile")
    assert response.status_code == 200
```

## 🎨 插件开发指南

### 创建你的第一个插件

想要创建一个插件？跟着这个步骤，5分钟搞定：

```python
# plugins/awesome_plugin.py
"""
超棒插件 - 让测试更有趣
"""

import pytest
from src.utils.log_moudle import logger

class AwesomePlugin:
    """超棒的插件类"""

    def __init__(self):
        self.test_count = 0
        self.emoji_map = {
            "PASSED": "🎉",
            "FAILED": "😭",
            "SKIPPED": "🙄"
        }

    @pytest.hookimpl
    def pytest_runtest_setup(self, item):
        """测试开始前的准备工作"""
        self.test_count += 1
        logger.info(f"🚀 开始第 {self.test_count} 个测试: {item.name}")

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item, nextitem):
        """测试结束后的清理工作"""
        logger.info(f"🧹 测试 {item.name} 清理完成")

    @pytest.hookimpl
    def pytest_runtest_logreport(self, report):
        """测试结果报告"""
        if report.when == "call":
            emoji = self.emoji_map.get(report.outcome, "🤔")
            logger.info(f"{emoji} 测试结果: {report.outcome}")

            if report.outcome == "FAILED":
                logger.error(f"💔 失败原因: {report.longrepr}")

# conftest.py - 注册插件
def pytest_configure(config):
    """注册我们的超棒插件"""
    config.pluginmanager.register(AwesomePlugin(), "awesome")
```

### 高级插件示例

```python
# plugins/performance_monitor.py
"""
性能监控插件 - 让慢测试无处遁形
"""

import time
import pytest
from src.utils.log_moudle import logger

class PerformanceMonitor:
    """性能监控器 - 测试界的体检医生"""

    def __init__(self):
        self.slow_tests = []
        self.test_times = {}
        self.warning_threshold = 5.0  # 5秒警告线
        self.danger_threshold = 10.0   # 10秒危险线

    @pytest.hookimpl
    def pytest_runtest_setup(self, item):
        """记录测试开始时间"""
        self.test_times[item.nodeid] = time.time()

    @pytest.hookimpl
    def pytest_runtest_teardown(self, item, nextitem):
        """计算测试耗时"""
        start_time = self.test_times.get(item.nodeid)
        if start_time:
            duration = time.time() - start_time

            if duration > self.danger_threshold:
                emoji = "🐌"
                level = "DANGER"
            elif duration > self.warning_threshold:
                emoji = "⚠️"
                level = "WARNING"
            else:
                emoji = "⚡"
                level = "FAST"

            logger.info(f"{emoji} [{level}] {item.name}: {duration:.2f}s")

            if duration > self.warning_threshold:
                self.slow_tests.append({
                    "name": item.name,
                    "duration": duration,
                    "level": level
                })

    @pytest.hookimpl
    def pytest_sessionfinish(self, session, exitstatus):
        """测试结束后的性能报告"""
        if self.slow_tests:
            logger.warning("🐌 发现慢测试，需要优化：")
            for test in sorted(self.slow_tests, key=lambda x: x["duration"], reverse=True):
                logger.warning(f"  - {test['name']}: {test['duration']:.2f}s ({test['level']})")
        else:
            logger.info("🚀 所有测试都很快，棒棒哒！")
```

## 🎪 Hook系统 - 事件驱动的魔法

我们的Hook系统就像是一个事件派对，每个重要时刻都会发出邀请：

```python
# hooks/test_lifecycle.py
"""
测试生命周期钩子 - 见证每个测试的一生
"""

class TestLifecycleHooks:
    """测试生命周期钩子管理器"""

    def __init__(self):
        self.hooks = {
            "before_test": [],
            "after_test": [],
            "before_request": [],
            "after_response": [],
            "on_error": []
        }

    def register_hook(self, event, callback):
        """注册钩子函数"""
        if event in self.hooks:
            self.hooks[event].append(callback)

    def trigger_hook(self, event, *args, **kwargs):
        """触发钩子事件"""
        for callback in self.hooks.get(event, []):
            try:
                callback(*args, **kwargs)
            except Exception as e:
                logger.error(f"钩子执行失败 {event}: {e}")

# 全局钩子管理器
lifecycle = TestLifecycleHooks()

# 注册一些有趣的钩子
def log_test_start(test_name):
    """测试开始日志"""
    logger.info(f"🎬 测试开始: {test_name}")

def log_test_end(test_name, result):
    """测试结束日志"""
    emoji = "🎉" if result == "PASSED" else "😭"
    logger.info(f"{emoji} 测试结束: {test_name} - {result}")

def log_api_request(method, url, data=None):
    """API请求日志"""
    logger.info(f"📤 API请求: {method} {url}")
    if data:
        logger.debug(f"📦 请求数据: {data}")

def log_api_response(response):
    """API响应日志"""
    logger.info(f"📥 API响应: {response.status_code}")

# 注册钩子
lifecycle.register_hook("before_test", log_test_start)
lifecycle.register_hook("after_test", log_test_end)
lifecycle.register_hook("before_request", log_api_request)
lifecycle.register_hook("after_response", log_api_response)
```

## 🚀 实战案例：构建企业级扩展

让我们来看一个真实的企业级扩展案例：

```python
# extensions/enterprise_suite.py
"""
企业级扩展套件 - 一站式解决方案
"""

class EnterpriseSuite:
    """企业级功能套件"""

    def __init__(self, config):
        self.config = config
        self.audit_logger = AuditLogger()
        self.security_checker = SecurityChecker()
        self.performance_monitor = PerformanceMonitor()

    def setup_enterprise_features(self, client):
        """设置企业级功能"""
        # 1. 安全检查
        self.security_checker.validate_ssl(client)

        # 2. 审计日志
        self.audit_logger.start_session()

        # 3. 性能监控
        self.performance_monitor.start_monitoring()

        # 4. 合规检查
        self.ensure_compliance()

    def ensure_compliance(self):
        """确保合规性"""
        # 检查是否符合GDPR、SOX等法规要求
        compliance_rules = [
            "data_encryption",
            "access_logging",
            "retention_policy"
        ]

        for rule in compliance_rules:
            if not self.check_compliance_rule(rule):
                raise ComplianceError(f"违反合规规则: {rule}")

# 使用企业级扩展
def test_with_enterprise_features():
    """使用企业级功能的测试"""
    enterprise = EnterpriseSuite(config)
    client = BaseClient("https://api.company.com")

    # 启用企业级功能
    enterprise.setup_enterprise_features(client)

    # 正常的测试逻辑
    response = client.get("/sensitive-data")
    assert response.status_code == 200

    # 企业级验证
    enterprise.audit_logger.log_data_access(response.json())
    enterprise.security_checker.validate_response(response)
```

## 💡 扩展最佳实践

### 1. 保持简单
```python
# ✅ 好的扩展 - 简单明了
class SimpleValidator:
    def validate_email(self, email):
        return "@" in email and "." in email

# ❌ 过度复杂的扩展
class OverComplexValidator:
    def __init__(self, config, logger, cache, db, redis, kafka, elasticsearch):
        # 太多依赖了...
```

### 2. 文档先行
```python
class AwesomeExtension:
    """
    超棒的扩展

    这个扩展可以让你的测试变得更棒！

    使用方法:
        ext = AwesomeExtension()
        ext.make_awesome(your_test)

    注意事项:
        - 需要Python 3.8+
        - 不要在生产环境使用
        - 记得给我点赞 ⭐
    """
```

### 3. 向后兼容
```python
def new_feature(data, new_param=None):
    """新功能，但保持向后兼容"""
    if new_param is None:
        # 使用旧的行为
        return old_behavior(data)
    else:
        # 使用新的行为
        return new_behavior(data, new_param)
```

## 🎯 总结

扩展机制让我们的框架变成了一个"变形金刚"：
- 🔧 **自定义断言** - 让验证更贴合业务
- 📊 **自定义数据源** - 数据从哪里来都不是问题
- 🔐 **自定义认证** - 安全方案你说了算
- 🎪 **Hook系统** - 在关键时刻插入你的逻辑
- 🚀 **插件机制** - 功能无限扩展

记住：**好的扩展不是炫技，而是解决实际问题。**

开始创建你的第一个扩展吧！让框架真正为你所用！

---

**下一步**: 试试创建一个简单的自定义断言，体验扩展的乐趣！
