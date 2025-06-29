"""
Mock服务器工具模块

提供轻量级的Mock服务器，用于模拟API响应
"""

import json
import threading
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, List, Optional
from urllib.parse import parse_qs, urlparse

from src.utils.log_moudle import logger


class MockResponse:
    """Mock响应类"""

    def __init__(
        self,
        status_code: int = 200,
        headers: Dict[str, str] = None,
        body: Any = None,
        delay: float = 0,
    ):
        """
        初始化Mock响应

        Args:
            status_code: HTTP状态码
            headers: 响应头
            body: 响应体
            delay: 响应延迟（秒）
        """
        self.status_code = status_code
        self.headers = headers or {"Content-Type": "application/json"}
        self.body = body or {}
        self.delay = delay


class MockRule:
    """Mock规则类"""

    def __init__(
        self,
        method: str,
        path: str,
        response: MockResponse,
        query_params: Dict = None,
        request_body: Dict = None,
    ):
        """
        初始化Mock规则

        Args:
            method: HTTP方法
            path: 请求路径
            response: Mock响应
            query_params: 查询参数匹配条件
            request_body: 请求体匹配条件
        """
        self.method = method.upper()
        self.path = path
        self.response = response
        self.query_params = query_params or {}
        self.request_body = request_body or {}
        self.call_count = 0

    def matches(
        self,
        method: str,
        path: str,
        query_params: Dict = None,
        request_body: Dict = None,
    ) -> bool:
        """
        检查请求是否匹配规则

        Args:
            method: HTTP方法
            path: 请求路径
            query_params: 查询参数
            request_body: 请求体

        Returns:
            是否匹配
        """
        # 检查方法和路径
        if self.method != method.upper() or self.path != path:
            return False

        # 检查查询参数
        if self.query_params:
            query_params = query_params or {}
            for key, value in self.query_params.items():
                if key not in query_params or query_params[key] != value:
                    return False

        # 检查请求体
        if self.request_body:
            request_body = request_body or {}
            for key, value in self.request_body.items():
                if key not in request_body or request_body[key] != value:
                    return False

        return True


