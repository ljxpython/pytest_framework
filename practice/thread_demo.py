import time

# 线程池
from concurrent.futures import ThreadPoolExecutor

# 多进程
from multiprocessing import Pipe, Process
from threading import Thread
from time import sleep

from loguru import logger


def test_function(key_1: str):
    logger.info(f"test_function : {key_1} start")
    sleep(2)
    logger.info(f"test_function : {key_1} end")


if __name__ == "__main__":
    # 时间
    start_time = time.time()
    # logger.info("main start")
    # t = Thread(target=test_function,kwargs={"key_1":"value"})
    # t.start()
    # logger.info("main end")
    # t.join()
    # logger.info(f"耗时{time.time() - start_time}")
    # pool = ThreadPoolExecutor(max_workers=3)
    # pool.map(test_function,["key_1","key_2","key_3"])
    # pool.map(lambda x: test_function(x),["key_1","key_2","key_3"])
    # for i in range(10):
    #     pool.submit(test_function, f"key_{i}")
    # for i in range(10):
    #     pool.submit(test_function, {"key_1":f"value_{i}"})
    # pool.shutdown(wait=True)
    c1, c2 = Pipe()
    c1.send("hello")
    logger.info(c2.recv())
    c1.send("world")
    logger.info(c2.recv())
    c2.send("hello")
    logger.info(c1.recv())
    c2.close()
    logger.info(c1.recv())  # 因为c2已经close,所以会抛出异常raise EOFError
    logger.info(f"耗时{time.time() - start_time}")
