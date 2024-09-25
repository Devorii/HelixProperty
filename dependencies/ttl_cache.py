from cachetools import TTLCache

exp_timestamp=3600

cache_tool=TTLCache(maxsize=100, ttl=exp_timestamp)

class CacheTool:

    @staticmethod
    def set_cache(token):
        cache_tool[f'user_{token}']=token

    @staticmethod
    def get_cache(token):
        cached_token = cache_tool.get(f'user_{token}')
        return cached_token
