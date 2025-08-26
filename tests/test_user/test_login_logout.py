"""
    测试模块: 用户模块
    测试场景: 用户的登录登出
    测试重要性: P0
"""

import allure
from assertpy import assert_that

from src.client.flask_client.flask_client import flask_clinet
from src.utils.log_moudle import logger

# 该case需要后端启用服务,否则运行会报client连接失败


class TestLoginLogout(object):
    @allure.feature("用户管理")
    @allure.story("用户登录登出")
    def test_login_logout(self):
        """
        测试用例: 用户登录登出
        测试步骤:
            1. 用户登录
            2. 用户登出
        """
        with allure.step("用户登录"):
            login_resp = flask_clinet.login()
            assert_that(
                login_resp.status_code, description=f"status_code not right"
            ).is_equal_to(200)
            logger.info(f"login_resp:{login_resp.json}")
        with allure.step("用户登出"):
            logout_resp = flask_clinet.logout()
            assert_that(
                logout_resp.status_code, description=f"status_code not right"
            ).is_equal_to(200)
