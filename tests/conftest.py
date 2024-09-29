import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import pytest
from filelock import FileLock

# 在conftest.py文件中，使用sys.path.append()方法将当前工作目录添加到Python的模块搜索路径中，这样就可以在测试文件中导入自定义的模块了。
sys.path.append(os.getcwd())

from conf.config import settings

print(settings.DB)
from src.utils import util
from src.utils.log_moudle import logger

# 设置 faker 日志级别为 ERROR，减少不必要的 debug 信息输出
logging.getLogger("faker").setLevel(logging.ERROR)


# loguru 日志可以被 allure 记录 https://github.com/Delgan/loguru/issues/751#issuecomment-1320935865
class PropagateHandler(logging.Handler):
    def emit(self, record):
        logger = logging.getLogger(record.name)
        if logger.isEnabledFor(record.levelno):
            logger.handle(record)


@pytest.fixture(autouse=True, scope="session")
def propagate_loguru():
    handler_id = logger.add(PropagateHandler(), format="{message}")
    yield
    logger.remove(handler_id)


@pytest.fixture(scope="session", autouse=True)
def faker_session_locale():
    """set faker fixture locale
    https://faker.readthedocs.io/en/master/pytest-fixtures.html
    """
    return ["zh_CN", "en_US"]


@pytest.fixture(scope="function")
def faker_seed():
    """
    用例方法中引入faker_seed后，每次faker生成新的随机值，
    不引入则随机值保持不变
    """
    return None


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config: pytest.Config) -> None:
    # 配置加载完毕之后执行,所有测试用例执行前执行,可记录开始测试的时间
    # config.addinivalue_line("markers", "slow: mark tests as slow to run")
    # config.addinivalue_line(
    #     "markers", "result_sender: mark tests as result_sender to run"
    # )
    print("pytest_配置")
    # from src.utils.log_moudle import logger
    # logger.info(f"time:{datetime.now()}  pytest_执行 ")


# @pytest.hookimpl(trylast=True)
def pytest_unconfigure():
    # 所有测试用例执行完毕之后执行
    # 可以记录测试结束的时间,最后对测试结果进行处理,统计出:测试的执行时间,测试通过率,失败case等等
    logger.info(f"time:{datetime.now()}  pytest_结束 ")


def pytest_collection_finish(session: pytest.Session):
    # 用例加载完成之后执行,包含了全部的用例,可以统计测试用例的条数
    print(f"用例:  {session.testscollected}条")
    print(f"用例:  {session.items}")
    # logger.info(f"用例:  {session.testscollected}条")
    # logger.info(f"用例:  {session.items}")


def pytest_runtest_logreport(report: pytest.TestReport) -> None:
    # 每个用例执行完毕之后执行,采集测试结果,可以记录哪条测试用例成功,哪个用例失败
    print(f"用例:  {report.nodeid}  {report.when}  {report.outcome}")
    # logger.info(f"用例:  {report.nodeid}  {report.when}  {report.outcome}")


def pytest_addoption(parser):
    # 命令行参数
    parser.addini(
        "send_when", help="什么时候发送测试结果,是每次都发送还是只有失败时才发送"
    )
    parser.addini("send_to", help="发送测试结果的邮箱")
