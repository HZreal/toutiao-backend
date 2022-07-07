import os, sys
from core import app


def start():
    # 设置导包路径
    # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # sys.path.insert(0, os.path.join(BASE_DIR, 'common'))

    app.run(host='127.0.0.1', port=5000, debug=True)


if __name__ == '__main__':
    start()




