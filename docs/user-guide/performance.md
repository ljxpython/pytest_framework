# ⚡ 性能测试 - 让API跑得飞快

> "性能测试：发现瓶颈，优化体验，让用户爱上你的API！"

还在担心API在高并发下会崩溃？还在猜测系统能承受多少用户？性能测试让你心中有数，让API在任何情况下都稳如泰山！

## 🎯 为什么需要性能测试？

### 真实场景
你是不是遇到过这些噩梦：
- 😱 "双11活动一开始，服务器就挂了..."
- 🤦‍♂️ "平时好好的，用户一多就卡死"
- 😤 "老板问能支持多少用户，我只能说'应该可以吧'"
- 🙄 "新功能上线后，整个系统都变慢了"
- 😅 "用户投诉响应太慢，但我不知道慢在哪里"

性能测试帮你提前发现问题，避免线上翻车！

## 🚀 快速开始 - 第一个性能测试

### 最简单的负载测试

```python
from src.utils.performance import load_test
import requests

def simple_api_request():
    """简单的API请求函数"""
    return requests.get("https://httpbin.org/get")

# 执行负载测试
metrics = load_test(
    request_func=simple_api_request,
    concurrent_users=10,      # 10个并发用户
    total_requests=100        # 总共100个请求
)

# 查看结果
print(f"🎯 性能测试结果:")
print(f"   平均响应时间: {metrics.avg_response_time:.3f}s")
print(f"   95%响应时间: {metrics.p95_response_time:.3f}s")
print(f"   QPS: {metrics.requests_per_second:.2f}")
print(f"   成功率: {(1-metrics.error_rate)*100:.1f}%")

# 验证性能指标
assert metrics.avg_response_time < 2.0  # 平均响应时间小于2秒
assert metrics.error_rate < 0.05        # 错误率小于5%
assert metrics.requests_per_second > 5  # QPS大于5
```

### 在测试中使用性能测试

```python
import pytest
from src.utils.performance import load_test, stress_test

class TestAPIPerformance:
    """API性能测试类"""

    def setup_method(self):
        """测试前置设置"""
        from src.client.base_client import BaseClient
        self.client = BaseClient("https://httpbin.org")

    @pytest.mark.performance
    def test_get_users_performance(self):
        """用户列表性能测试"""

        def get_users_request():
            return self.client.get("/get?users=list")

        # 负载测试
        metrics = load_test(
            get_users_request,
            concurrent_users=5,
            total_requests=50
        )

        # 性能断言
        assert metrics.avg_response_time < 1.0    # 平均响应时间 < 1秒
        assert metrics.p95_response_time < 2.0    # 95%响应时间 < 2秒
        assert metrics.error_rate == 0            # 无错误
        assert metrics.requests_per_second > 10   # QPS > 10

        print(f"✅ 用户列表性能测试通过!")
        print(f"   并发用户: {5}")
        print(f"   平均响应时间: {metrics.avg_response_time:.3f}s")
        print(f"   QPS: {metrics.requests_per_second:.2f}")

    @pytest.mark.performance
    def test_create_user_performance(self):
        """用户创建性能测试"""

        def create_user_request():
            user_data = {
                "name": f"性能测试用户_{time.time()}",
                "email": f"perf_{int(time.time()*1000)}@example.com"
            }
            return self.client.post("/post", json=user_data)

        # 负载测试
        metrics = load_test(
            create_user_request,
            concurrent_users=3,
            total_requests=30
        )

        # 写操作性能要求相对宽松
        assert metrics.avg_response_time < 3.0    # 平均响应时间 < 3秒
        assert metrics.error_rate < 0.1           # 错误率 < 10%
        assert metrics.requests_per_second > 2    # QPS > 2

        print(f"✅ 用户创建性能测试通过!")
```

## 📊 性能测试类型

### 1. 负载测试 - 正常压力下的表现

```python
def test_normal_load():
    """正常负载测试"""

    def api_request():
        return requests.get("https://api.example.com/users")

    # 模拟正常业务负载
    metrics = load_test(
        api_request,
        concurrent_users=20,      # 20个并发用户
        total_requests=200        # 总共200个请求
    )

    # 正常负载下的性能要求
    assert metrics.avg_response_time < 1.0
    assert metrics.p95_response_time < 2.0
    assert metrics.error_rate < 0.01  # 错误率小于1%

    print(f"📊 正常负载测试结果:")
    print(f"   平均响应时间: {metrics.avg_response_time:.3f}s")
    print(f"   最大响应时间: {metrics.max_response_time:.3f}s")
    print(f"   QPS: {metrics.requests_per_second:.2f}")
```

### 2. 压力测试 - 找到系统极限

