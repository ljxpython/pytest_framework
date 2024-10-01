import os
import sys
import pytest
from datetime import datetime

from conf.config import settings
from src.utils.log_moudle import logger

import click

# pytest.main(["-s", "-v", "tests/test_goods/test_good_add_del.py","tests/test_goods/test_update_good.py"])

@click.command()
@click.option("--cases",type=str,help="指定测试用例",)
@click.option("--allure_dir", default="./reports", help="指定测试报告",)
def run_pytest(cases:str,allure_dir:str):
    logger.info(f"开始执行测试用例:{cases.split(',')},测试报告路径:{allure_dir.split(',')}")
    # 如果case和allure_dir参数为空,则抛出异常
    satrt_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    if cases == "" and allure_dir == "":
        raise Exception("请输入测试用例或测试报告路径")
    # 如果case参数为空,则执行所有测试用例
    if cases == "":
        pytest.main(["-s", "-v", "--alluredir", allure_dir])
    # 如果allure_dir参数为空,则执行指定测试用例
    elif allure_dir == "":
        pytest.main(["-s", "-v", *cases.split(',')])
    # 如果case和allure_dir参数都不为空,则执行指定测试用例并生成测试报告
    else:
        logger.info("test")
        logger.info(["-s", "-v", *cases.split(sep=" ",), "--alluredir", f"{allure_dir}/{satrt_time}-results"])
        pytest.main(["-s", "-v", *cases.split(sep=" ",), "--alluredir", f"{allure_dir}/{satrt_time}-results"])
    # 生成测试报告
    os.system(f"allure generate {allure_dir}/{satrt_time}-results -o {allure_dir}/{satrt_time}-report --clean")

if __name__ == '__main__':
    run_pytest()