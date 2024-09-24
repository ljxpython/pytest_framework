"""
     该库比Python的原始日志好用，故使用该库进行日志的封装
     官方文档： https://github.com/Delgan/loguru

     使用说明：
     *****
     from common.log_moudle import logger

     logger.info("this is info message")
     logger.debug("this in debug infomation")
     *****

     日志存储位置
     根目录下的log目录
     其中,tests{_xxx}.log 日志中存储我们通常使用的case
          error.log 日志中记录较为关键的崩溃及失败信息，信息包括但不限于以下：调用链路的logID，错误的case名称及错误的相关原因

"""

import os
import sys

from loguru import logger

from conf.constants import base_dir

##日志存储地址
# BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_PATH = os.getcwd()
BASE_PATH = base_dir
LOG_PATH = os.path.join(BASE_PATH, "logs")
if not os.path.exists(LOG_PATH):
    os.mkdir(LOG_PATH)


##测试代码

# logger.add(os.path.join(LOG_PATH,"test_{time}.log"))
# logger.add(os.path.join(LOG_PATH,"tests.log"),rotation="1 MB",retention="10 days",encoding="utf-8")  ## 目前，我们设置成自动清除存满100MB的文件跟换到下一个文件
# logger.add(os.path.join(LOG_PATH,"tests.log"),rotation="",encoding="utf-8")
# logger.add(os.path.join(LOG_PATH,"tests.log"),rotation="",encoding="utf-8")

## 按照日志等级记录到不同文件中
# logger.add(os.path.join(LOG_PATH,"test1.log"),level="INFO",filter=lambda x: "INFO" in str(x["level"]).upper())
# logger.add(os.path.join(LOG_PATH,"test2.log"),level=["DEBUG","WARNING"],filter=lambda x: "INFO" in str(x["level"]).upper())


## 封装成类
class MyLogger(object):
    def __init__(
        self,
        log_test_path=os.path.join(LOG_PATH, "tests.log"),
        log_error_path=os.path.join(LOG_PATH, "error.log"),
        log_warn_path=os.path.join(LOG_PATH, "debug.log"),
    ):
        self.logger = logger
        # 清空所有设置
        self.logger.remove()
        # 添加控制台输出的格式,sys.stdout为输出到屏幕;关于这些配置还需要自定义请移步官网查看相关参数说明
        self.logger.add(
            sys.stdout,
            format="<green>{time:YYYY-MM-DD HH:mm:ss:sss}</green> | "  # 颜色>时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 线程名
            "<cyan>{module}</cyan>.<cyan>{function}</cyan>"  # 模块名.方法名
            ":<cyan>{line}</cyan> | "  # 行号
            "<level>{level}</level>: "  # 等级
            "<level>{message}</level>",  # 日志内容
        )
        # 输出到文件的格式,注释下面的add',则关闭日志写入
        self.logger.add(
            log_test_path,
            format="{time:YYYYMMDD HH:mm:ss:sss} - "  # 时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 线程名
            "{module}.{function}:{line} - {level} -{message}",  # 模块名.方法名:行号
            rotation="100 MB",
            retention="10 days",
            encoding="utf-8",
        )
        # self.logger.add(
        #     log_error_path,
        #     level="ERROR",
        #     format="{time:YYYYMMDD HH:mm:ss:sss} - "  # 时间
        #     "{process.name} | "  # 进程名
        #     "{thread.name} | "  # 线程名
        #     "{module}.{function}:{line} - {level} -{message}",  # 模块名.方法名:行号
        #     rotation="100 MB",
        #     retention="10 days",
        #     encoding="utf-8",
        # )
        self.logger.add(
            log_warn_path,
            level="WARNING",
            format="{time:YYYYMMDD HH:mm:ss:sss} - "  # 时间
            "{process.name} | "  # 进程名
            "{thread.name} | "  # 线程名
            "{module}.{function}:{line} - {level} -{message}",  # 模块名.方法名:行号
            rotation="100 MB",
            retention="10 days",
            encoding="utf-8",
        )

    def get_logger(self):
        return self.logger


# logger.info("hello world")
logger = MyLogger().get_logger()

if __name__ == "__main__":
    print(LOG_PATH)
    logger.info("tests info")
    logger.debug("tests debug")
    logger.warning(" error")
