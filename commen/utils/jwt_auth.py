from flask import current_app
import jwt

class JWTEncodeDecodeToolHandler:
    """
    封装的JWT处理类，  生成、验证token
    """
    JWT_ALGORITHM = 'HS256'

    def __init__(self, secret=None):
        self.secret = secret or current_app.config['JWT_SECRET']

    def generate_jwt(self, payload, expiry):
        """
        生成JWT token
        :param payload:
        :param expiry:     unix时间戳
        :return:
        """
        payload.update({'exp': expiry})
        return jwt.encode(payload, key=self.secret, algorithm=self.JWT_ALGORITHM)

    def verify_jwt(self, token):
        """
        验证token是否有效
        :param token:
        :return:
        """

        try:
            payload = jwt.decode(token, key=self.secret, algorithms=[self.JWT_ALGORITHM])
        # except jwt.PyJWTError:
        except Exception as e:
            print(e)
            payload = None

        return payload
