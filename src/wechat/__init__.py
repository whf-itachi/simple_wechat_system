from redis import StrictRedis
from flask import Flask
from flask_session import Session
from .config import config


# 数据库
redis_store = None


def create_app():
    """通过传入不同的配置名字，初始化其对应配置的应用实例"""
    app = Flask(__name__)

    # 配置
    app.config.from_object(config)
    # 配置redis
    global redis_store
    redis_store = StrictRedis(host=config.REDIS_HOST, port=config.REDIS_PORT)
    # 设置session保存位置
    Session(app)

    # 注册蓝图
    from .index import index_blu

    return app
