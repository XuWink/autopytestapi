from flask import jsonify, request
from flask import Blueprint

user_bp = Blueprint('user_api', __name__) # 第一个参数是蓝图名称

@user_bp.route("/")
def hello():
    return 'hello world!'


@user_bp.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    sql = "SELECT * FROM user"
    data = db.select_db(sql)
    print("获取所有用户信息 == >> {}".format(data))
    return jsonify({"code": 0, "data": data, "msg": "查询成功"})


@user_bp.route("/users", methods=["POST"])
def create_new_user():
    """<UNK>"""
    data = request.get_json()