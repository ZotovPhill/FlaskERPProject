from dogpile.cache.region import make_region
from app.orm.caching.caching_query import ORMCache
from app.core.settings import settings
from hashlib import md5


regions = {}

def md5_key_mangler(key):
    return md5(key.encode("ascii")).hexdigest()

regions["default"] = make_region(
    key_mangler=md5_key_mangler
).configure(
    'dogpile.cache.redis',
    arguments = {
        'host': settings.cache_redis_host,
        'port': settings.cache_redis_port,
        'db': settings.cache_redis_db,
        'redis_expiration_time': settings.cache_default_timeout,
        'distributed_lock': True,
        'thread_local_lock': False
    }
)

# regions["local_session"] = make_region().configure(
#     "sqlalchemy.session", arguments={"scoped_session": Session}
# )


cache = ORMCache(regions)
