from enum import Enum


class ProportionalValveType(str, Enum):
    PROPORTIONAL_VALVE = "proportional valve"

    def __str__(self) -> str:
        return str(self.value)
