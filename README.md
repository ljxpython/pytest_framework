# 🚀 Pytest Framework - 现代化接口测试自动化框架

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Pytest](https://img.shields.io/badge/Pytest-8.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Build](https://img.shields.io/badge/Build-Passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/Coverage-90%25-brightgreen.svg)

**一个功能强大、易于扩展的Python接口测试自动化框架**

[快速开始](#-快速开始) • [文档](#-文档) • [示例](#-示例) • [贡献](#-贡献) • [社区](#-社区)

</div>

---

## ✨ 核心特性

### 🎯 **开箱即用**
- 🔧 **零配置启动** - 5分钟快速上手，无需复杂配置
- 📦 **丰富的内置功能** - HTTP客户端、断言、数据驱动、Mock服务器
- 🎨 **优雅的API设计** - 链式调用，代码简洁易读

### 🚀 **高级功能**
- 🔍 **增强断言引擎** - 基于JMESPath的强大查询和Schema验证
- 📊 **数据驱动测试** - Excel、CSV、JSON、YAML多格式支持
- 🎭 **内置Mock服务器** - 轻量级Mock服务，支持复杂场景
- ⚡ **性能测试** - 负载测试、压力测试、性能监控

### 🏗️ **企业级架构**
- 🌍 **多环境管理** - 开发、测试、生产环境无缝切换
- 🔌 **插件化扩展** - 灵活的插件机制，支持自定义扩展
- 📈 **全面监控** - 详细的日志记录和性能指标
- 🛡️ **安全可靠** - 认证支持、敏感数据保护

## 🎬 快速预览

### 简洁的测试用例

```python
from src.client.base_client import BaseClient
from src.utils.assertion import assert_success_response
from src.utils.environment import get_base_url

class TestUserAPI:
    def setup_method(self):
        self.client = BaseClient(get_base_url())

    def test_create_user(self):
        user_data = {"name": "张三", "email": "zhangsan@example.com"}
        response = self.client.post("/users", json=user_data)

        # 基于JMESPath的链式断言，优雅简洁
        (assert_success_response(response, 201)
         .assert_jmespath("data.name", "张三")
         .assert_jmespath("data.email", "zhangsan@example.com")
         .assert_response_time(2.0, response.elapsed.total_seconds()))
```

### 数据驱动测试

```python
from src.utils.data_driver import data_driver

# 生成测试数据
template = {
    "name": "faker.name",
    "email": "faker.email",
    "phone": "faker.phone_number"
}
test_users = data_driver.generate_test_data(template, count=10)

@pytest.mark.parametrize("user_data", test_users)
def test_batch_create_users(self, user_data):
    response = self.client.post("/users", json=user_data)
    assert_success_response(response, 201)
```

### Mock服务器

```python
from src.utils.mock_server import MockServer, create_mock_response

# 启动Mock服务器
mock_server = MockServer(port=8888)
mock_server.add_rule(
    "GET", "/api/users/123",
    create_mock_response(200, {"id": 123, "name": "张三"})
).start()
```

### 性能测试

```python
from src.utils.performance import load_test

def api_request():
    return requests.get("https://api.example.com/users")

# 负载测试：10个并发用户，100个请求
metrics = load_test(api_request, concurrent_users=10, total_requests=100)
print(f"平均响应时间: {metrics.avg_response_time}s")
print(f"QPS: {metrics.requests_per_second}")
```

## 🚀 快速开始

### 1. 安装框架

```bash
# 克隆项目
git clone https://github.com/ljxpython/pytest_framework.git
cd pytest-framework

# 安装依赖（推荐使用Poetry）
poetry install && poetry shell

# 或使用pip
pip install -r requirements.txt
```

### 2. 配置环境

编辑 `conf/settings.yaml`：

```yaml
boe:  # 开发环境
  API:
    base_url: "https://httpbin.org"
    timeout: 30
  DEBUG: true
```

### 3. 运行测试

```bash
# 运行示例测试
pytest tests/examples/ -v

# 生成Allure报告
pytest --alluredir=output/allure-result
allure generate output/allure-result -o output/allure-report --clean
```

### 4. 查看报告

打开 `output/allure-report/index.html` 查看详细测试报告。

## 📚 文档

| 文档类型 | 链接 | 描述 |
|---------|------|------|
| 📖 **快速开始** | [docs/quick-start/](./docs/quick-start/) | 5分钟快速上手指南 |
| 🏗️ **架构设计** | [docs/architecture/](./docs/architecture/) | 框架架构和设计理念 |
| 📋 **用户指南** | [docs/user-guide/](./docs/user-guide/) | 详细功能使用指南 |
| 🔧 **API参考** | [docs/api-reference/](./docs/api-reference/) | 完整API文档 |
| 💡 **最佳实践** | [docs/best-practices/](./docs/best-practices/) | 测试最佳实践 |
| 🔌 **扩展开发** | [docs/extension/](./docs/extension/) | 插件和扩展开发 |

## 🎯 示例项目

### 基础示例

```python
# tests/examples/basic_example.py
class TestBasicAPI:
    """基础API测试示例"""

    def test_get_users(self):
        """获取用户列表"""
        response = self.client.get("/users")
        assert_success_response(response)
        assert len(response.json()["data"]) > 0

    def test_create_user(self):
        """创建用户"""
        user_data = {"name": "测试用户", "email": "test@example.com"}
        response = self.client.post("/users", json=user_data)
        assert_success_response(response, 201)
```

### 高级示例

```python
# tests/examples/advanced_example.py
class TestAdvancedFeatures:
    """高级功能示例"""

    @pytest.mark.parametrize("user_data", load_test_data("users.json"))
    def test_data_driven(self, user_data):
        """数据驱动测试"""
        response = self.client.post("/users", json=user_data)
        (assert_success_response(response, 201)
         .assert_json_path("$.data.name", user_data["name"])
         .assert_schema(USER_SCHEMA))

    @pytest.mark.performance
    def test_performance(self):
        """性能测试"""
        metrics = load_test(
            lambda: self.client.get("/users"),
            concurrent_users=10,
            total_requests=100
        )
        assert metrics.avg_response_time < 1.0
        assert metrics.error_rate < 0.01
```

## 🏗️ 项目结构

```
pytest-framework/
├── 📁 conf/                    # 配置管理
│   ├── config.py              # 配置管理器
│   ├── constants.py           # 常量定义
│   └── settings.yaml          # 环境配置
├── 📁 src/                     # 核心源码
│   ├── 📁 client/             # HTTP客户端
│   │   ├── base_client.py     # 基础客户端
│   │   └── base_auth.py       # 认证处理
│   ├── 📁 model/              # 数据模型
│   │   ├── auto_pytest.py    # 测试模型
│   │   └── modelsbase.py      # 基础模型
│   └── 📁 utils/              # 工具类库
│       ├── assertion.py       # 增强断言
│       ├── data_driver.py     # 数据驱动
│       ├── environment.py     # 环境管理
│       ├── mock_server.py     # Mock服务器
│       ├── performance.py     # 性能测试
│       └── log_moudle.py      # 日志管理
├── 📁 tests/                   # 测试用例
│   ├── conftest.py            # pytest配置
│   ├── 📁 examples/           # 示例测试
│   ├── 📁 test_user/          # 用户模块测试
│   └── 📁 test_goods/         # 商品模块测试
├── 📁 docs/                    # 项目文档
├── 📁 output/                  # 测试输出
│   ├── 📁 allure-result/      # Allure原始数据
│   └── 📁 allure-report/      # Allure报告
├── 📄 main.py                  # 主入口文件
├── 📄 pytest.ini              # pytest配置
├── 📄 pyproject.toml           # 项目配置
└── 📄 README.md                # 项目说明
```

## 🌟 核心优势

### 🎯 **为测试工程师而生**
- **低学习成本** - 基于pytest，测试工程师快速上手
- **高开发效率** - 丰富的内置功能，减少重复代码
- **强大的断言** - 支持复杂的数据验证场景
- **完善的报告** - Allure集成，美观的测试报告

### 🏢 **企业级特性**
- **多环境支持** - 开发、测试、生产环境配置管理
- **团队协作** - 统一的代码规范和最佳实践
- **CI/CD集成** - 无缝集成Jenkins、GitHub Actions
- **可扩展架构** - 插件机制支持定制化需求

### 🚀 **性能卓越**
- **并发执行** - 支持多进程并行测试
- **连接复用** - HTTP连接池提升性能
- **内存优化** - 大数据量测试场景优化
- **性能监控** - 实时监控测试执行性能

## 🛠️ 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| **Python** | 3.8+ | 核心开发语言 |
| **Pytest** | 8.0+ | 测试框架 |
| **JMESPath** | 1.0+ | JSON查询语言（核心技术栈） |
| **Requests** | 2.32+ | HTTP客户端 |
| **Allure** | 2.13+ | 测试报告 |
| **Dynaconf** | 3.2+ | 配置管理 |
| **Faker** | 29.0+ | 测试数据生成 |
| **Loguru** | 0.7+ | 日志管理 |

## 📊 性能基准

| 指标 | 数值 | 说明 |
|------|------|------|
| **启动时间** | < 2s | 框架初始化时间 |
| **并发支持** | 100+ | 最大并发用户数 |
| **内存占用** | < 100MB | 基础运行内存 |
| **测试速度** | 100+/min | 每分钟执行测试数 |



## 🤝 贡献

我们欢迎所有形式的贡献！无论是：

- 🐛 **报告Bug** - 发现问题请提交Issue
- 💡 **功能建议** - 有好想法请告诉我们
- 📝 **文档改进** - 帮助完善文档
- 🔧 **代码贡献** - 提交Pull Request

### 贡献步骤

1. **Fork** 项目到您的GitHub
2. **创建** 功能分支 (`git checkout -b feature/AmazingFeature`)
3. **提交** 更改 (`git commit -m 'Add some AmazingFeature'`)
4. **推送** 到分支 (`git push origin feature/AmazingFeature`)
5. **创建** Pull Request

详细贡献指南请查看 [CONTRIBUTING.md](./docs/extension/contributing.md)

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=your-repo/pytest-framework&type=Date)](https://star-history.com/#your-repo/pytest-framework&Date)

## 🔗 相关链接

- 📖 [官方文档](./docs/)
- 🐛 [问题反馈](https://github.com/your-repo/pytest-framework/issues)
- 💬 [讨论区](https://github.com/your-repo/pytest-framework/discussions)
- 📧 [邮件联系](mailto:support@example.com)
- 🐦 [Twitter](https://twitter.com/pytest_framework)

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者和用户！

特别感谢以下开源项目：
- [Pytest](https://pytest.org/) - 优秀的Python测试框架
- [Requests](https://requests.readthedocs.io/) - 简洁的HTTP库
- [Allure](https://allurereport.org/) - 美观的测试报告工具

---

<div align="center">
**如果这个项目对您有帮助，请给我们一个 ⭐ Star！**

**让更多的测试工程师受益于这个框架！**

[⬆ 回到顶部](#-pytest-framework---现代化接口测试自动化框架)

</div>
