from flask import Flask
from commen.utils.middleware import jwt_auth_middleware
from controller.user import user_bp


def create_flask_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    return app


def create_app(config):
    # 创建flask app
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
    app.register_blueprint(user_bp, url_prefix='/user')
    # app.register_blueprint()
    # app.register_blueprint()
    # app.register_blueprint()

    return app






