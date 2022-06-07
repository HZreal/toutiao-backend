import random


class BaseCacheTTL(object):
    """
    缓存有效期
    为防止缓存雪崩，在设置缓存有效期时采用设置不同有效期的方案
    通过增加随机值实现
    """
    TTL = 0  # 由子类设置
    MAX_DELTA = 10 * 60  # 随机的增量上限

    @classmethod
    def get_val(cls):
        return cls.TTL + random.randrange(0, cls.MAX_DELTA)


class UserProfileCacheTTL(BaseCacheTTL):
    """
    用户资料数据缓存时间, 秒
    """
    TTL = 30 * 60