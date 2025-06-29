# ⚙️ 配置管理 - 一套配置，走遍天下

> "配置做得好，环境切换没烦恼！"

还在为不同环境的配置切换而头疼？还在担心把测试数据发到生产环境？别慌！我们的配置管理系统就像一个贴心的管家，帮你打理好一切。

## 🎯 为什么配置管理这么重要？

### 真实痛点
你是不是遇到过这些尴尬时刻：
- 😱 "卧槽！我把测试数据发到生产环境了！"
- 🤦‍♂️ "这个API地址又变了，要改100个地方..."
- 😤 "开发环境能跑，测试环境就挂了"
- 🙄 "每次换环境都要改代码，烦死了"

有了我们的配置管理，这些问题统统拜拜！

## 📁 配置文件结构 - 井井有条

```
conf/
├── settings.yaml          # 主配置文件 - 老大
├── settings.local.yaml    # 本地配置 - 小弟（不提交到git）
├── .secrets.yaml          # 敏感信息 - 机密（绝对不提交）
├── config.py              # 配置管理器 - 管家
└── constants.py           # 常量定义 - 规矩
```

## 🎨 配置文件编写 - 简单到飞起

### 主配置文件 `settings.yaml`

```yaml
# 这就是传说中的"一套配置走天下"
default:
  # 默认配置 - 所有环境的基础
  APP_NAME: "Pytest Framework"
  VERSION: "1.0.0"
  DEBUG: false
  LOG_LEVEL: "INFO"

  # 数据库配置模板
  DB:
    driver: "mysql"
    charset: "utf8mb4"
    pool_size: 10
    timeout: 30

# 开发环境 - 程序员的乐园
boe:
  DEBUG: true
  LOG_LEVEL: "DEBUG"

  API:
    base_url: "https://dev-api.example.com"
    timeout: 30
    retry_times: 3

  DB:
    host: "dev-db.example.com"
    port: 3306
    database: "test_db"
    user: "dev_user"
    # 密码放在.secrets.yaml里，安全第一！

  REDIS:
    host: "dev-redis.example.com"
    port: 6379
    db: 0

  # 第三方服务
  WECHAT:
    app_id: "dev_app_id"
    # app_secret 在.secrets.yaml里

  # 测试专用配置
  TEST:
    mock_enabled: true
    performance_test: false
    slow_test_threshold: 5.0

# 测试环境 - 接近真实的演练场
test:
  DEBUG: false
  LOG_LEVEL: "INFO"

  API:
    base_url: "https://test-api.example.com"
    timeout: 60
    retry_times: 2

  DB:
    host: "test-db.example.com"
    port: 3306
    database: "test_db"
    user: "test_user"

  REDIS:
    host: "test-redis.example.com"
    port: 6379
    db: 1

  TEST:
    mock_enabled: false
    performance_test: true
    slow_test_threshold: 3.0

# 生产环境 - 神圣不可侵犯
prod:
  DEBUG: false
  LOG_LEVEL: "WARNING"

  API:
    base_url: "https://api.example.com"
    timeout: 30
    retry_times: 1

  DB:
    host: "prod-db.example.com"
    port: 3306
    database: "prod_db"
    user: "prod_user"

  REDIS:
    host: "prod-redis.example.com"
    port: 6379
    db: 0

  TEST:
    mock_enabled: false
    performance_test: false
    slow_test_threshold: 1.0
```

### 敏感信息配置 `.secrets.yaml`

```yaml
# 这个文件绝对不要提交到git！
# 加到 .gitignore 里：*.secrets.yaml

boe:
  DB:
    password: "dev_super_secret_password"
  WECHAT:
    app_secret: "dev_wechat_secret"
  API:
    secret_key: "dev_api_secret_key"

test:
  DB:
    password: "test_super_secret_password"
  WECHAT:
    app_secret: "test_wechat_secret"
  API:
    secret_key: "test_api_secret_key"

prod:
  DB:
    password: "prod_ultra_secret_password"
  WECHAT:
    app_secret: "prod_wechat_secret"
  API:
    secret_key: "prod_api_secret_key"
```

### 本地个人配置 `settings.local.yaml`

```yaml
# 这是你的个人配置，也不要提交
# 用来覆盖一些个人偏好

boe:
  DEBUG: true
  LOG_LEVEL: "DEBUG"

  # 个人开发时用的本地数据库
  DB:
    host: "localhost"
    port: 3306
    user: "root"

  # 个人偏好的API地址
  API:
    base_url: "http://localhost:8080"

  # 个人测试配置
  TEST:
    mock_enabled: true
    auto_cleanup: false  # 测试后不自动清理数据，方便调试
```

