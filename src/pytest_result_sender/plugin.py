from datetime import datetime

from test_lib.utils.log_moudle import logger


def pytest_configure(config):
    # 配置加载完毕之后执行,所有测试用例执行前执行
    # config.addinivalue_line("markers", "slow: mark tests as slow to run")
    config.addinivalue_line(
        "markers", "result_sender: mark tests as result_sender to run"
    )
    logger.info(f"time:{datetime.now()}  pytest_执行 ")


def pytest_unconfigure(config):
    # 所有测试用例执行完毕之后执行
    logger.info(f"time:{datetime.now()}  pytest_结束 ")
