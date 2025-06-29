# ❓ 常见问题解答

本文档收集了使用 Pytest Framework 过程中的常见问题和解决方案。

## 🚀 快速开始问题

### Q: 安装后运行测试报错 "ModuleNotFoundError"
**A:** 这通常是Python路径问题。解决方案：

```bash
# 方法1: 设置PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 方法2: 在项目根目录运行
python -m pytest tests/

# 方法3: 使用相对导入
# 在测试文件中使用 from src.xxx import xxx
```

### Q: 为什么选择JMESPath而不是JSONPath？
**A:** JMESPath有以下优势：
- **语法更简洁**: `users[?active].name` vs `$.users[?(@.active)].name`
- **功能更强大**: 支持函数、排序、投影等高级功能
- **性能更好**: 编译型查询，比解释型JSONPath快
- **生态成熟**: AWS CLI等大型项目的首选
- **可读性强**: 声明式语法，更容易理解和维护

### Q: 如何配置不同的测试环境？
**A:** 编辑 `conf/settings.yaml` 文件：

```yaml
boe:  # 开发环境
  API:
    base_url: "https://dev-api.example.com"
    timeout: 30

test:  # 测试环境
  API:
    base_url: "https://test-api.example.com"
    timeout: 60

# 切换环境
ENV=test pytest tests/
```

## 🔍 JMESPath使用问题

### Q: JMESPath查询返回None怎么办？
**A:** 使用安全的查询方法：

```python
# 问题：直接查询可能返回None
result = jmespath.search("data.nonexistent", response)  # None

# 解决：使用默认值
from src.utils.jmespath_helper import jmes
helper = jmes(response)
result = helper.get_value("data.nonexistent", "默认值")
```

### Q: 如何查询数组中的特定元素？
**A:** 使用条件过滤：

```python
# 查询活跃用户
active_users = helper.filter_by("users", "status == 'active'")

# 查询特定ID的用户
user = helper.find_first("users", "id == `123`")

# 查询年龄大于25的用户
young_users = helper.filter_by("users", "age > `25`")
```

### Q: JMESPath复杂查询如何调试？
**A:** 使用在线工具和日志：

```python
# 1. 使用在线JMESPath测试工具
# https://jmespath.org/

# 2. 启用调试日志
import logging
logging.getLogger('jmespath_helper').setLevel(logging.DEBUG)

# 3. 分步查询
data = helper.get_value("data")
users = helper.get_list("data.users")
filtered = helper.filter_by("data.users", "active == `true`")
```

## 🌐 HTTP客户端问题

### Q: 如何处理HTTPS证书问题？
**A:** 配置SSL验证：

```python
# 忽略SSL证书验证（仅测试环境）
client = BaseClient("https://api.example.com")
client.session.verify = False

# 使用自定义证书
client.session.verify = "/path/to/cert.pem"

# 配置代理
client.session.proxies = {
    "http": "http://proxy.example.com:8080",
    "https": "https://proxy.example.com:8080"
}
```

### Q: 如何设置请求超时？
**A:** 多种超时设置方式：

```python
# 1. 客户端级别超时
client = BaseClient("https://api.example.com", timeout=30)

# 2. 请求级别超时
response = client.get("/users", timeout=60)

# 3. 分别设置连接和读取超时
response = client.get("/users", timeout=(5, 30))  # (连接超时, 读取超时)
```

### Q: 如何处理认证？
**A:** 框架支持多种认证方式：

```python
from src.client.base_auth import BearerAuth, BasicAuth

# Bearer Token
client.session.auth = BearerAuth("your-token")

# Basic认证
client.session.auth = BasicAuth("username", "password")

# API Key
client.session.headers.update({"X-API-Key": "your-key"})

# 自定义认证头
client.session.headers.update({"Authorization": "Custom your-token"})
```

## 📊 数据驱动问题

### Q: 如何处理大量测试数据？
**A:** 使用分批处理和优化策略：

```python
# 1. 分批加载数据
def load_data_in_batches(file_path, batch_size=100):
    all_data = load_test_data(file_path)
    for i in range(0, len(all_data), batch_size):
        yield all_data[i:i + batch_size]

# 2. 使用生成器
@pytest.mark.parametrize("user_data",
    (data for batch in load_data_in_batches("large_users.json") for data in batch))
def test_user_creation(self, user_data):
    pass

# 3. 过滤数据
filtered_data = [data for data in all_data if data.get("active")]
```

### Q: 如何生成关联的测试数据？
**A:** 使用数据依赖和模板：

```python
# 生成关联数据
def generate_related_data():
    # 先生成用户
    user = data_driver.generate_test_data({
        "id": "faker.random_int",
        "name": "faker.name",
        "email": "faker.email"
    }, count=1)[0]

    # 再生成该用户的订单
    order = {
        "user_id": user["id"],
        "order_id": f"ORD-{user['id']}-{random.randint(1000, 9999)}",
        "amount": random.uniform(10, 1000)
    }

    return {"user": user, "order": order}
```

## 🎭 Mock服务问题

### Q: Mock服务器端口冲突怎么办？
**A:** 使用动态端口分配：

