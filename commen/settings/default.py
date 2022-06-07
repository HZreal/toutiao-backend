

class DefaultConfig:
    SECRET_KEY = 'TPmi4aLWRbyVq8zu9v82dWYW1'



    # Mysql
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root123456@127.0.0.1:3306/toutiao'  # URL
    SQLALCHEMY_BINDS = {
        'bj-m1': 'mysql://root:mysql@127.0.0.1:3306/toutiao',
        'bj-s1': 'mysql://root:mysql@127.0.0.1:8306/toutiao',
        'masters': ['bj-m1'],
        'slaves': ['bj-s1'],
        'default': 'bj-m1'
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # 在Flask中是否追踪数据修改
    SQLALCHEMY_ECHO = True  # 显示生成的SQL语句，可用于调试

    # Redis Sentinel
    REDIS_SENTINELS = [
        ('127.0.0.1', '26379'),
    ]
    REDIS_SENTINEL_SERVER_NAME = 'mymaster'
    # Redis Cluster
    REDIS_CLUSTER = [
        {'host': '192.168.94.131', 'port': '7000'},
        {'host': '192.168.94.131', 'port': '7001'},
        {'host': '192.168.94.131', 'port': '7002'}
    ]

    # JWT
    JWT_SECRET = ''
    JWT_EXPIRY_HOURS = 2
    JWT_REFRESH_DAYS = 14

    # QINIU OSS
    QINIU_ACCESS_KEY = ''
    QINIU_SECRET_KEY = ''
    # qiniu存储空间名
    QINIU_BUCKET_NAME = ''
    # qiniu请求域
    QINIU_DOMAIN = ''

    # RPC

    # ES

    # CORS

    # Snowflake ID Worker