```python
def test_stress_load():
    """压力测试"""

    def api_request():
        return requests.get("https://api.example.com/users")

    # 持续压力测试
    metrics = stress_test(
        api_request,
        duration_seconds=60,      # 持续60秒
        concurrent_users=50       # 50个并发用户
    )

    # 压力测试下的基本要求
    assert metrics.error_rate < 0.05  # 错误率小于5%
    assert metrics.avg_response_time < 5.0  # 平均响应时间小于5秒

    print(f"🔥 压力测试结果:")
    print(f"   总请求数: {metrics.total_requests}")
    print(f"   成功请求数: {metrics.successful_requests}")
    print(f"   平均QPS: {metrics.requests_per_second:.2f}")
    print(f"   错误率: {metrics.error_rate:.2%}")
```

### 3. 峰值测试 - 突发流量处理

```python
def test_spike_load():
    """峰值测试"""
    import threading
    import time

    def api_request():
        return requests.get("https://api.example.com/users")

    # 模拟突发流量
    def spike_test():
        # 先进行正常负载
        normal_metrics = load_test(api_request, concurrent_users=10, total_requests=50)

        # 突然增加到高并发
        spike_metrics = load_test(api_request, concurrent_users=100, total_requests=200)

        # 再回到正常负载
        recovery_metrics = load_test(api_request, concurrent_users=10, total_requests=50)

        return normal_metrics, spike_metrics, recovery_metrics

    normal, spike, recovery = spike_test()

    # 验证系统能够处理突发流量
    assert spike.error_rate < 0.1  # 突发流量下错误率小于10%
    assert recovery.avg_response_time <= normal.avg_response_time * 1.2  # 恢复后性能接近正常

    print(f"⚡ 峰值测试结果:")
    print(f"   正常负载QPS: {normal.requests_per_second:.2f}")
    print(f"   峰值负载QPS: {spike.requests_per_second:.2f}")
    print(f"   恢复后QPS: {recovery.requests_per_second:.2f}")
```

## 🎯 性能指标详解

### 核心性能指标

```python
from src.utils.performance import PerformanceMetrics

def analyze_performance_metrics(metrics: PerformanceMetrics):
    """分析性能指标"""

    print(f"📈 详细性能分析:")
    print(f"   总请求数: {metrics.total_requests}")
    print(f"   成功请求数: {metrics.successful_requests}")
    print(f"   失败请求数: {metrics.failed_requests}")
    print(f"   总耗时: {metrics.total_time:.2f}s")
    print()

    print(f"⏱️  响应时间分析:")
    print(f"   最小响应时间: {metrics.min_response_time:.3f}s")
    print(f"   最大响应时间: {metrics.max_response_time:.3f}s")
    print(f"   平均响应时间: {metrics.avg_response_time:.3f}s")
    print(f"   中位数响应时间: {metrics.median_response_time:.3f}s")
    print(f"   95%响应时间: {metrics.p95_response_time:.3f}s")
    print(f"   99%响应时间: {metrics.p99_response_time:.3f}s")
    print()

    print(f"🚀 吞吐量分析:")
    print(f"   QPS (每秒请求数): {metrics.requests_per_second:.2f}")
    print(f"   错误率: {metrics.error_rate:.2%}")
    print()

    # 性能等级评估
    if metrics.avg_response_time < 0.1:
        performance_level = "🚀 极快"
    elif metrics.avg_response_time < 0.5:
        performance_level = "⚡ 很快"
    elif metrics.avg_response_time < 1.0:
        performance_level = "✅ 良好"
    elif metrics.avg_response_time < 2.0:
        performance_level = "⚠️  一般"
    else:
        performance_level = "🐌 较慢"

    print(f"🎯 性能等级: {performance_level}")

    # 给出优化建议
    if metrics.error_rate > 0.05:
        print("💡 建议: 错误率较高，需要检查服务稳定性")

    if metrics.p95_response_time > metrics.avg_response_time * 3:
        print("💡 建议: 响应时间波动较大，可能存在性能瓶颈")

    if metrics.requests_per_second < 10:
        print("💡 建议: QPS较低，考虑优化服务器性能或增加缓存")

# 使用示例
def test_with_detailed_analysis():
    def api_request():
        return requests.get("https://httpbin.org/delay/0.1")  # 模拟100ms延迟

    metrics = load_test(api_request, concurrent_users=10, total_requests=100)
    analyze_performance_metrics(metrics)


## 🎨 高级性能测试场景

### 数据库性能测试

```python
def test_database_performance():
    """数据库操作性能测试"""

    def create_user_with_db():
        """创建用户（涉及数据库操作）"""
        user_data = {
            "name": f"用户_{int(time.time()*1000)}",
            "email": f"user_{int(time.time()*1000)}@example.com",
            "department": "技术部"
        }
        return requests.post("https://api.example.com/users", json=user_data)

    # 数据库写操作性能测试
    write_metrics = load_test(
        create_user_with_db,
        concurrent_users=5,    # 数据库写操作并发不宜过高
        total_requests=50
    )

    # 数据库写操作性能要求
    assert write_metrics.avg_response_time < 2.0
    assert write_metrics.error_rate < 0.02

    def query_users():
        """查询用户（数据库读操作）"""
        return requests.get("https://api.example.com/users?page=1&size=20")

    # 数据库读操作性能测试
    read_metrics = load_test(
        query_users,
        concurrent_users=20,   # 读操作可以有更高并发
        total_requests=200
    )

    # 数据库读操作性能要求
    assert read_metrics.avg_response_time < 0.5
    assert read_metrics.error_rate < 0.01

    print(f"💾 数据库性能测试结果:")
    print(f"   写操作平均响应时间: {write_metrics.avg_response_time:.3f}s")
    print(f"   读操作平均响应时间: {read_metrics.avg_response_time:.3f}s")
    print(f"   写操作QPS: {write_metrics.requests_per_second:.2f}")
    print(f"   读操作QPS: {read_metrics.requests_per_second:.2f}")