```python
import socket

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

# 使用动态端口
mock_server = MockServer(port=get_free_port())
```

### Q: 如何模拟复杂的API行为？
**A:** 使用动态响应和状态管理：

```python
class StatefulMockServer:
    def __init__(self):
        self.state = {}
        self.call_count = {}

    def dynamic_response(self, request):
        path = request.path
        self.call_count[path] = self.call_count.get(path, 0) + 1

        # 根据调用次数返回不同响应
        if self.call_count[path] == 1:
            return {"status": "processing"}
        elif self.call_count[path] == 2:
            return {"status": "completed"}
        else:
            return {"status": "error", "message": "Too many requests"}
```

## ⚡ 性能测试问题

### Q: 性能测试结果不稳定怎么办？
**A:** 使用多次测试和统计分析：

```python
def stable_performance_test(request_func, iterations=5):
    results = []

    for i in range(iterations):
        metrics = load_test(request_func, concurrent_users=10, total_requests=100)
        results.append(metrics.avg_response_time)

    # 计算统计值
    avg_time = sum(results) / len(results)
    std_dev = (sum((x - avg_time) ** 2 for x in results) / len(results)) ** 0.5

    # 使用平均值和标准差进行判断
    assert avg_time < 1.0
    assert std_dev < 0.2  # 标准差小于0.2秒，说明结果稳定
```

### Q: 如何测试API的并发安全性？
**A:** 使用并发测试模式：

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def test_concurrent_safety():
    results = []
    errors = []

    def concurrent_request():
        try:
            response = client.post("/api/counter/increment")
            results.append(response.json()["count"])
        except Exception as e:
            errors.append(str(e))

    # 并发执行
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(concurrent_request) for _ in range(100)]
        for future in futures:
            future.result()

    # 验证结果
    assert len(errors) == 0  # 没有错误
    assert len(set(results)) == len(results)  # 所有结果都不同（如果是计数器）
```

## 🔧 配置和环境问题

### Q: 如何管理敏感信息？
**A:** 使用环境变量和密钥文件：

```bash
# 1. 使用环境变量
export API_SECRET_KEY="your-secret-key"
export DB_PASSWORD="your-password"

# 2. 使用.env文件（不要提交到版本控制）
echo "API_SECRET_KEY=your-secret-key" > .env
echo "DB_PASSWORD=your-password" >> .env

# 3. 使用密钥管理服务
# AWS Secrets Manager, Azure Key Vault, etc.
```

```python
# 在代码中使用
import os
from src.utils.environment import get_config

# 优先使用环境变量
secret_key = os.getenv("API_SECRET_KEY") or get_config("API.secret_key")
```

### Q: 如何在CI/CD中运行测试？
**A:** 配置环境变量和测试命令：

```yaml
# GitHub Actions示例
- name: Run tests
  env:
    ENV: test
    API_BASE_URL: https://test-api.example.com
    DB_HOST: localhost
  run: |
    pytest tests/ -v --junitxml=test-results.xml
```

## 🐛 调试和故障排除

### Q: 测试失败时如何调试？
**A:** 使用多种调试方法：

```python
# 1. 增加详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 2. 使用pytest的调试选项
# pytest tests/ -v -s --tb=long

# 3. 在测试中添加调试信息
def test_api_call(self):
    response = self.client.get("/users")

    # 打印调试信息
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {response.headers}")
    print(f"Response Body: {response.text}")

    assert response.status_code == 200

# 4. 使用pdb调试器
import pdb; pdb.set_trace()
```

### Q: 如何处理间歇性失败的测试？
**A:** 使用重试机制和更好的等待策略：

```python
# 1. 使用pytest-rerunfailures插件
# pytest tests/ --reruns 3 --reruns-delay 1

# 2. 在代码中实现重试
import time
from functools import wraps

def retry(times=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == times - 1:
                        raise
                    time.sleep(delay)
            return wrapper
    return decorator

@retry(times=3, delay=2)
def test_flaky_api(self):
    response = self.client.get("/flaky-endpoint")
    assert response.status_code == 200
```

## 📚 学习资源

### Q: 如何深入学习JMESPath？
**A:** 推荐学习资源：
- [JMESPath官方教程](https://jmespath.org/tutorial.html)
- [JMESPath在线测试工具](https://jmespath.org/)
- [AWS CLI JMESPath指南](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html)

### Q: 如何学习更多pytest技巧？
**A:** 推荐资源：
- [pytest官方文档](https://docs.pytest.org/)
- [pytest插件列表](https://plugincompat.herokuapp.com/)
- [Python Testing 101](https://python-testing-101.readthedocs.io/)

## 🆘 获取更多帮助

如果您的问题在这里没有找到答案：

1. 📖 查看 [故障排除指南](./troubleshooting.md)
2. 🔍 搜索 [GitHub Issues](https://github.com/your-repo/pytest-framework/issues)
3. 💬 在 [讨论区](https://github.com/your-repo/pytest-framework/discussions) 提问
4. 📧 发送邮件到 [support@example.com](mailto:support@example.com)

---

**相关文档**: [用户指南](../user-guide/basic-usage.md) | [性能测试](../user-guide/performance.md)
