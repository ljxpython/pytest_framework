from datetime import date, datetime

from peewee import *
from playhouse.mysql_ext import JSONField
from playhouse.pool import PooledMySQLDatabase
from playhouse.shortcuts import ReconnectMixin

from conf.config import settings
from src.utils.log_moudle import logger

dbconfig = settings.DB


class ReconnectMySQLDatabase(ReconnectMixin,PooledMySQLDatabase):
    pass


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name="添加时间")
    is_deleted = BooleanField(default=False, verbose_name="是否删除")
    update_time = DateTimeField(verbose_name="更新时间", default=datetime.now)

    def save(self, *args, **kwargs):
        # 判断这是一个新添加的数据还是更新的数据
        if self._pk is not None:
            # 这是一个新数据
            self.update_time = datetime.now()
        return super().save(*args, **kwargs)

    @classmethod
    def delete(cls, permanently=False):  # permanently表示是否永久删除
        if permanently:
            return super().delete()
        else:
            return super().update(is_deleted=True)

    def delete_instance(
        self, permanently=False, recursive=False, delete_nullable=False
    ):
        if permanently:
            return self.delete(permanently).where(self._pk_expr()).execute()
        else:
            self.is_deleted = True
            self.save()

    @classmethod
    def select(cls, *fields):
        return super().select(*fields).where(cls.is_deleted == False)

    class Meta:
        database = ReconnectMySQLDatabase(
            dbconfig.database,
            host=dbconfig.host,
            port=dbconfig.port,
            user=dbconfig.user,
            password=dbconfig.password,
        )


class Person(BaseModel):
    name = CharField()
    birthday = DateField()
    is_relative = BooleanField()
    test_cha = CharField()


database = ReconnectMySQLDatabase(
    dbconfig.database,
    host=dbconfig.host,
    port=dbconfig.port,
    user=dbconfig.user,
    password=dbconfig.password,
)

# 实例化migrate对象
# mgrt = SqliteMigrator(database)

if __name__ == "__main__":
    # 创建表
    # p_info = Person.create_table()
    # logger.info(p_info)
    # 创建表也可以这样, 可以创建多个
    # database.create_tables([Person])
    # p = Person(name='waws520', birthday=date(1990, 12, 20), is_relative=True)
    # logger.info( p.save())
    # p = Person(name="lasd", birthday=date(1990, 12, 20), is_relative=True, test_cha="1")
    # p.save()
    # 查询

    logger.info(Person.get(Person.name == "lasd").birthday)
    res = Person.select().where(Person.name == "lasd").dicts()

    logger.info(res)
    logger.info(Person.select().where(Person.name == "lasd"))
    logger.info(list(res))
    # for p in res:
    #     logger.info(p)

    # p = Person.select().where(Person.name == 'waws520').get()
    # p_id = Person.insert({
    #     'name': 'liuchungui'
    # }).execute()
    # logger.info(p_id)
    # NUM = 10000
    # data = [{
    #     'name': '123'
    # } for i in range(NUM)]
    #
    # with database.atomic():
    #     for i in range(0, NUM, 100):
    #         # 每次批量插入100条，分成多次插入
    #         Person.insert_many(data[i:i + 100]).execute()

    # with database.atomic() as transaction: # 事务
    #     try:
    #         p = Person(name='waws520', birthday=date(1990, 12, 20), is_relative=True)
    #         p.save()
    #         p = Person(name='waws520', birthday=date(1990, 12, 20), is_relative=True)
    #         p.save()
    #     except Exception as e:
    #         transaction.rollback()
    #         logger.error(e)
    #     else:
    #         transaction.commit()

    # with database.atomic() as transaction: # 事务
    #     p = Person(name='waws520', birthday=date(1990, 12, 20), is_relative=True)
    #     p = Person(name='waws520', birthday=date(1990, 12, 20), is_relative=True)
    #     p.save()
    # # 删除表
    # database.drop_tables([Person])
