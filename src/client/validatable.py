'''

对响应的信息进行断言


'''


import json

import jmespath
from assertpy import assert_that
from requests import Response,Request
from src.utils.log_moudle import logger


"""
用下面的方式进行断言,支持链式调用


对于相关第三方库的使用方法，可以根据需求，查看相关的文档：
 - https://github.com/hamcrest/PyHamcrest
 - https://github.com/jmespath/jmespath.py
 下面进行一些简要的使用方式
 1. 对于hamcrest，我们一般用到如下的操作:
    二者是否相等：equal_to
    数字的大于等于小于：greater_than,greater_than_or_equal_to,less_than,less_than_or_equal_to
    字符串是否包含：contains_string
    assert_that("aaaaa",has_length(5))  ## 匹配其字符串的长度是不是5
    assert_that(None,none()) ## 匹配是不是空值
    # assert_that(1,not_none())  ## 匹配空
    assert_that(1.5,close_to(1,0.5))  ## 1.6就不行
    assert_that(3,greater_than(2.9))
    assert_that(3,greater_than_or_equal_to(3))
    assert_that(["nihao"],contains("nihao"))
    assert_that("nihaoa",contains_string("nihao"))
 2. 对于jmespath,我们要掌握其简单的语法：
    字典的下一级 .xxxx
    列表的元素  [:]
    下一级列表中，包含什么的字段 [*].xxx
    跳过中间参数 a.*.b ->跳过ab之间的参数，找b里面的数据
    *.xxxx 查找字典中xxx的值，返回一个列表 e.g:*.success_task_num

"""
class Validatable(object):
    def __init__(self, response: Response):
      self.response = response
      self.request = response.request
      self.json = response.json()
      self.status_code = response.status_code
      self.headers = response.headers
      self.url = response.url
      self.body = response.text
      self.request_body = self.request.body
      self.request_headers = self.request.headers
      self.request_method = self.request.method
      self.request_path = self.request.path_url
      self.data = self.json.get("data") if self.json else None

    def search(self, expression: str = None, data: dict = None, *args, **kwargs):
      """
      expression: 匹配表达式,
      data：匹配的数据,
      options=None
      学习文档：
          - https://github.com/jmespath/jmespath.py
          - https://jmespath.org/tutorial.html
      """
      return jmespath.search(expression, data, *args, **kwargs)

    def assert_status_code(self, expected :int= 200, reason: str = "HTTP Status check"):
      assert_that(self.status_code, description=reason).is_equal_to(expected)
      return self

    def get_data_result_expression(self, expression: str = None):
      """
      我们会在result里面找一些我们想要的值，对应这部分我们进行封装，只需要暴露出expression这个参数即可
      """
      return jmespath.search(expression=expression, data=self.data)




