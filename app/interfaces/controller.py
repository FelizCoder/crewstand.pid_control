from abc import ABC, abstractmethod
from typing import Optional

from app.swncrew_backend_client.models.sensor_reading import SensorReading


class ControllerInterface(ABC):
    """
    Abstract interface for controller implementations.

    Defines the required methods that any controller implementation must provide
    for calculating updates based on current values and managing setpoints.
    """

    @abstractmethod
    def calculate_update(self, sensor_reading: SensorReading) -> Optional[float]:
        pass

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
