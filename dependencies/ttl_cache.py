# from cachetools import TTLCache
from dependencies.redis_client import RedisClient


exp_timestamp=86400

# cache_tool=TTLCache(maxsize=100, ttl=exp_timestamp)

class CacheTool:

    @classmethod
    async def set_cache(self, token):
        try:
            client_instance = RedisClient()
            client=await client_instance.redis_client()
            await client.set(f'user_{token}', token, ex=exp_timestamp)
        except Exception as e:
            print(f'Redis triggerd an error check your logs. - {e}')
    




    @classmethod
    async def get_cache(self,token):
        try:
            client_instance = RedisClient()
            client=await client_instance.redis_client()
            cached_token = await client.get(f'user_{token}')
            return cached_token
    
        except Exception as e:
            print(f'Redis triggerd an error check your logs. - {e}')
  