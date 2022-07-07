from flask import jsonify
from commen.settings.default import DefaultConfig
from core.set_app import create_app


app = create_app(DefaultConfig)


@app.route('/')
def index():
    """
    主页
    """
    return 'index page'

@app.route('/doc')
def route_map():
    """
    主视图，返回所有视图网址
    """
    rules_iterator = app.url_map.iter_rules()
    return jsonify({rule.endpoint: rule.rule for rule in rules_iterator if rule.endpoint not in ('route_map', 'static')})


