from flask import jsonify, request
from flask import Blueprint
from app.event import user_event

user_bp = Blueprint('user_api', __name__) # 第一个参数是蓝图名称

@user_bp.route("/")
def hello():
    return 'hello world!'


@user_bp.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    data = user_event.get_all_users()
    return jsonify({"data": data, "msg": "查询成功"})

