from enum import Enum


class FlowmeterType(str, Enum):
    FLOWMETER = "flowmeter"

    def __str__(self) -> str:
        return str(self.value)
