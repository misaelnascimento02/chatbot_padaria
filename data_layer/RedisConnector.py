import redis

class RedisConnector:
    def inc(key):
        cache = redis.Redis(host='redis', port=6379)
        retries = 5
        while True:
            try:
                return cache.incr(key)                                   
            except redis.exceptions.ConnectionError as exc:
                if retries == 0:
                    raise exc
                retries -= 1
                time.sleep(0.5)
