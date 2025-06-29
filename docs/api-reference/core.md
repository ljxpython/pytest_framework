# 🔧 核心API参考

本文档提供 Pytest Framework 核心API的详细参考信息。

## 🌐 HTTP客户端API

### BaseClient

基础HTTP客户端类，提供所有HTTP操作的核心功能。

```python
class BaseClient:
    def __init__(self, host: str, timeout: int = 10, **kwargs)
```

#### 参数
- `host` (str): 服务器主机地址，如 "https://api.example.com"
- `timeout` (int): 请求超时时间，默认10秒
- `**kwargs`: 其他可选参数

#### 方法

##### get()
```python
def get(self, url: str, params: Dict = None, **kwargs) -> Response
```
发送GET请求。

**参数:**
- `url` (str): 请求路径
- `params` (Dict, optional): 查询参数
- `**kwargs`: 传递给requests的其他参数

**返回:** `requests.Response` 对象

**示例:**
```python
client = BaseClient("https://api.example.com")
response = client.get("/users", params={"page": 1, "size": 10})
```

##### post()
```python
def post(self, url: str, data: Any = None, json: Dict = None, **kwargs) -> Response
```
发送POST请求。

**参数:**
- `url` (str): 请求路径
- `data` (Any, optional): 请求体数据
- `json` (Dict, optional): JSON格式的请求体
- `**kwargs`: 传递给requests的其他参数

**示例:**
```python
# 发送JSON数据
response = client.post("/users", json={"name": "张三", "email": "zhangsan@example.com"})

# 发送表单数据
response = client.post("/upload", data={"file": "content"})
```

##### put()
```python
def put(self, url: str, data: Any = None, json: Dict = None, **kwargs) -> Response
```
发送PUT请求。

##### delete()
```python
def delete(self, url: str, **kwargs) -> Response
```
发送DELETE请求。

##### request()
```python
def request(self, method: str, url: str, **kwargs) -> Response
```
发送自定义HTTP方法的请求。

**示例:**
```python
response = client.request("PATCH", "/users/123", json={"name": "新名称"})
```

## 🔍 断言API

### EnhancedAssertion

增强的断言类，提供丰富的断言方法。

```python
class EnhancedAssertion:
    def __init__(self, response_data: Any = None)
```

#### JMESPath断言方法

##### assert_jmespath()
```python
def assert_jmespath(self, jmes_path: str, expected_value: Any) -> 'EnhancedAssertion'
```
使用JMESPath查询并断言值。

**参数:**
- `jmes_path` (str): JMESPath查询表达式
- `expected_value` (Any): 期望的值

**示例:**
```python
(assert_response(response_data)
 .assert_jmespath("code", 200)
 .assert_jmespath("data.user.name", "张三"))
```

##### assert_jmespath_exists()
```python
def assert_jmespath_exists(self, jmes_path: str) -> 'EnhancedAssertion'
```
断言JMESPath路径存在。

##### assert_jmespath_length()
```python
def assert_jmespath_length(self, jmes_path: str, expected_length: int) -> 'EnhancedAssertion'
```
断言JMESPath查询结果的长度。

##### assert_jmespath_type()
```python
def assert_jmespath_type(self, jmes_path: str, expected_type: type) -> 'EnhancedAssertion'
```
断言JMESPath查询结果的类型。

#### 基础断言方法

##### assert_status_code()
```python
def assert_status_code(self, expected_code: int, actual_code: int) -> 'EnhancedAssertion'
```
断言HTTP状态码。

##### assert_response_time()
```python
def assert_response_time(self, max_time: float, actual_time: float) -> 'EnhancedAssertion'
```
断言响应时间。

##### assert_contains()
```python
def assert_contains(self, expected_value: Any, container: Any = None) -> 'EnhancedAssertion'
```
断言包含关系。

### 便捷断言函数

##### assert_response()
```python
def assert_response(response_data: Any = None) -> EnhancedAssertion
```
创建断言对象的便捷函数。

##### assert_success_response()
```python
def assert_success_response(response, expected_code: int = 200) -> EnhancedAssertion
```
断言成功响应的快捷函数。

##### assert_jmes()
```python
def assert_jmes(data: Any, path: str, expected_value: Any = None) -> EnhancedAssertion
```
JMESPath断言的便捷函数。

## 🔍 JMESPath辅助API

### JMESPathHelper

JMESPath查询辅助类。

```python
class JMESPathHelper:
    def __init__(self, data: Any)
```

#### 查询方法

##### search()
```python
def search(self, path: str) -> Any
```
执行JMESPath查询。

##### get_value()
```python
def get_value(self, path: str, default: Any = None) -> Any
```
获取值，支持默认值。

##### get_list()
```python
def get_list(self, path: str) -> List[Any]
```
获取列表结果，确保返回列表类型。

##### exists()
```python
def exists(self, path: str) -> bool
```
检查路径是否存在。

##### count()
```python
def count(self, path: str) -> int
```
计算查询结果的数量。

#### 高级查询方法

##### filter_by()
```python
def filter_by(self, list_path: str, condition: str) -> List[Any]
```
根据条件过滤列表。

**示例:**
```python
helper = jmes(data)
active_users = helper.filter_by("users", "status == 'active'")
```

##### sort_by()
```python
def sort_by(self, list_path: str, sort_key: str, reverse: bool = False) -> List[Any]
```
根据键排序列表。

