from abc import ABC, abstractmethod


class HealthCheck(ABC):
    name: str

    @abstractmethod
    def check(self) -> bool:
        """Return True if healthy, False otherwise"""
        pass
