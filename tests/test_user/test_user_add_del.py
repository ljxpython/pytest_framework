'''

    测试模块: 用户模块
    测试场景: 添加、删除用户
    测试重要性: P0

'''

from assertpy import assert_that
import allure
import time

from src.utils.log_moudle import logger
from src.client.flask_client.flask_client import flask_clinet

class TestUserAddDel(object):
    @allure.feature("用户管理")
    @allure.story("添加、删除用户")
    def test_user_add_del(self):
        '''
            测试用例: 添加、删除用户
            测试步骤:
                1. 添加用户
                2. 删除用户
        '''
        # 1. 添加用户
        with allure.step("添加用户"):
            logger.info("添加用户")
            user_name = "test_user" + str(int(time.time()))
            user_password = "123456"
            user_email = "test_user" + str(int(time.time())) + "@test.com"
            user = flask_clinet.register_user(user_name, user_password, user_email)
            assert_that(user['code']).is_equal_to(200)
            assert_that(user['data']['id']).is_not_none()
            assert_that(user['data']['username']).is_equal_to(user_name)
        with allure.step("删除用户"):
            logger.info("删除用户")
            user_id = user['data']['id']
            user = flask_clinet.delete_user(user_id)
            assert_that(user['code']).is_equal_to(200)
