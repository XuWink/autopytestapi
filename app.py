# from common.logger import test as test_logger
# from common.redis import test as test_redis
# from common.generate_fake_data import test as test_gen_fake_data

# def test():
#     test_logger()
#     test_redis()
#     test_gen_fake_data()

# test()

import sys
from app import create_app
from config.setting import SERVER_HOST, SERVER_PORT
from utils.util import get_base_path

sys.path.insert(0, get_base_path())

# @app.route("/")
# def hello():
#     return 'hello world!'

if __name__ == "__main__":
    app = create_app()
    app.run(host=SERVER_HOST, port=SERVER_PORT, debug=False)