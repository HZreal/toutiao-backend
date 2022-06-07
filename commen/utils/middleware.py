from flask import request, g
from commen.utils.jwt_auth import JWTEncodeDecodeToolHandler


def jwt_auth_middleware():
    """
    请求钩子，认证中间件
    :return:
    """
    # 获取请求头中的token
    # Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzb21lIjoicGF5bG9hZCJ9.4twFt5NiznN84AWoo1d7KO1T_yoc0Z6XOpOVswacPZg

    # 定义默认值，避免其他地方从g中取值报错；要么函数体不论if、else,最终必有定义这两个数据
    g.user_id = None
    g.is_refresh = False

    token = request.headers.get('Authorization')
    if token is not None and token.startswith('Bearer '):
        # 取token进行验证
        payload = JWTEncodeDecodeToolHandler().verify_jwt(token[7:])

        if payload is not None:
            g.user_id = payload.get('user_id')
            g.is_refresh = payload.get('is_refresh', False)   # 若解析的是refresh_token, 则可以得到is_refresh=True