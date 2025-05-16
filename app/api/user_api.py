from flask import jsonify, request
from flask import Blueprint

user_bp = Blueprint('user_api', __name__) # 第一个参数是蓝图名称

@user_bp.route("/")
def hello():
    return 'hello world!'
