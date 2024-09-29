import os
import sys

from conf.config import settings
from src.utils.log_moudle import logger

if __name__ == "__main__":
    logger.info("hello world")
    logger.info(os.path.abspath(os.path.dirname(__file__)))
    logger.info(settings.DB)
    logger.info(sys.path)
