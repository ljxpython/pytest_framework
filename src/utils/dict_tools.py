"""
把一个字典格式数据进行格式化美观的输出，或者把一个字符串转化为字典格式供用户使用

不太方面看的形式可能如下：
    {'name': 'tom', 'age': 18, 'people': ['tom', 'jack'], 'number': 12.3, 'isset': 'ture', 'parent': None, 'iso8601': datetime.datetime(2001, 12, 14, 21, 59, 43, 100000, tzinfo=datetime.timezone(datetime.timedelta(days=-1, seconds=68400))), 'date': datetime.date(1927, 7, 31), 'e': '123', 'f': 'true', 'str': '这是一行字符串', 'str1': '内容：    字符串', 'str2': "labor's day", 's1': '内容\\n 字符串', 's2': '内容\n 字符串', 'str3': 'this is first this is seconde this is third'}


"""

import json

from src.utils.log_moudle import logger


def dict_format(data):
    """
    首先判断是否为字符串，是字符串则先转化为字典格式
    :param data:
    :return:
    """
    if not isinstance(data, (str, dict)):
        logger.debug("data type is not we need ,please check data ~ ")
        return False
    if isinstance(data, str):
        try:
            data = json.loads(data)
        except Exception as e:
            logger.debug(f"data can not transform dict ,the error: {e}")
    try:
        data = json.dumps(data, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.debug(f"fail to transform dict, the error: {e}")
    return data
