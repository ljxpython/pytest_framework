from peewee import *

from src.model.modelsbase import BaseModel
from src.utils.log_moudle import logger


class AsyncTask(BaseModel):
    task_id = CharField(unique=True, null=False, max_length=32, verbose_name="任务ID")
    task_type = CharField(null=False, max_length=32, verbose_name="任务类型")
    task_status = CharField(null=False, max_length=32, verbose_name="任务状态")
    task_args = TextField(null=True, verbose_name="任务参数")
    task_result = TextField(null=True, verbose_name="任务结果")
    task_error = TextField(null=True, verbose_name="任务错误")

if __name__ == '__main__':
    # AsyncTask.create_table()
    pass