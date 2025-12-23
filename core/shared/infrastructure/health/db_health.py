from django.db import connections
from django.db.utils import OperationalError
from .base import HealthCheck


class DatabaseHealthCheck(HealthCheck):
    name = "database"

    def check(self) -> bool:
        try:
            connections["default"].cursor()
            return True
        except OperationalError:
            return False
