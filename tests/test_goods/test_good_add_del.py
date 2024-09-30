'''
    测试模块: 商品管理
    测试场景: 添加、删除商品
    测试重要性: P0
'''

from assertpy import assert_that
import allure

from src.utils.log_moudle import logger
from src.client.flask_client.flask_client import flask_clinet



class TestGoodAddDel(object):

    @allure.feature("商品管理")
    @allure.story("添加、删除商品")
    def test_good_add_del(self):
        '''
        测试用例: 添加、删除商品
        测试步骤:
            1. 添加商品
            2. 确认商品添加完成
            3. 删除商品
            4. 确认商品删除完成
        '''
        with allure.step("1. 添加商品"):
            pass
        with allure.step("2. 确认商品添加完成"):
            pass
        with allure.step("3. 删除商品"):
            pass
        with allure.step("4. 确认商品删除完成"):
            pass


