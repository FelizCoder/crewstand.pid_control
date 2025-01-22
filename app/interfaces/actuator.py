from abc import ABC, abstractmethod


class ActuatorInterface(ABC):
    """
    Abstract base class for an actuator interface.

    Methods
    -------
    update(value: float, timestamp_ns: int) -> None
        Update the actuator with a new value and timestamp.
    """
    @abstractmethod
    def update(self, value: float, timestamp_ns: int) -> None:
        """
        Update the actuator with a new value.

        Args:
            value (float): The new value to set for the actuator.
            timestamp_ns (int): The timestamp in nanoseconds when the update is made.

        Returns:
            None
        """
