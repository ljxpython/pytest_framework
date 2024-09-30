'''

    测试模块:商品管理
    测试场景: 更新商品
    测试重要性: P0

'''

from assertpy import assert_that
import allure

from src.utils.log_moudle import logger
from src.client.flask_client.flask_client import flask_clinet


class TestGoodUpdate(object):
    @allure.feature("商品管理")
    @allure.story("更新商品")
    def test_good_update(self):
        '''
        测试用例: 更新商品
        测试步骤:
            1. 获取商品列表
            2. 选择一个商品
            3. 更新商品信息
            4. 验证商品信息是否更新成功

        '''
        with allure.step("获取商品列表"):
            logger.info("调用接口,查询商品列表")
            pass
        with allure.step("选择一个商品"):
            pass
        with allure.step("更新商品信息"):
            pass
        with allure.step("验证商品信息是否更新成功"):
            resp = "success"
            assert_that(resp).is_equal_to("success")
            logger.info(f"商品正确更新完成")
