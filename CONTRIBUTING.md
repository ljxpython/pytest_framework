# 🤝 贡献指南

感谢您对 Pytest Framework 的关注！我们欢迎所有形式的贡献，无论是代码、文档、问题报告还是功能建议。

## 📋 贡献方式

### 🐛 报告Bug
- 在 [Issues](https://github.com/your-repo/pytest-framework/issues) 页面创建新的问题
- 使用 Bug 报告模板
- 提供详细的复现步骤和环境信息

### 💡 功能建议
- 在 [Issues](https://github.com/your-repo/pytest-framework/issues) 页面创建功能请求
- 使用功能请求模板
- 详细描述功能需求和使用场景

### 📝 改进文档
- 修复文档中的错误
- 添加缺失的文档
- 改进示例和教程

### 🔧 代码贡献
- 修复Bug
- 实现新功能
- 优化性能
- 重构代码

## 🚀 开发环境设置

### 1. Fork 和克隆项目

```bash
# Fork 项目到您的GitHub账户
# 然后克隆您的Fork

git clone https://github.com/YOUR_USERNAME/pytest-framework.git
cd pytest-framework

# 添加上游仓库
git remote add upstream https://github.com/your-repo/pytest-framework.git
```

### 2. 安装开发环境

```bash
# 安装Poetry（如果还没有安装）
curl -sSL https://install.python-poetry.org | python3 -

# 安装项目依赖
poetry install

# 激活虚拟环境
poetry shell

# 安装pre-commit钩子
pre-commit install
```

### 3. 验证环境

```bash
# 运行测试
pytest tests/ -v

# 运行代码质量检查
black --check .
isort --check-only .
flake8 .
mypy src/
```

## 📝 开发流程

### 1. 创建功能分支

```bash
# 确保主分支是最新的
git checkout main
git pull upstream main

# 创建新的功能分支
git checkout -b feature/your-feature-name
```

### 2. 开发和测试

```bash
# 进行开发...

# 运行测试
pytest tests/ -v

# 运行代码质量检查
black .
isort .
flake8 .

# 提交更改
git add .
git commit -m "feat: add your feature description"
```

### 3. 提交Pull Request

```bash
# 推送到您的Fork
git push origin feature/your-feature-name

# 在GitHub上创建Pull Request
```

## 📏 代码规范

### 1. Python代码风格

我们使用以下工具确保代码质量：

- **Black**: 代码格式化
- **isort**: 导入排序
- **flake8**: 代码检查
- **mypy**: 类型检查

```bash
# 格式化代码
black .
isort .

# 检查代码
flake8 .
mypy src/
```

### 2. 命名规范

```python
# 文件名：使用下划线分隔
test_user_authentication.py
data_driver.py

# 类名：使用驼峰命名
class UserAuthentication:
    pass

class DataDriver:
    pass

# 函数和变量名：使用下划线分隔
def create_user():
    pass

user_data = {}

# 常量：使用大写字母和下划线
MAX_RETRY_TIMES = 3
DEFAULT_TIMEOUT = 30
```

### 3. 文档字符串

```python
def create_user(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    创建新用户

    Args:
        user_data: 用户数据字典，包含name、email等字段

    Returns:
        创建成功的用户信息字典

    Raises:
        ValueError: 当用户数据无效时
        APIError: 当API调用失败时

    Example:
        >>> user_data = {"name": "张三", "email": "zhangsan@example.com"}
        >>> result = create_user(user_data)
        >>> print(result["id"])
        123
    """
    pass
```

### 4. 类型注解

```python
from typing import Dict, List, Optional, Union

def process_users(users: List[Dict[str, Any]],
                 filter_active: bool = True) -> List[Dict[str, Any]]:
    """处理用户列表"""
    pass

class APIClient:
    def __init__(self, base_url: str, timeout: Optional[int] = None) -> None:
        self.base_url = base_url
        self.timeout = timeout or 30
```

## 🧪 测试规范

### 1. 测试文件组织

```
tests/
├── unit/                   # 单元测试
├── integration/            # 集成测试
├── examples/              # 示例测试
└── conftest.py            # pytest配置
```

### 2. 测试命名

```python
class TestUserAuthentication:
    """用户认证测试类"""

    def test_login_with_valid_credentials_should_return_success(self):
        """使用有效凭据登录应该返回成功"""
        pass

    def test_login_with_invalid_password_should_return_401(self):
        """使用无效密码登录应该返回401错误"""
        pass
```

### 3. 测试结构

```python
def test_create_user_with_valid_data(self, api_client):
    """测试用例应该遵循AAA模式"""

    # Arrange - 准备测试数据
    user_data = {
        "name": "张三",
        "email": "zhangsan@example.com"
    }

    # Act - 执行操作
    response = api_client.post("/users", json=user_data)

    # Assert - 验证结果
    assert response.status_code == 201
    assert response.json()["data"]["name"] == "张三"
```

### 4. 测试覆盖率

- 新功能必须有对应的测试
- 测试覆盖率应该保持在80%以上
- 关键功能的测试覆盖率应该达到95%以上

```bash
# 运行覆盖率测试
pytest --cov=src --cov-report=html --cov-fail-under=80
```

## 📚 文档规范

### 1. 文档结构

```markdown
# 标题

简短的功能描述

## 目标

说明文档的学习目标

## 内容

详细的功能说明和示例

## 示例

具体的代码示例

## 最佳实践

使用建议和注意事项
```

### 2. 代码示例

```python
# 好的示例：完整且可运行
from src.client.base_client import BaseClient

client = BaseClient("https://api.example.com")
response = client.get("/users")
assert response.status_code == 200

# 避免：不完整的示例
client.get("/users")  # 缺少导入和初始化
```

## 🔄 提交规范

### 1. 提交消息格式

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### 2. 提交类型

- `feat`: 新功能
- `fix`: Bug修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

### 3. 示例

```bash
feat(client): add retry mechanism for HTTP requests

Add automatic retry functionality with exponential backoff
for handling transient network failures.

Closes #123
```

## 🎯 Pull Request 规范

### 1. PR标题

- 使用清晰描述性的标题
- 遵循提交消息格式
- 包含相关的Issue编号

### 2. PR描述

```markdown
## 变更说明
简要描述这个PR的变更内容

## 变更类型
- [ ] Bug修复
- [ ] 新功能
- [ ] 文档更新
- [ ] 代码重构
- [ ] 性能优化

## 测试
- [ ] 添加了新的测试
- [ ] 所有测试通过
- [ ] 手动测试通过

## 检查清单
- [ ] 代码遵循项目规范
- [ ] 添加了必要的文档
- [ ] 更新了CHANGELOG
```

### 3. 代码审查

- 所有PR都需要至少一个维护者的审查
- 确保CI/CD检查通过
- 解决所有审查意见

## 🏷️ 发布流程

### 1. 版本号规范

我们使用 [语义化版本](https://semver.org/lang/zh-CN/)：

- `MAJOR.MINOR.PATCH`
- `1.0.0` -> `1.0.1` (补丁版本)
- `1.0.0` -> `1.1.0` (次版本)
- `1.0.0` -> `2.0.0` (主版本)

### 2. 发布步骤

```bash
# 1. 更新版本号
poetry version patch  # 或 minor, major

# 2. 更新CHANGELOG
# 编辑 CHANGELOG.md

# 3. 提交版本更新
git add .
git commit -m "chore: bump version to x.x.x"

# 4. 创建标签
git tag vx.x.x

# 5. 推送
git push origin main --tags
```

## 🆘 获取帮助

如果您在贡献过程中遇到任何问题：

- 📖 查看 [文档](./docs/)
- 💬 在 [Discussions](https://github.com/your-repo/pytest-framework/discussions) 中提问
- 📧 发送邮件到 [maintainers@example.com](mailto:maintainers@example.com)
- 🐛 在 [Issues](https://github.com/your-repo/pytest-framework/issues) 中报告问题

## 🙏 致谢

感谢所有为这个项目做出贡献的开发者！

您的贡献将被记录在 [CONTRIBUTORS.md](./CONTRIBUTORS.md) 文件中。

---

**再次感谢您的贡献！** 🎉
