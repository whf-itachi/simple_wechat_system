from redis import StrictRedis


class Config(object):
    """工程配置信息"""
    DEBUG = True
    # mysql数据库配置
    SQLALCHEMY_DATABASE_URI = "mysql://root:@127.0.0.1:3306/wechat"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True

    # redis配置
    REDIS_HOST = "127.0.0.1"
    REDIS_PORT = 6379

    # flask_session的配置信息
    SESSION_TYPE = 'redis'
    SESSION_USE_SIGNER = True
    SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
    PERMANENT_SESSION_LIFETIME = 86400


config = Config()
