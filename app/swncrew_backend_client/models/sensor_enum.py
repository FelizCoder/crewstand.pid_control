from enum import Enum


class SensorEnum(str, Enum):
    FLOWMETER = "flowmeter"

    def __str__(self) -> str:
        return str(self.value)