## 🚀 使用配置 - 简单到不敢相信

### 基础使用

```python
from src.utils.environment import get_config, get_base_url, switch_environment

# 获取配置 - 就这么简单
api_url = get_base_url()  # 获取当前环境的API地址
timeout = get_config("API.timeout", 30)  # 获取超时配置，默认30秒
debug_mode = get_config("DEBUG", False)  # 获取调试模式

# 获取复杂配置
db_config = get_config("DB")
redis_config = get_config("REDIS")

print(f"连接数据库: {db_config['host']}:{db_config['port']}")
print(f"Redis地址: {redis_config['host']}")
```

### 环境切换 - 一键搞定

```python
# 方法1: 代码中切换
switch_environment("test")  # 切换到测试环境
api_url = get_base_url()    # 现在获取的是测试环境的URL

# 方法2: 环境变量切换
# export ENV=test
# python -m pytest tests/

# 方法3: 命令行参数
# pytest tests/ --env=test
```

### 高级用法 - 配置也能玩出花

```python
class ConfigHelper:
    """配置助手 - 让配置使用更优雅"""

    @staticmethod
    def get_database_url():
        """获取数据库连接URL"""
        db = get_config("DB")
        password = get_config("DB.password", "")

        return f"mysql://{db['user']}:{password}@{db['host']}:{db['port']}/{db['database']}"

    @staticmethod
    def get_redis_client():
        """获取Redis客户端"""
        import redis
        config = get_config("REDIS")

        return redis.Redis(
            host=config["host"],
            port=config["port"],
            db=config["db"]
        )

    @staticmethod
    def is_mock_enabled():
        """检查是否启用Mock"""
        return get_config("TEST.mock_enabled", False)

    @staticmethod
    def get_performance_threshold():
        """获取性能测试阈值"""
        return get_config("TEST.slow_test_threshold", 5.0)

# 在测试中使用
class TestUserAPI:
    def setup_method(self):
        # 根据配置决定使用真实API还是Mock
        if ConfigHelper.is_mock_enabled():
            self.client = MockClient()
        else:
            self.client = BaseClient(get_base_url())

    def test_user_creation(self):
        response = self.client.post("/users", json={"name": "测试用户"})
        assert response.status_code == 201

        # 根据配置决定是否进行性能检查
        if get_config("TEST.performance_test", False):
            assert response.elapsed.total_seconds() < ConfigHelper.get_performance_threshold()
```

## 🎭 环境特定配置 - 因地制宜

### 开发环境配置技巧

```python
# 开发环境专用配置
if get_config("DEBUG"):
    # 开发环境下的特殊处理
    import logging
    logging.basicConfig(level=logging.DEBUG)

    # 启用详细日志
    from src.utils.log_moudle import logger
    logger.add("debug.log", level="DEBUG", rotation="1 day")

    # 开发环境下不验证SSL证书
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
```

### 测试环境配置技巧

```python
# 测试环境专用配置
if get_config("ENV") == "test":
    # 测试环境下自动清理数据
    @pytest.fixture(autouse=True)
    def auto_cleanup():
        yield
        if get_config("TEST.auto_cleanup", True):
            cleanup_test_data()

    # 测试环境下启用性能监控
    if get_config("TEST.performance_test"):
        pytest_plugins = ["plugins.performance_monitor"]
```

### 生产环境配置技巧

```python
# 生产环境安全检查
if get_config("ENV") == "prod":
    # 生产环境下禁止某些危险操作
    def dangerous_operation():
        raise RuntimeError("生产环境禁止执行此操作！")

    # 生产环境下启用审计日志
    from src.utils.audit import AuditLogger
    audit_logger = AuditLogger()
    audit_logger.start()
```

## 🔐 安全配置管理 - 安全第一

### 敏感信息处理

```python
import os
from src.utils.environment import get_config

class SecureConfig:
    """安全配置管理器"""

    @staticmethod
    def get_secret(key, default=None):
        """安全地获取敏感信息"""
        # 优先级：环境变量 > 配置文件 > 默认值
        env_key = key.replace(".", "_").upper()

        # 1. 先从环境变量获取
        value = os.getenv(env_key)
        if value:
            return value

        # 2. 再从配置文件获取
        value = get_config(key)
        if value:
            return value

        # 3. 最后使用默认值
        return default

    @staticmethod
    def get_database_password():
        """获取数据库密码"""
        return SecureConfig.get_secret("DB.password")

    @staticmethod
    def get_api_secret():
        """获取API密钥"""
        return SecureConfig.get_secret("API.secret_key")

# 使用示例
db_password = SecureConfig.get_database_password()
api_secret = SecureConfig.get_api_secret()
```

