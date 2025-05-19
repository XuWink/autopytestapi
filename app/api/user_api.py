from flask import jsonify, request
from flask import Blueprint
from app.event import user_event
from utils.util import validate_phone_number
from common.logger import logger
from common.httpstatus import HTTPStatus

user_bp = Blueprint('user_api', __name__) # 第一个参数是蓝图名称

DEFAULT_ROLE = 1 # 默认1普通，0管理员

@user_bp.route("/")
def hello():
    return 'hello world!'


@user_bp.route("/users", methods=["GET"])
def get_all_users():
    """获取所有用户信息"""
    data = user_event.get_all_users()
    return jsonify({"data": data, "msg": "成功"}), HTTPStatus.OK


@user_bp.route("/users/<string:username>", methods=['GET'])
def get_user(username):
    '''获取某个用户的信息'''
    data = user_event.get_user(username)
    if data:
        return jsonify({"data":data,"msg":"成功"}), HTTPStatus.OK
    return jsonify({"data": None, "msg":"查找失败"}), HTTPStatus.BAD_REQUEST


@user_bp.route("/register", methods=['POST'])
def user_register():
    '''用户注册'''
    username = request.json.get("username","").strip()
    password = request.json.get("password", "").strip()
    sex = request.json.get("sex", "0").strip()  # 默认0(男性)
    telephone = request.json.get("telephone","").strip()
    address = request.json.get("address","").strip()
    
    if not username or not password or not telephone:
        return jsonify({"data":None, "msg": "用户名/密码/手机号不能为空，请检查"}), HTTPStatus.BAD_REQUEST
    
    if sex not in ("0", "1"):
        return jsonify({"data": None, "msg": "输入的性别只能是0（男）或1（女）"}), HTTPStatus.BAD_REQUEST
    
    if not validate_phone_number(telephone):
        return jsonify({"data": None, "msg": "手机号格式不正确"}), HTTPStatus.BAD_REQUEST
    
    try:
        res1 = user_event.select_by_username(username)
        if res1:
            return jsonify({"data":None, "msg":"用户名已存在，注册失败"}), HTTPStatus.BAD_REQUEST
        res2 = user_event.select_by_telephone(telephone)
        if res2:
            return jsonify({"data":None, "msg": "手机号已被注册"}), HTTPStatus.BAD_REQUEST
        
        r = user_event.register(username, password, DEFAULT_ROLE, sex, telephone, address)
        if r:
            return jsonify({"data":None, "msg": "注册成功！"}), HTTPStatus.OK
        return jsonify({"data": None, "msg": "注册失败"}), HTTPStatus.BAD_REQUEST

    except Exception as e:
        logger.error("注册失败：{e}")
        return jsonify({"data":None, "msg": "服务器内部错误，请稍后再试"}), HTTPStatus.INTERNAL_SERVER_ERROR