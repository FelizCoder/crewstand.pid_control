from app.interfaces.actuator import ActuatorInterface
from app.utils.config import config
from app.utils.logger import logger
from app.utils.influx_client import influx_connector
from app.swncrew_backend_client import Client
from app.swncrew_backend_client.models.proportional_valve import ProportionalValve
from app.swncrew_backend_client.api.proportional_valves import (
    set_state_v1_actuators_proportional_set_post,
)


class ProportionalValveActuator(ActuatorInterface):
    """
    ProportionalValveActuator is responsible for controlling a proportional valve actuator.
    Attributes:
        client (Client): The client used to communicate with the actuator.
    Methods:
        __init__(client: Client):
            Initializes the ProportionalValveActuator with the given client.
        update(value: float, timestamp_ns: int) -> None:
            Updates the state of the proportional valve actuator with the given value and timestamp.
            Logs the response from the actuator and writes the PID value to the influx connector.
    """

    def __init__(self, client: Client):
        self.client = client

    def update(self, value: float, timestamp_ns: int) -> None:
        update_request = ProportionalValve(id=config.PROPORTIONAL_VALVE_ID, state=value)
        response = set_state_v1_actuators_proportional_set_post.sync(
            client=self.client, body=update_request
        )
        logger.debug(f"Actuator update response: {response}")
        influx_connector.write_pid(value, timestamp_ns)
