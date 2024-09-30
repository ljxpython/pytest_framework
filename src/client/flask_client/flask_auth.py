

from requests.auth import AuthBase
from src.utils.log_moudle import logger

class FlaskAuth(AuthBase):
    def __init__(self, jwt_token):
        self.jwt_token = jwt_token

    def __call__(self, r):
        r.headers['Authorization'] = f'Bearer {self.jwt_token}'
        return r