### 配置验证

```python
class ConfigValidator:
    """配置验证器 - 防止配置错误"""

    @staticmethod
    def validate_required_configs():
        """验证必需的配置项"""
        required_configs = [
            "API.base_url",
            "DB.host",
            "DB.port",
            "DB.database"
        ]

        missing_configs = []
        for config_key in required_configs:
            if not get_config(config_key):
                missing_configs.append(config_key)

        if missing_configs:
            raise ValueError(f"缺少必需的配置项: {missing_configs}")

    @staticmethod
    def validate_config_format():
        """验证配置格式"""
        # 验证URL格式
        api_url = get_config("API.base_url")
        if api_url and not api_url.startswith(("http://", "https://")):
            raise ValueError(f"API URL格式错误: {api_url}")

        # 验证端口号
        db_port = get_config("DB.port")
        if db_port and not (1 <= db_port <= 65535):
            raise ValueError(f"数据库端口号错误: {db_port}")

        # 验证超时时间
        timeout = get_config("API.timeout")
        if timeout and timeout <= 0:
            raise ValueError(f"超时时间必须大于0: {timeout}")

# 在应用启动时验证配置
def startup_validation():
    """启动时配置验证"""
    try:
        ConfigValidator.validate_required_configs()
        ConfigValidator.validate_config_format()
        print("✅ 配置验证通过")
    except ValueError as e:
        print(f"❌ 配置验证失败: {e}")
        exit(1)
```

## 🎪 动态配置 - 配置也能热更新

```python
import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigWatcher(FileSystemEventHandler):
    """配置文件监控器 - 配置变了我就知道"""

    def __init__(self, config_manager):
        self.config_manager = config_manager
        self.last_reload = 0

    def on_modified(self, event):
        """配置文件被修改时的处理"""
        if event.src_path.endswith('.yaml'):
            # 防止重复触发
            current_time = time.time()
            if current_time - self.last_reload > 1:
                print(f"🔄 检测到配置文件变化: {event.src_path}")
                self.config_manager.reload()
                self.last_reload = current_time

class DynamicConfigManager:
    """动态配置管理器"""

    def __init__(self):
        self.observer = Observer()
        self.watcher = ConfigWatcher(self)

    def start_watching(self, config_dir="conf"):
        """开始监控配置文件"""
        self.observer.schedule(self.watcher, config_dir, recursive=True)
        self.observer.start()
        print(f"🔍 开始监控配置目录: {config_dir}")

    def stop_watching(self):
        """停止监控"""
        self.observer.stop()
        self.observer.join()
        print("⏹️ 停止配置监控")

    def reload(self):
        """重新加载配置"""
        # 这里重新加载配置逻辑
        print("🔄 配置已重新加载")

# 使用动态配置
dynamic_config = DynamicConfigManager()
dynamic_config.start_watching()

# 在程序结束时停止监控
import atexit
atexit.register(dynamic_config.stop_watching)
```

## 💡 配置最佳实践

### 1. 配置分层原则
```
环境变量 > 本地配置 > 主配置 > 默认值
```

### 2. 敏感信息处理
```python
# ✅ 正确做法
password = os.getenv("DB_PASSWORD") or get_config("DB.password")

# ❌ 错误做法 - 直接写在代码里
password = "my_secret_password"  # 千万别这样！
```

### 3. 配置命名规范
```yaml
# ✅ 好的命名 - 清晰明了
API:
  base_url: "https://api.example.com"
  timeout: 30
  retry_times: 3

# ❌ 不好的命名 - 容易混淆
api_url: "https://api.example.com"
t: 30
retry: 3
```

### 4. 环境隔离
```python
# ✅ 环境隔离 - 安全可靠
if get_config("ENV") == "prod":
    # 生产环境特殊处理
    pass

# ❌ 混合环境 - 危险操作
# 不要在一个配置文件里混合不同环境的敏感信息
```

## 🎯 总结

配置管理就像是测试框架的"大脑"：
- 🎨 **结构清晰** - 配置文件井井有条
- 🔐 **安全可靠** - 敏感信息妥善保护
- 🚀 **使用简单** - 一行代码获取配置
- 🎭 **环境隔离** - 不同环境互不干扰
- 🔄 **动态更新** - 配置变化实时感知

记住：**好的配置管理让你专注于测试逻辑，而不是环境问题！**

现在，去配置你的测试环境吧，让测试在任何地方都能完美运行！

---

**小贴士**: 别忘了把 `.secrets.yaml` 和 `settings.local.yaml` 加到 `.gitignore` 里哦！
