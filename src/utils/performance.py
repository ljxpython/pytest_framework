"""
性能测试工具模块

提供接口性能监控和分析功能
"""

import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

import requests

from src.utils.log_moudle import logger


@dataclass
class PerformanceMetrics:
    """性能指标数据类"""

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

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "total_time": round(self.total_time, 3),
            "min_response_time": round(self.min_response_time, 3),
            "max_response_time": round(self.max_response_time, 3),
            "avg_response_time": round(self.avg_response_time, 3),
            "median_response_time": round(self.median_response_time, 3),
            "p95_response_time": round(self.p95_response_time, 3),
            "p99_response_time": round(self.p99_response_time, 3),
            "requests_per_second": round(self.requests_per_second, 2),
            "error_rate": round(self.error_rate * 100, 2),
        }


@dataclass
class RequestResult:
    """单次请求结果"""

    success: bool
    response_time: float
    status_code: Optional[int] = None
    error_message: Optional[str] = None


class PerformanceTester:
    """性能测试器"""

    def __init__(self):
        """初始化性能测试器"""
        self.logger = logger

    def _execute_request(
        self, request_func: Callable, *args, **kwargs
    ) -> RequestResult:
        """
        执行单次请求

        Args:
            request_func: 请求函数
            *args: 位置参数
            **kwargs: 关键字参数

        Returns:
            请求结果
        """
        start_time = time.time()
        try:
            response = request_func(*args, **kwargs)
            end_time = time.time()

            response_time = end_time - start_time

            # 检查响应状态
            if hasattr(response, "status_code"):
                success = 200 <= response.status_code < 400
                status_code = response.status_code
            else:
                success = True
                status_code = None

            return RequestResult(
                success=success, response_time=response_time, status_code=status_code
            )

        except Exception as e:
            end_time = time.time()
            response_time = end_time - start_time

            return RequestResult(
                success=False, response_time=response_time, error_message=str(e)
            )

    def load_test(
        self,
        request_func: Callable,
        concurrent_users: int = 10,
        total_requests: int = 100,
        *args,
        **kwargs,
    ) -> PerformanceMetrics:
        """
        负载测试

        Args:
            request_func: 请求函数
            concurrent_users: 并发用户数
            total_requests: 总请求数
            *args: 传递给请求函数的位置参数
            **kwargs: 传递给请求函数的关键字参数

        Returns:
            性能指标
        """
        self.logger.info(
            f"开始负载测试: {concurrent_users} 并发用户, {total_requests} 总请求"
        )

        results: List[RequestResult] = []
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            # 提交所有任务
            futures = [
                executor.submit(self._execute_request, request_func, *args, **kwargs)
                for _ in range(total_requests)
            ]

            # 收集结果
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"请求执行失败: {e}")
                    results.append(
                        RequestResult(
                            success=False, response_time=0, error_message=str(e)
                        )
                    )

        end_time = time.time()
        total_time = end_time - start_time

        # 计算性能指标
        return self._calculate_metrics(results, total_time)

    def stress_test(
        self,
        request_func: Callable,
        duration_seconds: int = 60,
        concurrent_users: int = 10,
        *args,
        **kwargs,
    ) -> PerformanceMetrics:
        """
        压力测试

        Args:
            request_func: 请求函数
            duration_seconds: 测试持续时间（秒）
            concurrent_users: 并发用户数
            *args: 传递给请求函数的位置参数
            **kwargs: 传递给请求函数的关键字参数

        Returns:
            性能指标
        """
        self.logger.info(
            f"开始压力测试: {concurrent_users} 并发用户, 持续 {duration_seconds} 秒"
        )

        results: List[RequestResult] = []
        start_time = time.time()
        end_time = start_time + duration_seconds

        with ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = []

            # 在指定时间内持续提交任务
            while time.time() < end_time:
                future = executor.submit(
                    self._execute_request, request_func, *args, **kwargs
                )
                futures.append(future)

                # 避免提交过多任务导致内存问题
                if len(futures) >= concurrent_users * 10:
                    # 等待一些任务完成
                    completed_futures = []
                    for f in futures:
                        if f.done():
                            completed_futures.append(f)

                    for f in completed_futures:
                        try:
                            result = f.result()
                            results.append(result)
                        except Exception as e:
                            self.logger.error(f"请求执行失败: {e}")
                            results.append(
                                RequestResult(
                                    success=False, response_time=0, error_message=str(e)
                                )
                            )
                        futures.remove(f)

            # 等待剩余任务完成
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"请求执行失败: {e}")
                    results.append(
                        RequestResult(
                            success=False, response_time=0, error_message=str(e)
                        )
                    )

        actual_duration = time.time() - start_time

        # 计算性能指标
        return self._calculate_metrics(results, actual_duration)

    def _calculate_metrics(
        self, results: List[RequestResult], total_time: float
    ) -> PerformanceMetrics:
        """
        计算性能指标

        Args:
            results: 请求结果列表
            total_time: 总耗时

        Returns:
            性能指标
        """
        if not results:
            raise ValueError("没有请求结果数据")

        # 基本统计
        total_requests = len(results)
        successful_requests = sum(1 for r in results if r.success)
        failed_requests = total_requests - successful_requests

        # 响应时间统计
        response_times = [r.response_time for r in results]
        min_response_time = min(response_times)
        max_response_time = max(response_times)
        avg_response_time = statistics.mean(response_times)
        median_response_time = statistics.median(response_times)

        # 百分位数
        sorted_times = sorted(response_times)
        p95_index = int(len(sorted_times) * 0.95)
        p99_index = int(len(sorted_times) * 0.99)
        p95_response_time = (
            sorted_times[p95_index]
            if p95_index < len(sorted_times)
            else max_response_time
        )
        p99_response_time = (
            sorted_times[p99_index]
            if p99_index < len(sorted_times)
            else max_response_time
        )

        # 吞吐量和错误率
        requests_per_second = total_requests / total_time if total_time > 0 else 0
        error_rate = failed_requests / total_requests if total_requests > 0 else 0

        metrics = PerformanceMetrics(
            total_requests=total_requests,
            successful_requests=successful_requests,
            failed_requests=failed_requests,
            total_time=total_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            avg_response_time=avg_response_time,
            median_response_time=median_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time,
            requests_per_second=requests_per_second,
            error_rate=error_rate,
        )

        self.logger.info(f"性能测试完成: {metrics.to_dict()}")
        return metrics


# 全局性能测试器实例
performance_tester = PerformanceTester()


def load_test(
    request_func: Callable,
    concurrent_users: int = 10,
    total_requests: int = 100,
    *args,
    **kwargs,
) -> PerformanceMetrics:
    """负载测试的便捷函数"""
    return performance_tester.load_test(
        request_func, concurrent_users, total_requests, *args, **kwargs
    )


def stress_test(
    request_func: Callable,
    duration_seconds: int = 60,
    concurrent_users: int = 10,
    *args,
    **kwargs,
) -> PerformanceMetrics:
    """压力测试的便捷函数"""
    return performance_tester.stress_test(
        request_func, duration_seconds, concurrent_users, *args, **kwargs
    )
