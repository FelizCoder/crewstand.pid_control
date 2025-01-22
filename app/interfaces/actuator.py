from abc import ABC, abstractmethod


class ActuatorInterface(ABC):
    """
    Abstract base class for an actuator interface.

    Methods
    -------
    update(value: float) -> None
        Update the actuator with a new value and timestamp.
    """

    @abstractmethod
    def update(self, value: float) -> None:
        """
        Update the actuator with a new value.

        Args:
            value (float): The new value to set for the actuator.

        Returns:
            None
        """
