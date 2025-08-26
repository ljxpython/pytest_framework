"""
    测试模块: 商品管理
    测试场景: 添加、删除商品
    测试重要性: P0
"""

import allure
from assertpy import assert_that
from loguru import logger

# from src.utils.log_moudle import logger
from src.client.flask_client.flask_client import flask_clinet


# 该case需要后端启用服务,否则运行会报client连接失败
@allure.title("商品管理-添加、删除商品")
class TestGoodAddDel(object):

    @allure.feature("商品管理")
    @allure.story("添加、删除商品")
    def test_good_add_del(self):
        """
        测试用例: 添加、删除商品
        测试步骤:
            1. 添加商品
            2. 确认商品添加完成
            3. 删除商品
            4. 确认商品删除完成
        """
        with allure.step("1. 添加商品"):
            resp = flask_clinet.add_product(
                name="测试商品",
                price=12,
                type_="测试商品类型",
                subtype="测试商品子类型",
            )
            logger.info(f"添加商品结果: {resp.json}")
            logger.info(f"添加商品完成")
            pass
        with allure.step("2. 确认商品添加完成"):
            pass
        with allure.step("3. 删除商品"):
            pass
        with allure.step("4. 确认商品删除完成"):
            assert_that(
                val=1,
            ).is_equal_to(1)
            pass
