from abc import ABC, abstractmethod
from typing import Optional


class ControllerInterface(ABC):
    """
    Abstract interface for controller implementations.

    Defines the required methods that any controller implementation must provide
    for calculating updates based on current values and managing setpoints.
    """

    @abstractmethod
    def calculate_update(self, current_value: float) -> Optional[float]:
        """
        Calculate controller update based on current value.

        Parameters
        ----------
        current_value : float
            Current measured value from sensor

        Returns
        -------
        Optional[float]
            Calculated update value, or None if update cannot be calculated
        """

    @abstractmethod
    def set_setpoint(self, setpoint: Optional[float]) -> None:
        """
        Set the controller's target setpoint.

        Parameters
        ----------
        setpoint : Optional[float]
            Target value for the controller, None to disable control

        Returns
        -------
        None
        """
