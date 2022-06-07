from flask import current_app
from redis.exceptions import RedisError
import json
from sqlalchemy.orm import load_only

from model.user import User
from . import constants


class UserProfileCache(object):
    """
    用户资料信息缓存
    """

    def __init__(self, user_id):
        self.key = 'user:{}:info'.format(user_id)
        self.user_id = user_id

    def save(self):
        """
        查询数据库保存缓存记录
        :return:
        """
        r = current_app.redis_cluster
        # 查询数据库
        user = User.query.options(load_only(User.name,
                                            User.profile_photo,
                                            User.introduction,
                                            User.certificate)).filter_by(id=self.user_id).first()
        # 判断结果是否存在
        # 保存到redis中
        if user is None:
            try:
                r.setex(self.key, constants.USER_NOT_EXISTS_CACHE_TTL, -1)
            except RedisError as e:
                current_app.logger.error(e)
            return None
        else:
            cache_data = {
                'name': user.name,
                'photo': user.profile_photo,
                'intro': user.introduction,
                'certi': user.certificate
            }
            try:
                r.setex(self.key, constants.UserProfileCacheTTL.get_val(), json.dumps(cache_data))
            except RedisError as e:
                current_app.logger.error(e)
        return cache_data

    def get(self):
        """
        获取用户的缓存数据
        :return:
        """
        r = current_app.redis_cluster

        # 先查询redis
        try:
            ret = r.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        if ret is not None:
            # 如果存在记录，读取
            if ret == b'-1':
                # 判断记录值，如果为-1，表示用户不存在
                return None
                # 如果不为-1，需要json转换，返回
            else:
                return json.loads(ret)
        else:
            # 如果记录不存在，
            cache_data = self.save()
            return cache_data

    def clear(self):
        """
        清除用户缓存
        """
        try:
            current_app.redis_cluster.delete(self.key)
        except RedisError as e:
            current_app.logger.error(e)

    def exists(self):
        """
        判断用户是否存在
        """
        # 查询redis
        r = current_app.redis_cluster
        try:
            ret = r.get(self.key)
        except RedisError as e:
            current_app.logger.error(e)
            ret = None

        # 如果缓存记录存在
        if ret is not None:
            if ret == b'-1':
                # 如果缓存记录为-1 ，表示用户不存在
                return False
            else:
                # 如果缓存记录不为-1， 表示用户存在
                return True

        # 如果缓存记录不存在，查询数据库
        else:
            cache_data = self.save()
            if cache_data is not None:
                return True
            else:
                return False
