from typing import Optional
from simple_pid import PID

from app.interfaces.controller import ControllerInterface
from app.swncrew_backend_client.models.sensor_reading import SensorReading
from app.utils.config import config
from app.utils.influx_client import influx_connector
from app.utils.logger import logger


class PIDController(ControllerInterface):
    def __init__(self):
        self.pid = PID(
            config.PID_KP,
            config.PID_KI,
            config.PID_KD,
            output_limits=(config.PID_OUTPUT_MIN, config.PID_OUTPUT_MAX),
            auto_mode=False,
        )

    def calculate_update(self, sensor_reading: SensorReading) -> Optional[float]:
        update = self.pid(sensor_reading.value)
        logger.debug(f"Calculated PID Update {update}")
        influx_connector.write_pid(self.pid, sensor_reading.timestamp_ns)
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
