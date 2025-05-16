from common.logger import test as test_logger
from common.redis import test as test_redis
from common.generate_fake_data import test as test_gen_fake_data

def test():
    test_logger()
    test_redis()
    test_gen_fake_data()

test()