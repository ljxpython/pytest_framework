from peewee import *

from src.model.modelsbase import BaseModel, database
from src.utils.log_moudle import logger

"""
接口自动化的case表



"""


class CaseMoudle(BaseModel):
    moudle = CharField(max_length=100, null=False, verbose_name="模块名称", unique=True)
    desc = TextField(null=True, verbose_name="模块描述")


class CaseFunc(BaseModel):
    # 外键
    casemoudle = ForeignKeyField(
        CaseMoudle, verbose_name="所属模块", backref="case_func"
    )
    case_path = CharField(
        max_length=100,
        null=False,
        verbose_name="接口所在的位置,用于执行case",
        unique=True,
    )
    # case_sence 其实就是py的文件名
    case_sence = CharField(max_length=100, null=True, verbose_name="case场景")
    path_desc = TextField(null=True, verbose_name="接口描述")
    case_func = CharField(max_length=100, null=True, verbose_name="case函数名")
    case_func_desc = TextField(null=True, verbose_name="case函数描述")
    tags = CharField(max_length=100, null=True, verbose_name="标签")
    # class Meta:
    #     primary_key = CompositeKey("case_path", "case_func")


class Project(BaseModel):
    project_name = CharField(max_length=100, verbose_name="项目名称", unique=True)
    project_desc = TextField(null=True, verbose_name="项目描述")
    project_owners = CharField(verbose_name="可执行测试的人员")


class Suite(BaseModel):
    suite_name = CharField(max_length=100, verbose_name="套件名称", unique=True)
    # project_id 作为外键
    project = ForeignKeyField(
        Project, backref="suites", verbose_name="项目名称", on_delete="CASCADE"
    )
    # owners = CharField(verbose_name="可执行测试的人员")
    describe = TextField(verbose_name="套件描述")
    # 需要执行的case集
    case_ids = TextField(verbose_name="需要执行的case集")
    # case_sences,
    case_sences = TextField(verbose_name="需要执行的case场景集")
    # 测试类型
    # test_type = CharField(max_length=100, null=False, verbose_name="测试类型")
    # 测试环境 线上线下
    # test_env = CharField(max_length=100, null=False, verbose_name="测试环境")


# 测试用例 -> 测试套件 -> 测试计划 -> 测试结果+报告


# 测试计划,配置定期任务
class TestPlan(BaseModel):
    # 测试套件为外键
    suite = ForeignKeyField(Suite, verbose_name="suite_name")
    # 测试计划名称
    plan_name = CharField(
        max_length=100, null=False, verbose_name="测试计划名称", unique=True
    )
    # 定时任务
    cron = CharField(max_length=100, null=False, verbose_name="定时任务")
    # 测试环境 线上线下
    test_env = CharField(max_length=100, null=False, verbose_name="测试环境")
    # 是否开启,默认为关闭
    # is_open = BooleanField(null=False, default=False, verbose_name="是否开启")
    is_open = CharField(null=False, default="off", verbose_name="是否开启")
    # 测试计划的任务id,用于取消任务
    plan_id = CharField(max_length=100, null=True, verbose_name="任务id")


class TestResult(BaseModel):
    # 标题
    title = CharField(max_length=100, null=True, verbose_name="测试报告标题")
    # 外键 suite_name
    suite = ForeignKeyField(Suite, verbose_name="suite_name")
    # 运行的状态 0 代表运行中 1 代表流程结束
    status = IntegerField(null=True, default=0, verbose_name="运行状态")
    # 测试结果 成功,失败,部分失败
    result = CharField(max_length=100, null=True, verbose_name="测试结果")
    # 测试报告链接
    report_link = CharField(max_length=1000, null=True, verbose_name="测试报告链接")
    # 测试报告下载地址
    report_download = CharField(
        max_length=1000, null=True, verbose_name="测试报告下载地址"
    )
    # 上一次测试报告的id
    last_report_id = IntegerField(null=True, verbose_name="上一次测试报告的id")
    # result_desc = TextField(max_length=1000, null=True, verbose_name="测试结果描述")
    # 测试类型 定时 webhook 手动
    test_type = CharField(max_length=100, null=True, verbose_name="测试类型")
    # 测试环境 线上线下
    test_env = CharField(max_length=100, null=True, verbose_name="测试环境")
    # task_id
    task_id = CharField(max_length=100, null=True, verbose_name="任务id")
    # 如果有测试计划,则会有testplan_id字段
    plan_id = IntegerField(null=True, verbose_name="测试计划id")


class CaseTag(BaseModel):
    tag = CharField(max_length=100, null=False, verbose_name="标签", unique=True)


if __name__ == "__main__":
    # 删除表
    # database.drop_tables(
    #     [CaseMoudle, CaseFunc, Project, Suite, TestPlan, TestResult, CaseTag]
    # )
    # # 创建表
    database.create_tables(
        [CaseMoudle, CaseFunc, Project, Suite, TestPlan, TestResult, CaseTag]
    )

    pass
