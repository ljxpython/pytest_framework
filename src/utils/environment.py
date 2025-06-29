"""
环境管理工具模块

支持多环境配置管理和动态切换
"""

import os
from typing import Any, Dict, Optional

from dynaconf import Dynaconf

from src.utils.log_moudle import logger


class EnvironmentManager:
    """环境管理器"""

    def __init__(self, config_dir: str = "conf"):
        """
        初始化环境管理器

        Args:
            config_dir: 配置文件目录
        """
        self.config_dir = config_dir
        self.logger = logger
        self._current_env = None
        self._settings = None
        self._load_settings()

    def _load_settings(self):
        """加载配置设置"""
        try:
            self._settings = Dynaconf(
                root_path=self.config_dir,
                envvar_prefix="PYTEST_FRAMEWORK",
                settings_files=[
                    "settings.yaml",
                    "settings.local.yaml",
                    ".secrets.yaml",
                ],
                environments=True,
                load_dotenv=True,
                env=os.getenv("ENV", "boe"),  # 默认环境
            )
            self._current_env = self._settings.current_env
            self.logger.info(f"配置加载成功，当前环境: {self._current_env}")
        except Exception as e:
            self.logger.error(f"配置加载失败: {e}")
            raise

    @property
    def current_env(self) -> str:
        """获取当前环境"""
        return self._current_env

    @property
    def settings(self) -> Dynaconf:
        """获取配置对象"""
        return self._settings

    def switch_env(self, env_name: str):
        """
        切换环境

        Args:
            env_name: 环境名称
        """
        try:
            self._settings.setenv(env_name)
            self._current_env = env_name
            self.logger.info(f"环境已切换到: {env_name}")
        except Exception as e:
            self.logger.error(f"环境切换失败: {e}")
            raise

    def get_config(self, key: str, default: Any = None) -> Any:
        """
        获取配置值

        Args:
            key: 配置键，支持点号分隔的嵌套键
            default: 默认值

        Returns:
            配置值
        """
        try:
            return self._settings.get(key, default)
        except Exception as e:
            self.logger.warning(f"获取配置失败: {key}, 使用默认值: {default}")
            return default

    def get_db_config(self) -> Dict[str, Any]:
        """获取数据库配置"""
        return self.get_config("DB", {})

    def get_api_config(self) -> Dict[str, Any]:
        """获取API配置"""
        return self.get_config("API", {})

    def get_test_config(self) -> Dict[str, Any]:
        """获取测试配置"""
        return self.get_config("TEST", {})

    def get_base_url(self, service_name: str = "default") -> str:
        """
        获取服务基础URL

        Args:
            service_name: 服务名称

        Returns:
            基础URL
        """
        api_config = self.get_api_config()
        if service_name in api_config:
            return api_config[service_name].get("base_url", "")
        return api_config.get("base_url", "")

    def get_timeout(self, service_name: str = "default") -> int:
        """
        获取超时配置

        Args:
            service_name: 服务名称

        Returns:
            超时时间（秒）
        """
        api_config = self.get_api_config()
        if service_name in api_config:
            return api_config[service_name].get("timeout", 30)
        return api_config.get("timeout", 30)

    def is_debug_mode(self) -> bool:
        """是否为调试模式"""
        return self.get_config("DEBUG", False)

    def get_log_level(self) -> str:
        """获取日志级别"""
        return self.get_config("LOG_LEVEL", "INFO")

    def get_parallel_workers(self) -> int:
        """获取并行执行的工作进程数"""
        return self.get_config("PARALLEL_WORKERS", 1)

    def get_retry_times(self) -> int:
        """获取重试次数"""
        return self.get_config("RETRY_TIMES", 0)

    def get_allure_dir(self) -> str:
        """获取Allure报告目录"""
        return self.get_config("ALLURE_DIR", "output/allure-result")

    def list_environments(self) -> list:
        """列出所有可用环境"""
        try:
            # 从配置文件中获取环境列表
            environments = []
            if hasattr(self._settings, "_environments"):
                environments = list(self._settings._environments.keys())
            return environments
        except Exception as e:
            self.logger.error(f"获取环境列表失败: {e}")
            return []

    def validate_environment(self, env_name: str) -> bool:
        """
        验证环境是否有效

        Args:
            env_name: 环境名称

        Returns:
            是否有效
        """
        available_envs = self.list_environments()
        return env_name in available_envs

    def export_env_vars(self):
        """导出环境变量"""
        try:
            # 导出当前环境的配置为环境变量
            for key, value in self._settings.as_dict().items():
                if isinstance(value, (str, int, float, bool)):
                    os.environ[f"PYTEST_FRAMEWORK_{key.upper()}"] = str(value)

            self.logger.info("环境变量导出成功")
        except Exception as e:
            self.logger.error(f"环境变量导出失败: {e}")


# 全局环境管理器实例
env_manager = EnvironmentManager()


def get_current_env() -> str:
    """获取当前环境"""
    return env_manager.current_env


def get_config(key: str, default: Any = None) -> Any:
    """获取配置值的便捷函数"""
    return env_manager.get_config(key, default)


def get_base_url(service_name: str = "default") -> str:
    """获取基础URL的便捷函数"""
    return env_manager.get_base_url(service_name)


def switch_environment(env_name: str):
    """切换环境的便捷函数"""
    env_manager.switch_env(env_name)
