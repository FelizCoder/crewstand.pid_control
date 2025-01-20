from enum import Enum


class SolenoidValveType(str, Enum):
    SOLENOID_VALVE = "solenoid valve"

    def __str__(self) -> str:
        return str(self.value)
