# import redis
# import os
# from dotenv import load_dotenv
#
# load_dotenv()
#
# redis_host = os.getenv('redis_host')
# redis_port = os.getenv('redis_port')
# redis_db = os.getenv('redis_db')
#
# redis_client = redis.Redis(
#     host=redis_host,
#     port=redis_port,
#     db=redis_db)
#
# # foo = redis_client.set(1, 'foo')
# # bar = redis_client.get(1)
#
# # print(foo, bar)