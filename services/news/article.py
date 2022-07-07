from flask_restful import Resource
from commen.utils.decorator import login_required



class ArticleResource(Resource):
    """
    用户自己的数据
    """
    method_decorators = [login_required]

    def get(self):
        """
        获取当前用户自己的数据
        """
        return ''


class ArticleResource2(Resource):
    """

    """
    pass


class ArticleResource3(Resource):
    """

    """
    pass


class ArticleResource4(Resource):
    """

    """
    pass