### 缓存性能测试

```python
def test_cache_performance():
    """缓存性能测试"""

    # 第一次请求（缓存未命中）
    def first_request():
        return requests.get("https://api.example.com/users/123")

    first_metrics = load_test(first_request, concurrent_users=1, total_requests=1)

    # 后续请求（缓存命中）
    def cached_request():
        return requests.get("https://api.example.com/users/123")

    cached_metrics = load_test(cached_request, concurrent_users=10, total_requests=100)

    # 缓存应该显著提升性能
    cache_improvement = first_metrics.avg_response_time / cached_metrics.avg_response_time

    assert cache_improvement > 2  # 缓存至少提升2倍性能
    assert cached_metrics.avg_response_time < 0.1  # 缓存响应时间小于100ms

    print(f"🚀 缓存性能测试结果:")
    print(f"   首次请求响应时间: {first_metrics.avg_response_time:.3f}s")
    print(f"   缓存请求响应时间: {cached_metrics.avg_response_time:.3f}s")
    print(f"   性能提升倍数: {cache_improvement:.1f}x")


## 💡 性能测试最佳实践

### 1. 测试环境准备

```python
class PerformanceTestSetup:
    """性能测试环境准备"""

    @staticmethod
    def prepare_test_data():
        """准备测试数据"""
        # 创建足够的测试数据
        test_users = []
        for i in range(1000):
            test_users.append({
                "id": i + 1,
                "name": f"测试用户{i+1}",
                "email": f"user{i+1}@example.com"
            })
        return test_users

    @staticmethod
    def cleanup_test_data():
        """清理测试数据"""
        # 测试后清理数据，避免影响后续测试
        pass

    @staticmethod
    def warm_up_system():
        """系统预热"""
        # 发送一些预热请求，让系统进入稳定状态
        for _ in range(10):
            requests.get("https://api.example.com/health")
            time.sleep(0.1)


### 2. 性能基准管理

```python
class PerformanceBenchmark:
    """性能基准管理"""

    def __init__(self):
        self.benchmarks = {
            "user_list": {"avg_response_time": 0.5, "qps": 100},
            "user_create": {"avg_response_time": 1.0, "qps": 50},
            "user_update": {"avg_response_time": 0.8, "qps": 60},
            "user_delete": {"avg_response_time": 0.3, "qps": 80}
        }

    def check_performance(self, test_name, metrics):
        """检查性能是否达标"""
        if test_name not in self.benchmarks:
            print(f"⚠️  未找到 {test_name} 的性能基准")
            return True

        benchmark = self.benchmarks[test_name]

        # 检查响应时间
        if metrics.avg_response_time > benchmark["avg_response_time"]:
            print(f"❌ {test_name} 响应时间超标: {metrics.avg_response_time:.3f}s > {benchmark['avg_response_time']}s")
            return False

        # 检查QPS
        if metrics.requests_per_second < benchmark["qps"]:
            print(f"❌ {test_name} QPS不达标: {metrics.requests_per_second:.2f} < {benchmark['qps']}")
            return False

        print(f"✅ {test_name} 性能达标")
        return True

# 使用性能基准
benchmark = PerformanceBenchmark()

def test_with_benchmark():
    def user_list_request():
        return requests.get("https://api.example.com/users")

    metrics = load_test(user_list_request, concurrent_users=10, total_requests=100)

    # 检查是否达到性能基准
    assert benchmark.check_performance("user_list", metrics)


## 🎯 总结

性能测试让你的API变得：
- ⚡ **快速** - 发现性能瓶颈，优化响应时间
- 🛡️ **稳定** - 验证高并发下的系统稳定性
- 📊 **可预测** - 了解系统容量和极限
- 🎯 **可靠** - 确保用户体验始终良好
- 🚀 **可扩展** - 为系统扩容提供数据支持

记住：**性能测试不是一次性的，而是持续的过程！**

现在就开始性能测试，让你的API在任何情况下都能稳定快速地服务用户！

---

**小贴士**: 性能测试要在接近生产环境的条件下进行，结果才有参考价值！
```
