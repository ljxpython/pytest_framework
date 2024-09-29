"""
参考文献：
https://blog.csdn.net/u011250186/article/details/103972471
这篇文章的教程已经很全面了
我只是在这个基础上进行了二次封装
"""

import datetime

"""
        在这里，我们首先统一一下时间格式,有利于后期我们对时间的一些处理
        当前的时间
        返回当前时间的一个字符串
        对一个特定的时间字符串处理，转化为datetime格式
        对时间的加减处理
        那么，时间的格式如下：
        '%Y.%m.%d.%H.%M.%S'
        下面主要用到的函数列举：
        datetime.datetime.now()
        datetime.datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
        datetime.date.today()
        datetime.datetime.strptime(string,"%Y.%m.%d.%H.%M.%S")
"""


class DatetimeSlove(object):
    def __init__(self):
        pass

    def now(self):
        """
        获取当前的时间
        :return:
        """
        return datetime.datetime.now()

    def str_now(self, separate: str = "."):
        """
        返回一个字符串类型的时间
        :return:
        """
        return datetime.datetime.now().strftime(
            f"%Y{separate}%m{separate}%d{separate}%H{separate}%M{separate}%S"
        )  ## 等价于datetime.datetime.now().__format__('%Y.%m.%d.%H.%M.%S')

    def today(self):
        """
        获取当天的时间
        :return:
        """
        return datetime.date.today()

    def str_today(self):
        """
        这个是返回一个年月日的字符串
        :return:
        """
        return datetime.date.today().strftime("%Y.%m.%d")

    def str_seconde(self):
        """
        这个是返回一个年月日的字符串
        :return:
        """
        return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

    def str_to_date(self, string):
        """
        将字符串格式的，转化为时间格式进行处理
        :param string:
        :return:
        """
        return datetime.datetime.strptime(string, "%Y.%m.%d.%H.%M.%S")

    def strdata_interval(self, new_time, old_time):
        """
        该函数实现，将两个字符串格式的时间，先转化成时间格式，在进行相减，求出时间差
        :param new_time:
        :param old_time:
        :return:
        """
        return self.subtime(self.str_to_date(new_time), self.str_to_date(old_time))

    def subtime(self, a, b):
        """
        两个日期相减
        :param a:
        :param b:
        :return:
        """
        return a.__sub__(b)


datatime_sovle = DatetimeSlove()

if __name__ == "__main__":
    d = DatetimeSlove()
    # print(d.now().isoformat())
    print(d.str_now())
    print(d.str_today())
    print(d.str_to_date("2021.08.19.20.57.55"))
    print(datatime_sovle.str_seconde())
    print(d.str_now(separate="_"))
