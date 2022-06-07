# 项目Redis持久存储实现


from flask import current_app
from redis.exceptions import ConnectionError


class CountStorageBase(object):
    """
    统计数据存储父类
    """

    key = ''

    @classmethod
    def get(cls, user_id):
        """
        获取指定用户的数值
        :param user_id:
        :return:
        """
        try:
            ret = current_app.redis_master.zscore(cls.key, user_id)
        except ConnectionError as e:
            current_app.logger.error(e)
            ret = current_app.redis_slave.zscore(cls.key, user_id)

        if ret is not None:
            return int(ret)
        else:
            return 0

    @classmethod
    def incr(cls, user_id, increment=1):
        """
        给指定用户机统计数据累计
        :param user_id:
        :param increment:
        :return:
        """
        current_app.redis_master.zincrby(cls.key, user_id, increment)


class UserArticleCountStorage(CountStorageBase):
    """
    用户文章数量存储
    """
    key = 'count:user:arts'


class UserFollowingCountStorage(CountStorageBase):
    """
    用户关注数量
    """
    key = 'count:user:followings'