##### group_by()
```python
def group_by(self, list_path: str, group_key: str) -> Dict[str, List[Any]]
```
根据键分组列表。

### 便捷函数

##### jmes()
```python
def jmes(data: Any) -> JMESPathHelper
```
创建JMESPath辅助器的便捷函数。

##### quick_search()
```python
def quick_search(data: Any, path: str, default: Any = None) -> Any
```
快速JMESPath查询。

## 📊 数据驱动API

### DataDriver

数据驱动测试类。

```python
class DataDriver:
    def __init__(self, data_dir: str = "data")
```

#### 数据加载方法

##### load_json()
```python
def load_json(self, file_path: str, encoding: str = 'utf-8') -> Union[List[Dict], Dict]
```
从JSON文件加载数据。

##### load_yaml()
```python
def load_yaml(self, file_path: str, encoding: str = 'utf-8') -> Union[List[Dict], Dict]
```
从YAML文件加载数据。

##### load_excel()
```python
def load_excel(self, file_path: str, sheet_name: str = None) -> List[Dict]
```
从Excel文件加载数据。

##### load_csv()
```python
def load_csv(self, file_path: str, encoding: str = 'utf-8') -> List[Dict]
```
从CSV文件加载数据。

#### 数据生成方法

##### generate_test_data()
```python
def generate_test_data(self, template: Dict, count: int = 1) -> List[Dict]
```
根据模板生成测试数据。

**参数:**
- `template` (Dict): 数据模板，支持Faker方法
- `count` (int): 生成数据条数

**示例:**
```python
template = {
    "name": "faker.name",
    "email": "faker.email",
    "age": 25
}
test_data = data_driver.generate_test_data(template, count=5)
```

### 便捷函数

##### load_test_data()
```python
def load_test_data(file_path: str, file_type: str = None) -> Union[List[Dict], Dict]
```
加载测试数据的便捷函数。

## 🌍 环境管理API

### EnvironmentManager

环境管理器类。

```python
class EnvironmentManager:
    def __init__(self, config_dir: str = "conf")
```

#### 配置方法

##### get_config()
```python
def get_config(self, key: str, default: Any = None) -> Any
```
获取配置值。

##### switch_env()
```python
def switch_env(self, env_name: str) -> None
```
切换环境。

##### get_base_url()
```python
def get_base_url(self, service_name: str = "default") -> str
```
获取服务基础URL。

### 便捷函数

##### get_config()
```python
def get_config(key: str, default: Any = None) -> Any
```
获取配置值的便捷函数。

##### get_base_url()
```python
def get_base_url(service_name: str = "default") -> str
```
获取基础URL的便捷函数。

##### switch_environment()
```python
def switch_environment(env_name: str) -> None
```
切换环境的便捷函数。

## 🎭 Mock服务API

### MockServer

Mock服务器类。

```python
class MockServer:
    def __init__(self, host: str = "localhost", port: int = 8888)
```

#### 服务器控制方法

##### start()
```python
def start(self) -> None
```
启动Mock服务器。

##### stop()
```python
def stop(self) -> None
```
停止Mock服务器。

#### 规则管理方法

##### add_rule()
```python
def add_rule(self, method: str, path: str, response: MockResponse,
             query_params: Dict = None, request_body: Dict = None) -> 'MockServer'
```
添加Mock规则。

##### reset_rules()
```python
def reset_rules(self) -> None
```
重置所有规则。

### MockResponse

Mock响应类。

```python
class MockResponse:
    def __init__(self, status_code: int = 200, headers: Dict[str, str] = None,
                 body: Any = None, delay: float = 0)
```

### 便捷函数

##### create_mock_response()
```python
def create_mock_response(status_code: int = 200, body: Any = None,
                        headers: Dict[str, str] = None, delay: float = 0) -> MockResponse
```
创建Mock响应的便捷函数。

## ⚡ 性能测试API

### PerformanceTester

性能测试器类。

```python
class PerformanceTester:
    def __init__(self)
```

#### 测试方法

##### load_test()
```python
def load_test(self, request_func: Callable, concurrent_users: int = 10,
              total_requests: int = 100, *args, **kwargs) -> PerformanceMetrics
```
负载测试。

##### stress_test()
```python
def stress_test(self, request_func: Callable, duration_seconds: int = 60,
                concurrent_users: int = 10, *args, **kwargs) -> PerformanceMetrics
```
压力测试。

### PerformanceMetrics

性能指标数据类。

```python
@dataclass
class PerformanceMetrics:
    total_requests: int
    successful_requests: int
    failed_requests: int
    total_time: float
    min_response_time: float
    max_response_time: float
    avg_response_time: float
    median_response_time: float
    p95_response_time: float
    p99_response_time: float
    requests_per_second: float
    error_rate: float
```

#### 方法

##### to_dict()
```python
def to_dict(self) -> Dict[str, Any]
```
转换为字典格式。

### 便捷函数

##### load_test()
```python
def load_test(request_func: Callable, concurrent_users: int = 10,
              total_requests: int = 100, *args, **kwargs) -> PerformanceMetrics
```
负载测试的便捷函数。

---

**下一步**: [用户指南](../user-guide/basic-usage.md) | [JMESPath指南](../user-guide/jmespath-guide.md)
