'''

http 接口封装

'''


from requests import Session


class BaseClient(object):
    def __init__(self, host, timeout=10):
        self.host = host
        self.timeout = timeout
        self.session = Session()

    def request(self, method, path, params=None, data=None, json=None, headers=None,*args,**kwargs):
        url = self.host + path
        response = self.session.request(method, url, params=params, data=data, json=json, headers=headers, timeout=self.timeout,*args, **kwargs)
        return response

    def get(self, path, params=None, data=None, json=None, headers=None,*args,**kwargs):
        return self.request('GET', path, params=params, data=data, json=json, headers=headers,*args, **kwargs)

    def post(self, path, params=None, data=None, json=None, headers=None,*args,**kwargs):
        return self.request('POST', path, params=params, data=data, json=json, headers=headers,*args, **kwargs)

    def put(self, path, params=None, data=None, json=None, headers=None,*args,**kwargs):
        return self.request('PUT', path, params=params, data=data, json=json, headers=headers,*args, **kwargs)




