from flask import Blueprint
from flask_restful import Api
from services.news import article


news_bp = Blueprint('news', __name__)



news_api = Api(news_bp)

news_api.add_resource(article.ArticleResource, '/article', endpoint='article')
news_api.add_resource(article.ArticleResource, '/article2', endpoint='article2')
news_api.add_resource(article.ArticleResource, '/article3', endpoint='article3')
news_api.add_resource(article.ArticleResource, '/article4', endpoint='article4')

