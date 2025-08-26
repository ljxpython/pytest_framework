"""
数据驱动测试工具模块

支持从多种数据源读取测试数据，包括Excel、CSV、JSON、YAML等
"""

import csv
import json
import os
from pathlib import Path
from typing import Any, Dict, Generator, List, Optional, Union

import pandas as pd
import yaml
from faker import Faker

from src.utils.log_moudle import logger


class DataDriver:
    """数据驱动测试类"""

    def __init__(self, data_dir: str = "data"):
        """
        初始化数据驱动器

        Args:
            data_dir: 数据文件目录
        """
        # 确保data_dir是绝对路径
        if not os.path.isabs(data_dir):
            # 获取项目根目录
            project_root = self._find_project_root()
            self.data_dir = Path(project_root) / data_dir
        else:
            self.data_dir = Path(data_dir)

        self.faker = Faker("zh_CN")  # 中文数据生成器
        self.logger = logger

    def _find_project_root(self) -> str:
        """查找项目根目录"""
        current_dir = os.path.dirname(os.path.abspath(__file__))

        # 向上查找项目标识文件
        while current_dir != os.path.dirname(current_dir):
            # 检查常见的项目标识文件
            for marker in [
                "pyproject.toml",
                "setup.py",
                "requirements.txt",
                "pytest.ini",
                ".git",
            ]:
                if os.path.exists(os.path.join(current_dir, marker)):
                    return current_dir
            current_dir = os.path.dirname(current_dir)

        # 如果找不到，返回当前文件所在目录的上上级目录（假设是 src/utils/）
        return os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )

    def load_excel(self, file_path: str, sheet_name: str = None) -> List[Dict]:
        """
        从Excel文件加载测试数据

        Args:
            file_path: Excel文件路径
            sheet_name: 工作表名称，默认为第一个工作表

        Returns:
            测试数据列表
        """
        full_path = self.data_dir / file_path
        try:
            if sheet_name:
                df = pd.read_excel(full_path, sheet_name=sheet_name)
            else:
                df = pd.read_excel(full_path)

            # 将NaN值替换为None
            df = df.where(pd.notnull(df), None)
            data = df.to_dict("records")

            self.logger.info(f"从Excel文件加载了 {len(data)} 条测试数据: {full_path}")
            return data

        except Exception as e:
            self.logger.error(f"加载Excel文件失败: {full_path}, 错误: {e}")
            raise

    def load_csv(self, file_path: str, encoding: str = "utf-8") -> List[Dict]:
        """
        从CSV文件加载测试数据

        Args:
            file_path: CSV文件路径
            encoding: 文件编码

        Returns:
            测试数据列表
        """
        full_path = self.data_dir / file_path
        try:
            data = []
            with open(full_path, "r", encoding=encoding) as file:
                reader = csv.DictReader(file)
                data = list(reader)

            self.logger.info(f"从CSV文件加载了 {len(data)} 条测试数据: {full_path}")
            return data

        except Exception as e:
            self.logger.error(f"加载CSV文件失败: {full_path}, 错误: {e}")
            raise

    def load_json(
        self, file_path: str, encoding: str = "utf-8"
    ) -> Union[List[Dict], Dict]:
        """
        从JSON文件加载测试数据

        Args:
            file_path: JSON文件路径
            encoding: 文件编码

        Returns:
            测试数据
        """
        full_path = self.data_dir / file_path
        try:
            with open(full_path, "r", encoding=encoding) as file:
                data = json.load(file)

            count = len(data) if isinstance(data, list) else 1
            self.logger.info(f"从JSON文件加载了 {count} 条测试数据: {full_path}")
            return data

        except Exception as e:
            self.logger.error(f"加载JSON文件失败: {full_path}, 错误: {e}")
            raise

    def load_yaml(
        self, file_path: str, encoding: str = "utf-8"
    ) -> Union[List[Dict], Dict]:
        """
        从YAML文件加载测试数据

        Args:
            file_path: YAML文件路径
            encoding: 文件编码

        Returns:
            测试数据
        """
        full_path = self.data_dir / file_path
        try:
            with open(full_path, "r", encoding=encoding) as file:
                data = yaml.safe_load(file)

            count = len(data) if isinstance(data, list) else 1
            self.logger.info(f"从YAML文件加载了 {count} 条测试数据: {full_path}")
            return data

        except Exception as e:
            self.logger.error(f"加载YAML文件失败: {full_path}, 错误: {e}")
            raise

    def generate_test_data(self, template: Dict, count: int = 1) -> List[Dict]:
        """
        根据模板生成测试数据

        Args:
            template: 数据模板，支持Faker方法
            count: 生成数据条数

        Returns:
            生成的测试数据列表
        """
        data_list = []

        for _ in range(count):
            data = {}
            for key, value in template.items():
                if isinstance(value, str) and value.startswith("faker."):
                    # 执行Faker方法
                    faker_method = value.replace("faker.", "")
                    try:
                        data[key] = getattr(self.faker, faker_method)()
                    except AttributeError:
                        self.logger.warning(f"Faker方法不存在: {faker_method}")
                        data[key] = value
                else:
                    data[key] = value
            data_list.append(data)

        self.logger.info(f"生成了 {count} 条测试数据")
        return data_list

    def save_data(
        self,
        data: Union[List[Dict], Dict],
        file_path: str,
        file_type: str = "json",
        encoding: str = "utf-8",
    ):
        """
        保存数据到文件

        Args:
            data: 要保存的数据
            file_path: 文件路径
            file_type: 文件类型 (json, yaml, csv, excel)
            encoding: 文件编码
        """
        full_path = self.data_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if file_type.lower() == "json":
                with open(full_path, "w", encoding=encoding) as file:
                    json.dump(data, file, ensure_ascii=False, indent=2)

            elif file_type.lower() == "yaml":
                with open(full_path, "w", encoding=encoding) as file:
                    yaml.dump(data, file, allow_unicode=True, default_flow_style=False)

            elif file_type.lower() == "csv":
                if isinstance(data, list) and data:
                    df = pd.DataFrame(data)
                    df.to_csv(full_path, index=False, encoding=encoding)
                else:
                    raise ValueError("CSV格式需要列表数据")

            elif file_type.lower() == "excel":
                if isinstance(data, list) and data:
                    df = pd.DataFrame(data)
                    df.to_excel(full_path, index=False)
                else:
                    raise ValueError("Excel格式需要列表数据")

            else:
                raise ValueError(f"不支持的文件类型: {file_type}")

            self.logger.info(f"数据已保存到: {full_path}")

        except Exception as e:
            self.logger.error(f"保存数据失败: {full_path}, 错误: {e}")
            raise


# 全局数据驱动器实例
data_driver = DataDriver()


def load_test_data(file_path: str, file_type: str = None) -> Union[List[Dict], Dict]:
    """
    加载测试数据的便捷函数

    Args:
        file_path: 文件路径
        file_type: 文件类型，如果不指定则根据文件扩展名判断

    Returns:
        测试数据
    """
    if file_type is None:
        file_type = Path(file_path).suffix.lower().lstrip(".")

    if file_type in ["xlsx", "xls"]:
        return data_driver.load_excel(file_path)
    elif file_type == "csv":
        return data_driver.load_csv(file_path)
    elif file_type == "json":
        return data_driver.load_json(file_path)
    elif file_type in ["yaml", "yml"]:
        return data_driver.load_yaml(file_path)
    else:
        raise ValueError(f"不支持的文件类型: {file_type}")


def parametrize_from_file(file_path: str, file_type: str = None):
    """
    从文件生成pytest参数化装饰器的数据

    Args:
        file_path: 文件路径
        file_type: 文件类型

    Returns:
        参数化数据
    """
    data = load_test_data(file_path, file_type)
    if isinstance(data, list):
        return data
    else:
        return [data]
