from flask import Blueprint
from flask_restful import Api
from conrtoller.user import passport, profile


user_bp = Blueprint('user', __name__)



user_api = Api(user_bp)

# 收集view
user_api.add_resource(passport.AuthorizationResource, '/authorization', endpoint='Authorization')
user_api.add_resource(profile.PhotoResource, '/profile', endpoint='profile')
user_api.add_resource(profile.CurrentUserResource, '/v1_0/user', endpoint='CurrentUser')





