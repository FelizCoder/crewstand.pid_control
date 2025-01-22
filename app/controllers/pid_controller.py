from typing import Optional
from simple_pid import PID

from app.interfaces.controller import ControllerInterface
from app.utils.config import config
from app.utils.logger import logger


class PIDController(ControllerInterface):
    """
    PIDController is a class that implements a Proportional-Integral-Derivative (PID) controller.

    Attributes:
        pid (PID): An instance of the PID class configured with parameters from the config module.

    Methods:
        __init__():
            Initializes the PIDController with PID parameters 
            and output limits from the config module.

        calculate_update(current_value: float) -> Optional[float]:
            Calculates the PID update based on the current value.
            Args:
                current_value (float): The current value to be used by the PID controller.
            Returns:
                Optional[float]: The calculated PID update value.

        set_setpoint(setpoint: Optional[float]) -> None:
            Sets the setpoint for the PID controller.
            If the setpoint is None, the PID controller is disabled.
            Args:
                setpoint (Optional[float]): 
                    The desired setpoint for the PID controller. 
                    If None, the controller is disabled.
    """

    def __init__(self):
        self.pid = PID(
            config.PID_KP,
            config.PID_KI,
            config.PID_KD,
            output_limits=(config.PID_OUTPUT_MIN, config.PID_OUTPUT_MAX),
            auto_mode=False,
        )

    def calculate_update(self, current_value: float) -> Optional[float]:
        update = self.pid(current_value)
        logger.debug(f"Calculated PID Update {update}")
        return update

    def set_setpoint(self, setpoint: Optional[float]) -> None:
        # TODO: on first None an Update of 0 should be emitted
        if setpoint is None:
            self.pid.set_auto_mode(False)
            logger.debug("Setpoint is None, disabling PID controller")
            return

        if not self.pid.auto_mode:
            self.pid.set_auto_mode(True, last_output=0)
            logger.debug("Setpoint is set, enabling PID controller")
        self.pid.setpoint = setpoint
        logger.debug(f"Setpoint updated to {setpoint}")
