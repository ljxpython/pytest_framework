# 📦 安装指南

本指南将详细介绍如何在不同环境下安装和配置 Pytest Framework。

## 📋 系统要求

### 最低要求
- **Python**: 3.8 或更高版本
- **操作系统**: Windows 10+、macOS 10.14+、Linux (Ubuntu 18.04+)
- **内存**: 2GB RAM
- **磁盘空间**: 500MB 可用空间

### 推荐配置
- **Python**: 3.11 或 3.12
- **内存**: 4GB RAM 或更多
- **磁盘空间**: 1GB 可用空间

## 🐍 Python环境准备

### 1. 检查Python版本

```bash
python --version
# 或
python3 --version
```

如果版本低于3.8，请升级Python。

### 2. 安装Python（如需要）

#### Windows
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载最新版本的Python安装包
3. 运行安装程序，**确保勾选"Add Python to PATH"**

#### macOS
```bash
# 使用Homebrew安装
brew install python

# 或使用pyenv管理多版本
brew install pyenv
pyenv install 3.12.0
pyenv global 3.12.0
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

## 🚀 安装方式

### 方式一：从源码安装（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/your-repo/pytest-framework.git
cd pytest-framework

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

# 4. 升级pip
pip install --upgrade pip

# 5. 安装依赖
pip install -r requirements.txt
```

### 方式二：使用Poetry（推荐开发者）

```bash
# 1. 安装Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. 克隆项目
git clone https://github.com/your-repo/pytest-framework.git
cd pytest-framework

# 3. 安装依赖
poetry install

# 4. 激活虚拟环境
poetry shell
```

### 方式三：使用pip安装（未来支持）

```bash
# 从PyPI安装（计划中）
pip install pytest-framework
```

## 🔧 依赖说明

### 核心依赖
```
pytest>=8.3.3          # 测试框架
requests>=2.32.3        # HTTP客户端
jmespath>=1.0.1         # JSON查询语言
assertpy>=1.1           # 增强断言
dynaconf>=3.2.6         # 配置管理
loguru>=0.7.2           # 日志管理
```

### 数据处理依赖
```
pandas>=2.2.3           # 数据处理
faker>=29.0.0           # 测试数据生成
pyyaml>=6.0.2           # YAML支持
jsonpath-ng>=1.6.1      # JSONPath支持
```

### 测试增强依赖
```
allure-pytest>=2.13.5   # 测试报告
pytest-xdist>=3.6.1     # 并行测试
pytest-rerunfailures>=14.0  # 失败重试
pytest-ordering>=0.6    # 测试排序
```

### 可选依赖
```
peewee>=3.17.6          # 数据库ORM
pymysql>=1.1.1          # MySQL驱动
adb-shell>=0.4.4        # Android调试
```

## ✅ 验证安装

### 1. 基础验证

```bash
# 检查pytest版本
pytest --version

# 检查Python包
python -c "import pytest, requests, jmespath; print('所有核心包安装成功')"
```

### 2. 运行测试验证

```bash
# 运行示例测试
pytest tests/examples/test_enhanced_features.py::TestEnhancedAssertion::test_jmespath_assertion -v

# 预期输出应包含：
# ✓ JMESPath断言通过: code = 200
# ✓ JMESPath断言通过: data.users[0].name = 张三
# PASSED
```

### 3. 功能验证

```bash
# 验证配置加载
python -c "from src.utils.environment import get_config; print('配置系统正常')"

# 验证断言功能
python -c "from src.utils.assertion import assert_response; print('断言系统正常')"

# 验证JMESPath功能
python -c "from src.utils.jmespath_helper import jmes; print('JMESPath系统正常')"
```

## 🛠️ 开发环境配置

### 1. 安装开发工具

```bash
# 代码格式化工具
pip install black isort

# 代码检查工具
pip install flake8 mypy

# 预提交钩子
pip install pre-commit
pre-commit install
```

### 2. IDE配置

#### VS Code
创建 `.vscode/settings.json`：
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.formatting.provider": "black",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests/"]
}
```

#### PyCharm
1. 设置Python解释器为虚拟环境中的Python
2. 配置代码格式化工具为Black
3. 启用pytest作为测试运行器

### 3. 环境变量配置

创建 `.env` 文件（可选）：
```bash
# 环境设置
ENV=boe
DEBUG=true

# 数据库配置（如需要）
DB_HOST=localhost
DB_PORT=3306
DB_USER=test_user
DB_PASSWORD=test_password

# API配置
API_BASE_URL=https://api.example.com
API_TIMEOUT=30
```

## 🐳 Docker安装（可选）

### 1. 创建Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装Python依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目文件
COPY . .

# 设置环境变量
ENV PYTHONPATH=/app

# 运行测试
CMD ["pytest", "tests/", "-v"]
```

### 2. 构建和运行

```bash
# 构建镜像
docker build -t pytest-framework .

# 运行测试
docker run --rm pytest-framework

# 交互式运行
docker run -it --rm -v $(pwd):/app pytest-framework bash
```

## 🔧 常见问题解决

### 1. Python版本问题

**问题**: `python: command not found`
**解决**:
```bash
# 尝试使用python3
python3 --version

# 或创建别名
alias python=python3
```

### 2. 权限问题

**问题**: `Permission denied`
**解决**:
```bash
# 使用用户安装
pip install --user -r requirements.txt

# 或修改权限
sudo chown -R $USER:$USER /path/to/project
```

### 3. 依赖冲突

**问题**: 包版本冲突
**解决**:
```bash
# 创建新的虚拟环境
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

### 4. 网络问题

**问题**: 下载速度慢或失败
**解决**:
```bash
# 使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/

# 或配置pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
```

### 5. 导入错误

**问题**: `ModuleNotFoundError`
**解决**:
```bash
# 检查PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

# 或在项目根目录运行
python -m pytest tests/
```

## 📊 性能优化

### 1. 并行测试配置

```bash
# 安装并行测试插件
pip install pytest-xdist

# 运行并行测试
pytest -n auto  # 自动检测CPU核心数
pytest -n 4     # 使用4个进程
```

### 2. 缓存配置

```bash
# 启用pytest缓存
pytest --cache-clear  # 清除缓存
pytest --lf          # 只运行上次失败的测试
pytest --ff          # 先运行上次失败的测试
```

## 🎯 下一步

安装完成后，您可以：

1. 📖 阅读 [第一个测试](./first-test.md) 编写您的第一个测试用例
2. 📋 查看 [基础用法](../user-guide/basic-usage.md) 了解框架基本功能
3. 🏗️ 学习 [架构设计](../architecture/overview.md) 理解框架原理
4. 💡 参考 [最佳实践](../best-practices/test-organization.md) 编写高质量测试

## 🆘 获取帮助

如果安装过程中遇到问题：

- 📖 查看 [常见问题](../faq/troubleshooting.md)
- 🐛 提交 [Issue](https://github.com/your-repo/pytest-framework/issues)
- 💬 参与 [讨论](https://github.com/your-repo/pytest-framework/discussions)
- 📧 发送邮件到 [support@example.com](mailto:support@example.com)

---

**下一步**: [第一个测试](./first-test.md) | [基础用法](../user-guide/basic-usage.md)
