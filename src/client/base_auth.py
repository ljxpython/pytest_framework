'''

对于需要进行鉴权的request,在如下进行鉴权

下面只是一个自己的例子,应该根据自己服务的一个鉴权标准进行二次封装
'''

from requests.auth import AuthBase

class BaseAuth(AuthBase):
    # def __init__(self, access_key, secret_key):
    #     self.access_key = access_key
    #     self.secret_key = secret_key

    def __init__(self):
        pass

    def __call__(self, r):
        # r.headers['AccessKey'] = self.access_key
        # r.headers['SecretKey'] = self.secret_key
        return r