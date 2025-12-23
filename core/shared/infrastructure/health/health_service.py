from .db_health import DatabaseHealthCheck
from .redis_health import RedisHealthCheck
from .kafka_health import KafkaHealthCheck


class HealthService:
    def __init__(self):
        self.checks = [
            DatabaseHealthCheck(),
            RedisHealthCheck(),
            KafkaHealthCheck(),
        ]

    def run(self) -> dict:
        results = {}
        overall_ok = True

        for check in self.checks:
            healthy = check.check()
            results[check.name] = "ok" if healthy else "down"
            if not healthy:
                overall_ok = False

        return {
            "status": "ok" if overall_ok else "degraded",
            "checks": results,
        }
