from datetime import datetime, timedelta
from flask_restful import Resource
from flask import current_app, request, abort, g
from commen.utils.jwt_auth import JWTEncodeDecodeToolHandler




class AuthorizationResource(Resource):
    """
    # 登录/刷新token
    post: 登录认证，返回token、 refresh_token
    put: 刷新access token, 不返回refresh_token(前端不变)，只返回access token，
    """

    def _generate_tokens(self, user_id, refresh=True):
        """
        生成access token，refresh_token
        :param user_id: the id of authenticated user
        :param refresh: whether refresh the access token
        :return: access token and refresh token by default, only access token when refresh is False.
        """

        # 生成 access token
        expiry = datetime.utcnow() + timedelta(hours=current_app.config['JWT_EXPIRY_HOURS'])
        access_token = JWTEncodeDecodeToolHandler().generate_jwt({'user_id': user_id}, expiry)

        # 是否生成refresh_token
        if refresh:
            # 默认登录接口，需要生成refresh token，也表示refresh token过期
            exipry = datetime.utcnow() + timedelta(days=current_app.config['JWT_REFRESH_DAYS'])
            refresh_token = JWTEncodeDecodeToolHandler().generate_jwt({'user_id': user_id, 'is_refresh': True}, exipry)      # payload增加is_refresh表示这是refresh token
        else:
            # refresh_token无需改变
            refresh_token = None

        return access_token, refresh_token


    def post(self):
        """
        登录，获取Token
        :return: access Token and refresh Token
        """

        # 校验
        # json_parser = reqparse.RequestParser()
        # json_parser.add_argument('username', type=str, location='json', required=True)
        # json_parser.add_argument('password', type=str, location='json', required=True)
        # args = json_parser.parse_args()
        # username = args['username']
        # password = args['password']

        # 取数据
        form_data = request.form
        username = form_data['username']
        password = form_data['password']

        # 基本认证
        # user = User.query.filter_by(username=username, password=password).first()
        # 模拟数据库比对用户名密码，返回user
        if not (username == 'huang' and password == '123456'):
            abort(401)

        user_id = 524
        token, refresh_token = self._generate_tokens(user_id=user_id)

        return {'access_token': token, 'refresh_token': refresh_token}, 200

    def put(self):
        """
        刷新 access token  请求头中: Authorization传refresh token，为 Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo1MjQsImV4cCI6MTY1MzA0NTc2NH0.D8BgUtK5A0uGttC98WNvGCRoyQ5J8Y9awy_hmjy65aY
        :return:  获取access_token
        """
        if g.user_id is not None and g.is_refresh is True:    # 说明refresh token有效，则刷新access token
            token, fresh_token = self._generate_tokens(user_id='user_id', refresh=False)
            return {'token': token}
        else:
            return {'msg': 'Invalid refresh token'}, 403



