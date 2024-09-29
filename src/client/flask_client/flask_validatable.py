'''


继承Vidaliable类，并实现validate方法
    如下的vilidatable 都与业务相结合

'''

from src.client.validatable import Validatable


class FlaskValidatable(Validatable):

    def __init__(self, response):
        super().__init__(response)
