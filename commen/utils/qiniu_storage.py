from qiniu import Auth, put_file, put_data, etag
from flask import current_app

import qiniu.config


def upload(file_data):
    """
    上传文件到七牛云服务
    :param file_data: 视图接收到的图片二进制数据
    :return: key: 文件名
    """

    # Access Key 和 Secret Key
    access_key = current_app.config['QINIU_ACCESS_KEY']
    secret_key = current_app.config['QINIU_SECRET_KEY']

    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 要上传的对象空间
    bucket_name = current_app.config['QINIU_BUCKET_NAME']

    print('ak={};  sk={};  bn={}'.format(access_key, secret_key, bucket_name))

    # 上传后保存的文件名
    # key = 'my-news-logo.png'
    key = None      # 不指定文件名，由qiniu服务提供(uuid)

    # 生成上传 Token，可以指定过期时间、上传策略
    token = q.upload_token(bucket_name, key, 360000, policy=None)
    print('token={}'.format(token))

    # 以本地文件进行上传
    # localfile = './static/my-news-logo.jpg'
    # ret, info = put_file(token, key, localfile)
    # 以文件数据(如图片二进制数据)上传，前端/客户端传来的数据保存在内存
    ret, info = put_data(token, key, file_data)
    print('ret={}'.format(ret))                 # {'hash': 'Fv9NW-O8Ysg0ytgK6uggLaJjfk6z', 'key': 'Fv9NW-O8Ysg0ytgK6uggLaJjfk6z'}
    print('info={}'.format(info))               # _ResponseInfo__response:<Response [200]>

    # 返回文件名
    return ret['key']



if __name__ == '__main__':
    with open('/Users/hz/Desktop/WeChat323b195bcc71489a188da4a087620c69.png', 'rb') as f:
        content = f.read()
        file_name = upload(content)
        print(file_name)