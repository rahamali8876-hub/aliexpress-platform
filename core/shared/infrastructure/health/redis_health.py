from django.conf import settings
import redis
from .base import HealthCheck


class RedisHealthCheck(HealthCheck):
    name = "redis"

    def check(self) -> bool:
        try:
            client = redis.Redis.from_url(settings.REDIS_URL)
            return client.ping()
        except Exception:
            return False
