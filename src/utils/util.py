"""
存放一些在测试过程中,可能经常用到的函数,方便复用

"""

import hashlib
import random
import re
import string
import time
from typing import Callable, Optional, TypeVar
from urllib.parse import urlparse

import humps
import requests

from conf.config import settings
from src.utils.log_moudle import logger

# config = settings.client_config


def wait_for(condition: Callable, timeout: int = 30, interval: int = 1):
    start_time = time.time()
    try_times = 0
    while not condition():
        try_times += 1
        run_time = time.time() - start_time
        logger.info(f"Wait for {round(run_time,2)} seconds, try {try_times} times.")
        if run_time >= timeout:
            return
        time.sleep(interval)


def remove_empty_values(
    obj: list | dict, empty_values: Optional[list] = None
) -> dict | list:
    """移除列表或字典中的空值

    Args:
        obj (list | dict): 要操作的对象
        empty_values (Optional[list], optional): 要移除的空值列表，默认值移除 None. Defaults to None.

    Returns:
        dict | list: 移除空值后的对象
    """
    if empty_values is None:
        empty_values = [None, ""]  # 默认移除 None 和 空字符串
    if isinstance(obj, dict):
        return {
            k: remove_empty_values(v, empty_values)
            for k, v in obj.items()
            if v not in empty_values
        }
    elif isinstance(obj, list):
        return [
            remove_empty_values(item, empty_values)
            for item in obj
            if item not in empty_values
        ]
    else:
        return obj


T = TypeVar("T")


def trimmed_split(
    s: str, seps: str | tuple[str, str] = (";", ","), remove_empty_item=True
) -> list[str]:
    """Given a string s, split is by one of one of the seps."""
    s = s.strip()
    for sep in seps:
        if sep not in s:
            continue
        data = [
            item.strip() for item in s.split(sep) if remove_empty_item and item.strip()
        ]
        return data
    return [item for item in [s] if remove_empty_item and item]


def ensure_a_list(data: Optional[str] | list[str] | tuple[str]) -> list[str]:
    """Ensure data is a list or wrap it in a list"""
    if not data:
        return []
    if isinstance(data, str):  # 如果输入是字符串
        data_list = trimmed_split(data)
    elif isinstance(data, (list, tuple)):  # 如果输入是列表或元组
        data_list = list(data)
    return data_list


def to_camel_case(key: str) -> str:
    """
    humps库地址后续可以研究大小驼峰转换
    https://github.com/nficano/humps?tab=readme-ov-file#converting-dictionary-keys
    """
    # 特殊简写处理
    if key == "md5":
        return "MD5"
    return humps.pascalize(key)


def to_snake_case(key: str) -> str:
    return humps.decamelize(key)


def expression_to_camel_case(expression: str):
    """
    将表达式中的key转为大驼峰
    找到所有符合条件的key，并分别处理为大驼峰并替换返回新的结果
    """
    pattern = r"\b(?<!')[A-Za-z_]\w*\b"
    matchs = re.findall(pattern, expression)
    for match in matchs:
        camel_math = to_camel_case(match)
        ptn = r"\b" + match + r"\b"
        expression = re.sub(ptn, camel_math, expression, count=1, flags=0)
    return expression


def get_radmon_str(
    prefix: str = "",
    length: int = 10,
    characters: str = string.ascii_letters + string.digits,
) -> str:
    """生成随机字符串

    Args:
        prefix (str, optional): 要获取的字符串前缀. Defaults to "".
        length (int, optional): 要获取的字符串长度，包括前缀. Defaults to 10.
        characters (str, optional): 随机字符串列表. Defaults to a-zA-Z0-9.

    Returns:
        str: 生成的随机字符串
    """
    prefix_len = len(prefix)
    if prefix_len >= length:
        raise ValueError(
            f'The length of prefix "{prefix}" must be less than length [{length}].'
        )

    random_string = "".join(random.choices(characters, k=length - prefix_len))
    return prefix + random_string


def write_properties_file(filename: str, properties: dict):
    """
    将properties写入文件
    """
    with open(filename, "w") as f:
        for key, value in properties.items():
            f.write(f"{key}={value}\n")


def download_and_get_md5(url):
    """
    下载 URL 指向的文件并计算其 MD5 值。

    参数:
    url (str): 文件下载链接

    返回:
    str: 文件的 MD5 值
    """
    logger.info(f"Downloading file from {url}")
    # 获取文件名
    parsed_url = urlparse(url)
    file_name = parsed_url.path.split("/")[-1]

    # 下载文件
    response = requests.get(url, stream=True, timeout=600)
    logger.info("File downloaded successfully")
    logger.info("Calculating MD5 hash...")
    # 计算 MD5 值
    md5_hash = hashlib.md5()
    for chunk in response.iter_content(chunk_size=1024):
        if chunk:
            md5_hash.update(chunk)
    logger.info("MD5 hash calculated successfully")
    logger.info(f"MD5 hash: {md5_hash.hexdigest()}")
    logger.info(f"File name: {file_name}")
    return file_name, md5_hash.hexdigest()


def json_list_to_tuple_list(json_list: list) -> list:
    """将json列表转换为元组列表"""
    tuple_list = []
    for item in json_list:
        tuple_list.append(tuple(item.values()))
    return tuple_list