class MockRequestHandler(BaseHTTPRequestHandler):
    """Mock请求处理器"""

    def log_message(self, format, *args):
        """重写日志方法，使用自定义logger"""
        logger.info(f"Mock Server: {format % args}")

    def do_GET(self):
        """处理GET请求"""
        self._handle_request("GET")

    def do_POST(self):
        """处理POST请求"""
        self._handle_request("POST")

    def do_PUT(self):
        """处理PUT请求"""
        self._handle_request("PUT")

    def do_DELETE(self):
        """处理DELETE请求"""
        self._handle_request("DELETE")

    def do_PATCH(self):
        """处理PATCH请求"""
        self._handle_request("PATCH")

    def _handle_request(self, method: str):
        """处理请求的通用方法"""
        try:
            # 解析请求
            parsed_url = urlparse(self.path)
            path = parsed_url.path
            query_params = parse_qs(parsed_url.query)

            # 读取请求体
            request_body = {}
            if method in ["POST", "PUT", "PATCH"]:
                content_length = int(self.headers.get("Content-Length", 0))
                if content_length > 0:
                    body_data = self.rfile.read(content_length)
                    try:
                        request_body = json.loads(body_data.decode("utf-8"))
                    except json.JSONDecodeError:
                        request_body = {"raw": body_data.decode("utf-8")}

            # 查找匹配的规则
            mock_server = getattr(self.server, "mock_server", None)
            if mock_server:
                response = mock_server.find_response(
                    method, path, query_params, request_body
                )
                if response:
                    # 模拟延迟
                    if response.delay > 0:
                        time.sleep(response.delay)

                    # 发送响应
                    self.send_response(response.status_code)
                    for key, value in response.headers.items():
                        self.send_header(key, value)
                    self.end_headers()

                    # 发送响应体
                    if isinstance(response.body, (dict, list)):
                        response_data = json.dumps(response.body, ensure_ascii=False)
                    else:
                        response_data = str(response.body)

                    self.wfile.write(response_data.encode("utf-8"))
                    return

            # 没有找到匹配的规则，返回404
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {
                "error": "Not Found",
                "message": f"No mock rule found for {method} {path}",
            }
            self.wfile.write(json.dumps(error_response).encode("utf-8"))

        except Exception as e:
            logger.error(f"Mock服务器处理请求失败: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            error_response = {"error": "Internal Server Error", "message": str(e)}
            self.wfile.write(json.dumps(error_response).encode("utf-8"))


class MockServer:
    """Mock服务器类"""

    def __init__(self, host: str = "localhost", port: int = 8888):
        """
        初始化Mock服务器

        Args:
            host: 服务器主机
            port: 服务器端口
        """
        self.host = host
        self.port = port
        self.rules: List[MockRule] = []
        self.server = None
        self.server_thread = None
        self.logger = logger

    def add_rule(
        self,
        method: str,
        path: str,
        response: MockResponse,
        query_params: Dict = None,
        request_body: Dict = None,
    ) -> "MockServer":
        """
        添加Mock规则

        Args:
            method: HTTP方法
            path: 请求路径
            response: Mock响应
            query_params: 查询参数匹配条件
            request_body: 请求体匹配条件

        Returns:
            Mock服务器实例（支持链式调用）
        """
        rule = MockRule(method, path, response, query_params, request_body)
        self.rules.append(rule)
        self.logger.info(f"添加Mock规则: {method} {path}")
        return self

    def find_response(
        self,
        method: str,
        path: str,
        query_params: Dict = None,
        request_body: Dict = None,
    ) -> Optional[MockResponse]:
        """
        查找匹配的响应

        Args:
            method: HTTP方法
            path: 请求路径
            query_params: 查询参数
            request_body: 请求体

        Returns:
            匹配的响应或None
        """
        for rule in self.rules:
            if rule.matches(method, path, query_params, request_body):
                rule.call_count += 1
                self.logger.info(
                    f"匹配Mock规则: {method} {path} (调用次数: {rule.call_count})"
                )
                return rule.response

        self.logger.warning(f"未找到匹配的Mock规则: {method} {path}")
        return None

    def start(self):
        """启动Mock服务器"""
        try:
            self.server = HTTPServer((self.host, self.port), MockRequestHandler)
            self.server.mock_server = self  # 将Mock服务器实例传递给请求处理器

            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()

            self.logger.info(f"Mock服务器已启动: http://{self.host}:{self.port}")

        except Exception as e:
            self.logger.error(f"Mock服务器启动失败: {e}")
            raise

    def stop(self):
        """停止Mock服务器"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
            self.logger.info("Mock服务器已停止")

    def reset_rules(self):
        """重置所有规则"""
        self.rules.clear()
        self.logger.info("Mock规则已重置")

    def get_call_count(self, method: str, path: str) -> int:
        """
        获取指定规则的调用次数

        Args:
            method: HTTP方法
            path: 请求路径

        Returns:
            调用次数
        """
        for rule in self.rules:
            if rule.method == method.upper() and rule.path == path:
                return rule.call_count
        return 0

    @property
    def base_url(self) -> str:
        """获取Mock服务器的基础URL"""
        return f"http://{self.host}:{self.port}"


# 全局Mock服务器实例
mock_server = MockServer()


def create_mock_response(
    status_code: int = 200,
    body: Any = None,
    headers: Dict[str, str] = None,
    delay: float = 0,
) -> MockResponse:
    """创建Mock响应的便捷函数"""
    return MockResponse(status_code, headers, body, delay)


def start_mock_server(host: str = "localhost", port: int = 8888) -> MockServer:
    """启动Mock服务器的便捷函数"""
    global mock_server
    mock_server = MockServer(host, port)
    mock_server.start()
    return mock_server
