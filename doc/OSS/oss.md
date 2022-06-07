# OSS对象存储服务

应用

特定行业的海量非结构化数据

特点

对象存储采用扁平的文件组织方式，所以在文件量上升至千万、亿级别，容量在PB级别的时候，这种文件组织方式下的性能优势就显现出来，文件不在有目录树深度的问题，历史和近线数据有同样的访问效率

## 一、需求

用户头像、文章图片等数据需要使用文件存储系统来保存

## 二、方案

- 自己搭建文件系统服务

- 选用第三方对象存储服务

  - 优势: 提供CDN服务

## 三、存储服务提供商

### 1. 七牛云

七牛云对象存储服务 http://www.qiniu.com。

#### 使用

1. 注册
2. 新建存储空间
3. 使用七牛SDK完成代码实现

#### kodo文档

https://developer.qiniu.com/kodo

##### kodo API

https://developer.qiniu.com/kodo/3939/overview-of-the-api

##### Python SDK 网址

https://developer.qiniu.com/kodo/1242/python

######  	Python安装SDK

```python
pip install qiniu
```

###### 编码

上传及回调

```python
# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth, put_file, etag
import qiniu.config

access_key = 'Access_Key'
secret_key = 'Secret_Key'

q = Auth(access_key, secret_key)

bucket_name = 'Bucket_Name'

key = 'my-python-logo.png'

#上传文件到存储后， 存储服务将文件名和文件大小回调给业务服务器。
policy={
 'callbackUrl':'http://your.domain.com/callback.php',
 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
 }

token = q.upload_token(bucket_name, key, 3600, policy)

localfile = './sync/bbb.jpg'

ret, info = put_file(token, key, localfile, version='v2') 
print(info)
assert ret['key'] == key
assert ret['hash'] == etag(localfile)

```



### 2. 腾讯云

#### COS使用

1. -
2. -

COS文档

https://cloud.tencent.com/document/product/436

API

https://cloud.tencent.com/document/product/436/7751

python SDK

https://cloud.tencent.com/document/product/436/12269

### 3. 阿里云

