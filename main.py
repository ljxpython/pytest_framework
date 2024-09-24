import os
import sys

from test_lib.utils.log_moudle import logger
from conf.config import settings

if __name__ == "__main__":
    logger.info("hello world")
    logger.info(os.path.abspath(os.path.dirname(__file__)))
    logger.info(settings.DB )
    logger.info(sys.path)
