from requests.exceptions import RequestException
from retry import retry

from conf.config import settings
from src.client.base_client import BaseClient
from src.client.flask_client.flask_auth import FlaskAuth
from src.client.flask_client.flask_validatable import FlaskValidatable
from src.utils.log_moudle import logger

config = settings.flask


class FlaskClient(BaseClient):

    def __init__(self, host, account, password, timeout=10):
        super(FlaskClient, self).__init__(host, timeout)
        self.account = account
        self.password = password
        # 根据用户名进行登录,获取jwk鉴权信息
        jwt_token = self.login().get_data_result_expression("token")
        self.session.auth = FlaskAuth(jwt_token)
        self.resp: FlaskValidatable = None

    def request(
        self,
        method,
        path,
        params=None,
        data=None,
        json=None,
        headers=None,
        auth=None,
        *args,
        **kwargs
    ):
        url = self.host + path
        resp = self.session.request(
            method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            *args,
            **kwargs
        )
        self.resp = FlaskValidatable(resp)
        return self.resp

    def get(
        self,
        path,
        params=None,
        data=None,
        json=None,
        headers=None,
        auth=None,
        *args,
        **kwargs
    ):
        return self.request(
            "GET",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            *args,
            **kwargs
        )

    def post(
        self,
        path,
        params=None,
        data=None,
        json=None,
        headers=None,
        auth=None,
        *args,
        **kwargs
    ):
        return self.request(
            "POST",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            *args,
            **kwargs
        )

    def put(
        self,
        path,
        params=None,
        data=None,
        json=None,
        headers=None,
        auth=None,
        *args,
        **kwargs
    ):
        return self.request(
            "PUT",
            path,
            params=params,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            *args,
            **kwargs
        )

    # send_requests函数,增加重试功能,当状态码!=200时,重试3次
    @retry(tries=3, delay=10, exceptions=(RequestException))
    def send_requests(
        self,
        method,
        path,
        params=None,
        data=None,
        json=None,
        headers=None,
        auth=None,
        *args,
        **kwargs
    ):
        url = self.host + path
        return self.request(
            method,
            url=url,
            params=params,
            data=data,
            json=json,
            headers=headers,
            auth=auth,
            *args,
            **kwargs
        )
        # return self.session.request(method, url=url, params=params, data=data, json=json, headers=headers,auth=auth ,*args,**kwargs)

    # 登录接口
    def login(self, username: str = None, password: str = None):
        if not username:
            username = self.account
        if not password:
            password = self.password
        return self.post(
            "/api/user/login", json={"username": username, "password": password}
        )

    # 查询当前用户信息接口
    def get_current_user(self):
        return self.get("/api/user/currentUser")

    # 注册用户
    def register_user(
        self,
        username: str,
        password: str,
        email: str,
        access: int = 1,
        other_info: dict = None,
        **kwargs
    ):
        body = {
            "username": username,
            "password": password,
            "email": email,
            "access": access,
        }
        if other_info:
            body.update(other_info)
        return self.post("/api/user/register", json=body, **kwargs)

    # 修改用户信息
    def update_user(
        self,
        username: str,
        password: str,
        email: str = None,
        access: int = 1,
        other_info: dict = None,
        **kwargs
    ):
        body = {
            "username": username,
            "password": password,
            "email": email,
            "access": access,
        }
        if other_info:
            body.update(other_info)
        return self.post("/api/user/update", json=body, **kwargs)

    # 退出登录
    def logout(self):
        return self.send_requests("POST", "/api/user/logout")

    # 添加商品信息
    def add_product(
        self,
        name: str,
        price: float,
        type_: str,
        subtype: str,
        description: str = None,
        status: int = 2,
        other_info: dict = None,
        **kwargs
    ):
        body = {
            "name": name,
            "price": price,
            "description": description,
            "status": status,
            "type": type_,
            "subtype": subtype,
        }
        if other_info:
            body.update(other_info)
        return self.send_requests("POST", "/api/product/add", json=body, **kwargs)

    # 修改商品信息
    def update_product(
        self,
        product_id: int,
        name: str,
        price: float,
        type_: str,
        subtype: str,
        description: str = None,
        status: int = 2,
        other_info: dict = None,
        **kwargs
    ):
        body = {
            "name": name,
            "price": price,
            "description": description,
            "status": status,
            "type": type_,
            "subtype": subtype,
        }
        if other_info:
            body.update(other_info)
        return self.send_requests("POST", "/api/product/update", json=body, **kwargs)

    # 删除商品信息
    def delete_product(self, product_id: int, **kwargs):
        return self.send_requests(
            "POST", "/api/product/delete", json={"product_id": product_id}, **kwargs
        )

    # 根据条件查询查询商品信息
    def search_product(
        self,
        name: str = None,
        type_: str = None,
        subtype: str = None,
        status: int = None,
        **kwargs
    ):
        return self.send_requests(
            "POST",
            "/api/product/search",
            json={"name": name, "type": type_, "subtype": subtype, "status": status},
            **kwargs
        )


flask_clinet = FlaskClient(
    host=config.HOST, account=config.ACCOUNT, password=config.PASSWORD
)

if __name__ == "__main__":
    flask_clinet.login()
    resp = flask_clinet.get_current_user()
    logger.info(resp.json)
    flask_clinet.logout()
