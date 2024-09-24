import logging
import os
import sys
from pathlib import Path

import pytest
from filelock import FileLock

print(os.getcwd())
# 打印出项目的读取路径
print(sys.path)

# from conf.config import settings
# print(settings.DB)
# from test_lib.utils import util
# from test_lib.utils.log_moudle import logger
#
# # 设置 faker 日志级别为 ERROR，减少不必要的 debug 信息输出
# logging.getLogger("faker").setLevel(logging.ERROR)
#
#
# # loguru 日志可以被 allure 记录 https://github.com/Delgan/loguru/issues/751#issuecomment-1320935865
# class PropagateHandler(logging.Handler):
#     def emit(self, record):
#         logger = logging.getLogger(record.name)
#         if logger.isEnabledFor(record.levelno):
#             logger.handle(record)
#
#
# @pytest.fixture(autouse=True, scope="session")
# def propagate_loguru():
#     handler_id = logger.add(PropagateHandler(), format="{message}")
#     yield
#     logger.remove(handler_id)
#
#
# @pytest.fixture(scope="session", autouse=True)
# def faker_session_locale():
#     """set faker fixture locale
#     https://faker.readthedocs.io/en/master/pytest-fixtures.html
#     """
#     return ["zh_CN", "en_US"]
#
#
# @pytest.fixture(scope="function")
# def faker_seed():
#     """
#     用例方法中引入faker_seed后，每次faker生成新的随机值，
#     不引入则随机值保持不变
#     """
#     return None
