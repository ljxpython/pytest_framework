"""
这个模块将常量固定
框架项目的顶层目录
一定要注意，所有功能最好不好耦合，各个模块单独运行，有利于系统的良好运行
只有该模块，对相关环境的路径进行明确，与其他模块进行必要的联系
"""

import os
from datetime import timedelta
from pathlib import Path

# dirname(path) 是返回path的父路径
testpath = Path(__file__).absolute()

script_dir = testpath.parent.parent.parent
## 调试模式
base_dir = testpath.parent.parent
# ## 线上版本
# base_dir = os.getcwd()


conf_dir = os.path.join(base_dir, "conf")
settings_yaml = os.path.join(conf_dir, "settings.yaml")
common_dir = os.path.join(base_dir, "common")
data_dir = os.path.join(base_dir, "data")
demo_dir = os.path.join(base_dir, "demo")
logs_dir = os.path.join(base_dir, "logs")
output_dir = os.path.join(base_dir, "output")


class Config:
    """
    参数的另一种用法,可以存放一些线上线下开发环境相关的参数
    调用方法:
        conf = config_map[settings.env]
        conf.参数名
    """

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # flask-session配置 使用随机的字符串
    SECRET_KEY = "ljx-tests-palnt-srv"
    # flask-session配置
    SESSION_TYPE = "redis"
    SESSION_USE_SIGNER = True  # 对cookie中session_id进行隐藏处理 加密混淆
    PERMANENT_SESSION_LIFETIME = 200  # session数据的有效期，单位秒
    # JWT配置秘钥
    JWT_SECRET_KEY = "ljx-tests-palnt-srv"  # 加密
    # JWT配置过期时间
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=6)  # 1小时
    UPLOAD_FOLDER = "./logs"
    ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}
    MAX_CONTENT_PATH = 16 * 1024 * 1024  # 限制上传文件大小为16M


# 开发环境
class DevelopmentConfig(Config):
    """开发模式的配置信息"""


# 线上环境
class ProductionConfig(Config):
    """生产环境配置信息"""


config_map = {"develop": DevelopmentConfig, "product": ProductionConfig}


if __name__ == "__main__":
    print(os.path.abspath(""))
    print(base_dir)
