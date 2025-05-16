from flask import Flask
from app.api.user_api import user_bp


def create_app():
    app = Flask(__name__)
    # 注册蓝图
    app.register_blueprint(user_bp)

    return app