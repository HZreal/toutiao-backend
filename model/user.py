from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from db.mysql import db


class User(db.Model):
    """User模型类"""
    __tablename__ = 'user_basic'

    class STATUS:    # 枚举
        DISABLE = 0
        ENABLE = 1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    mobile = db.Column(db.String, doc='手机号')
    password = db.Column(db.String, doc='密码')
    name = db.Column('user_name', db.String, doc='昵称')
    profile_photo = db.Column(db.String, doc='头像')
    last_login = db.Column(db.DateTime, doc='最后登录时间')
    is_media = db.Column(db.Boolean, default=False, doc='是否是自媒体')
    is_verified = db.Column(db.Boolean, default=False, doc='是否实名认证')
    introduction = db.Column(db.String, doc='简介')
    certificate = db.Column(db.String, doc='认证')
    article_count = db.Column(db.Integer, default=0, doc='发帖数')
    following_count = db.Column(db.Integer, default=0, doc='关注的人数')
    fans_count = db.Column(db.Integer, default=0, doc='被关注的人数（粉丝数）')
    like_count = db.Column(db.Integer, default=0, doc='累计点赞人数')
    read_count = db.Column(db.Integer, default=0, doc='累计阅读人数')

    account = db.Column(db.String, doc='账号')
    email = db.Column(db.String, doc='邮箱')
    status = db.Column(db.Integer, default=STATUS.ENABLE, doc='状态，是否可用')

    # 额外声明的类属性，不映射数据库的字段；默认是惰性执行
    # 方式一、主模型类中声明关联表的连接属性，通过此属性查询获取从表信息(默认是对象列表)，此方式需要从模型类对应字段设置外键约束
    # profile = db.relationship('UserProfile', uselist=False)           # uselist表示主表调用profile返回时是否以列表返回，这里是一对一关系，返回从表对象即可，故不需要以列表返回
    # followings = db.relationship('Relation')                          # 多对多，以列表形式返回(默认)

    # 方式二、仅在主模型类中声明关联字段及关联条件，此时从模型类对应字段不需要设置外键约束
    profile = db.relationship('UserProfile', primaryjoin='User.id==foreign(UserProfile.id)', uselist=False)
    followings = db.relationship('Relation', primaryjoin='User.id==foreign(Relation.user_id)')

class UserProfile(db.Model):
    """
    用户资料表
    """
    __tablename__ = 'user_profile'

    class GENDER:
        MALE = 0
        FEMALE = 1

    id = db.Column('user_id', db.Integer, primary_key=True, doc='用户ID')
    # id = db.Column('user_id', db.Integer, db.ForeignKey('user_basic.user_id'), primary_key=True, doc='用户ID')   # 模型类声明外键时，传的是数据库中真实表名及字段名，用于关联查询时生成的SQL语句的传入，而非模型类名和属性名；实际数据库中并没有外键关系
    gender = db.Column(db.Integer, default=0, doc='性别')
    birthday = db.Column(db.Date, doc='生日')
    real_name = db.Column(db.String, doc='真实姓名')
    id_number = db.Column(db.String, doc='身份证号')
    id_card_front = db.Column(db.String, doc='身份证正面')
    id_card_back = db.Column(db.String, doc='身份证背面')
    id_card_handheld = db.Column(db.String, doc='手持身份证')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')     # default值为一个函数，模型类创建时会自动调用now()函数
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')   # onupdate指定修改时的调用
    register_media_time = db.Column(db.DateTime, doc='注册自媒体时间')

    area = db.Column(db.String, doc='地区')
    company = db.Column(db.String, doc='公司')
    career = db.Column(db.String, doc='职业')


class Relation(db.Model):
    """
    用户关系表
    """
    __tablename__ = 'user_relation'

    class RELATION:
        DELETE = 0
        FOLLOW = 1
        BLACKLIST = 2

    id = db.Column('relation_id', db.Integer, primary_key=True, doc='主键ID')
    user_id = db.Column(db.Integer, doc='用户ID')
    # user_id = db.Column(db.Integer, db.ForeignKey('user_basic.user_id'), doc='用户ID')
    target_user_id = db.Column(db.Integer, doc='目标用户ID')
    relation = db.Column(db.Integer, doc='关系')
    ctime = db.Column('create_time', db.DateTime, default=datetime.now, doc='创建时间')
    utime = db.Column('update_time', db.DateTime, default=datetime.now, onupdate=datetime.now, doc='更新时间')

    user = db.relationship('User', primaryjoin='Relation.target_user_id==foreign(User.id)', uselist=False)