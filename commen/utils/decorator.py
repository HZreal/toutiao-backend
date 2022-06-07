import functools
from flask import g


def login_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if g.user_id is not None and g.is_refresh == False:       # 认证通过且是一个普通access token，而不是refresh token
            return func(*args, **kwargs)
        else:
            # abort(401)
            return {'message': 'Invalid token'}, 401

    return wrapper