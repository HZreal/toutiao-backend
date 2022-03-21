from flask import Flask
from settings import FlaskConfig

app = Flask(__name__)

app.config.from_object(FlaskConfig)




@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'










if __name__ == '__main__':
    app.run()
