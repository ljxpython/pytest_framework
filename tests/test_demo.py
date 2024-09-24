# from conf.config import settings
from test_lib.utils.log_moudle import logger


def test_demo():
    logger.info("测试demo")
    # logger.debug("测试debug")
    # logger.error("测试error")
    # logger.warning("测试warning")
    # logger.critical("测试critical")
    assert 1 == 1
