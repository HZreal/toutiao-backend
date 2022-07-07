from flask import current_app, g
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from commen.utils import parser
from commen.utils.decorator import login_required
from commen.utils.qiniu_storage import upload
from model.user import db, User
from commen.cache.user import UserProfileCache


class PhotoResource(Resource):
    """
    用户图片资料的视图处理
    """
    method_decorators = [login_required]

    def patch(self):
        """
        修改用户的资料（修改用户头像）
        请求json:
        {
            "photo": <uploadFile>
        }
        :return:
        """

        # 获取请求参数并校验
        rp = RequestParser()
        rp.add_argument('photo', type=parser.image_file, required=True, location='files')
        req = rp.parse_args()

        # 业务处理
        # 1. 图片上传到七牛
        upload_file = req.photo                    # req.photo取出了请求中的文件对象upload_file
        file_data = upload_file.read()             # 通过read方法读取文件的二进制数据
        # 返回保存的文件名
        file_name = upload(file_data)

        # 2. 保存图片的元数据(图片名称、图片路径等)到数据库
        # a. 保存完整的图片路径(包含了域名、路径、文件名)，浪费空间，因为域名路径都一样
        # b. 仅保存图片名称，将域名路径设置到配置中，可修改；如果以图片完整路径保存在数据库中，一旦更改了域名，修改数据库中url极其不方便
        User.query.filter(User.id == g.user_id).update({'profile_photo': file_name})
        db.session.commit()

        # 构建返回数据
        photo_url = current_app.config['QINIU_DOMAIN'] + file_name
        return {'photo_url': photo_url}


class CurrentUserResource(Resource):
    """
    用户自己的数据
    """
    method_decorators = [login_required]

    def get(self):
        """
        获取当前用户自己的数据
        """
        user_data = UserProfileCache(g.user_id).get()
        user_data['id'] = g.user_id
        return user_data


