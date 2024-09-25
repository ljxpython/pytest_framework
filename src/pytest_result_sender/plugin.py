from datetime import datetime

import pytest

# from src.utils.log_moudle import logger


@pytest.hookimpl(tryfirst=True)
def pytest_configure():
    # 配置加载完毕之后执行,所有测试用例执行前执行
    # config.addinivalue_line("markers", "slow: mark tests as slow to run")
    # config.addinivalue_line(
    #     "markers", "result_sender: mark tests as result_sender to run"
    # )
    # logger.info(f"time:{datetime.now()}  pytest_执行 ")
    print("pytest_执行")


@pytest.hookimpl(trylast=True)
def pytest_unconfigure():
    # 所有测试用例执行完毕之后执行
    # logger.info(f"time:{datetime.now()}  pytest_结束 ")
    print("pytest_结束")
