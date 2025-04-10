import redis
import os
from dotenv import load_dotenv


load_dotenv()

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORTS')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

class RedisClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
            cls._instance.init_redis=redis.asyncio.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                password=REDIS_PASSWORD,
                decode_responses=True,
            )
        return cls._instance

    async def redis_client(self):
        if hasattr(self, 'init_redis'):
            return self.init_redis

    async def redis_client_close(self):
        if hasattr(self, 'init_redis'):
            await self.init_redis.close()



