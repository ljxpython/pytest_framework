import os
import sys
import pytest
from pathlib import Path
from datetime import datetime

from conf.config import settings
from src.utils.log_moudle import logger
from src.model.case import CaseMoudle, CaseFunc,Project,Suite, TestResult, CaseTag,TestPlan
from src.model.modelsbase import database
from src.utils.file_operation import file_opreator

import click

# pytest.main(["-s", "-v", "tests/test_goods/test_good_add_del.py","tests/test_goods/test_update_good.py"])

@click.command()
@click.option("--cases",type=str,help="指定测试用例",)
@click.option("--allure_dir", default="./reports", help="指定测试报告",)
@click.option("--result_id",help="唯一标识,用于存储测试相关数据")
def run_pytest(cases:str,allure_dir:str,result_id:str):
    cwd_path = str(Path().cwd())
    nginx_url = settings.test.nginx_url
    # 连接数据库
    database.connect()
    result = TestResult.get(id=result_id)
    logger.info(f"开始执行测试用例:{cases.split(',')},测试报告路径:{allure_dir.split(',')}")
    # 如果case和allure_dir参数为空,则抛出异常
    if cases == "" and allure_dir == "":
        raise Exception("请输入测试用例或测试报告路径")
    # 如果case参数为空,则执行所有测试用例
    if cases == "":
        ret_code = pytest.main(["-s", "-v", "--alluredir", allure_dir])
    # 如果allure_dir参数为空,则执行指定测试用例
    elif allure_dir == "":
        ret_code = pytest.main(["-s", "-v", *cases.split(',')])
    # 如果case和allure_dir参数都不为空,则执行指定测试用例并生成测试报告
    else:
        logger.info(["-s", "-v", *cases.split(sep=" ",), "--alluredir", f"{allure_dir}/results"])
        ret_code = pytest.main(["-s", "-v", *cases.split(sep=" ",), "--alluredir", f"{allure_dir}/results"])
    if ret_code == pytest.ExitCode.OK:
        result.result = "PASS"
        result.save()
    else:
        result.result = "FAIL"
        result.save()
    # 生成测试报告
    os.system(f"allure generate {allure_dir}/results -o {allure_dir}/report --clean")
    logger.info(f"测试报告已生成,路径为:{allure_dir}/report")
    result.report_link = f"{allure_dir}/report/index.html".replace(cwd_path, nginx_url)
    result.save()
    # 打包测试相关的产物
    file_opreator.tar_packge(output_filename=f"{allure_dir}.tar.gz", source_dir=f"{allure_dir}")
    report_path = f"{allure_dir}.tar.gz".replace(cwd_path, nginx_url)
    logger.info(report_path)
    result.report_download = report_path
    result.save()
    # 路径替换,前缀为settings.test.nginx_url的路径

    # 测试完成
    result.status = 1
    result.save()
    # 如果未关闭,关闭数据库连接
    if not database.is_closed():
        database.close()
    ## TODO 这部分缺少一个对比历史趋势的allure报告优化,可以参考allure的官方文档:https://allurereport.org/docs/history-and-retries/#how-to-enable-history 留作后期优化

if __name__ == '__main__':
    run_pytest()