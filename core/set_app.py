from flask import Flask
from commen.utils.middleware import jwt_auth_middleware
from services.news import news_bp
from services.user import user_bp


def create_flask_app(config):
    """
    创建flask app，从对象读取基本配置
    :param config:
    :return:
    """
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def declare_blueprint(app: Flask):
    """
    注册蓝图
    :param app:
    :return:
    """
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(news_bp, url_prefix='/news')
    # app.register_blueprint(notice_bp, url_prefix='/notice')


def create_app(config):
    """
    创建flask app，设置数据库、钩子、日志等相关
    :param config:
    :return:
    """
    app = create_flask_app(config)

    # 配置日志

    # 连接mysql
    from db.mysql import db
    db.init_app(app)

    # 配置redis
    # from redis.sentinel import Sentinel
    # _sentinel = Sentinel(app.config['REDIS_SENTINELS'])
    # app.redis_master = _sentinel.master_for('')
    # app.redis_slave = _sentinel.slave_for('REDIS_SENTINEL_SERVER_NAME')
    # from rediscluster import RedisCluster
    # app.redis_cluster = RedisCluster(startup_nodes=app.config[''])
    from redis import Redis
    app.redis_client = Redis(host='127.0.0.1', port=6379, db=0, password='root123456')

    # 添加请求钩子
    app.before_request(jwt_auth_middleware)

    # 注册蓝图
    declare_blueprint(app)

    return app
