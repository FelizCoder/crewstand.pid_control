from enum import Enum


class PumpType(str, Enum):
    PUMP = "pump"

    def __str__(self) -> str:
        return str(self.value)
