import json
from fastapi import FastAPI
from typing import Optional, Tuple
import websocket
import threading
from pydantic import BaseModel
from simple_pid import PID

from .utils.config import config
from .utils.influx_client import influx_connector
from .utils.logger import logger

from .swncrew_backend_client import Client
from .swncrew_backend_client.api.proportional_valves import (
    set_state_v1_actuators_proportional_set_post as set_proportional,
)
from .swncrew_backend_client.models.sensor_reading import SensorReading
from .swncrew_backend_client.models.proportional_valve import ProportionalValve

rest_client = Client(base_url=f"http://{config.BACKEND_BASE}", timeout=0.5)

app = FastAPI(
    version=config.VERSION,
    title=config.PROJECT_NAME,
    debug=config.DEBUG_LEVEL == "DEBUG",
)

pid = PID(
    config.PID_KP,
    config.PID_KI,
    config.PID_KD,
    output_limits=(config.PID_OUTPUT_MIN, config.PID_OUTPUT_MAX),
    auto_mode=False,
)

# State variables
setpoint: Optional[float] = None
sensor_reading: Optional[SensorReading] = None


class PIDComponents(BaseModel):
    """
    Model representing the components of a PID controller output.

    Parameters
    ----------
    P : float
        Proportional component of the PID output
    I : float
        Integral component of the PID output
    D : float
        Derivative component of the PID output
    """

    P: float
    I: float
    D: float

    def new(components: Tuple[float, float, float]):
        return PIDComponents(P=components[0], I=components[1], D=components[2])


# PID Controller function
def calculate_pid_update(sensor_reading: SensorReading) -> float:
    """
    Calculate PID controller update based on sensor reading.

    Parameters
    ----------
    sensor_reading : SensorReading
        Current sensor reading containing value and timestamp

    Returns
    -------
    float
        Calculated PID update value
    """
    update = pid(sensor_reading.value)

    logger.debug(f"Calculated PID Update {update}")

    return update


def actuator_update(update_state: float) -> None:
    """
    Update the actuator with new PID controller output.

    Parameters
    ----------
    update_state : float
        New state value for the proportional valve

    Returns
    -------
    None
    """
    update_request = ProportionalValve(
        id=config.PROPORTIONAL_VALVE_ID, state=update_state
    )
    update_response = set_proportional.sync(client=rest_client, body=update_request)
    logger.debug(f"Actuator update response: {update_response}")

    influx_connector.write_pid(pid, sensor_reading.timestamp_ns)


def on_setpoint_message(ws, message):
    """
    WebSocket callback for handling setpoint messages.

    Parameters
    ----------
    ws : WebSocket
        WebSocket connection instance
    message : str
        Received message containing new setpoint value

    Returns
    -------
    None
    """
    logger.debug(f"Received setpoint message: {message}")

    try:
        if message == "null":
            pid.set_auto_mode(False)
            actuator_update(0.0)
            logger.debug("PID in manual mode")
            return
        elif not pid.auto_mode:
            setpoint = float(message)
            pid.set_auto_mode(True, last_output=0)
            pid.setpoint = setpoint
            logger.debug(f"PID set to auto mode with setpoint: {pid.setpoint}")
        else:
            setpoint = float(message)
            pid.setpoint = setpoint
            logger.debug(f"Setpoint updated to: {pid.setpoint}")

        output = calculate_pid_update(sensor_reading)
        logger.debug(f"PID Update {output}")

        if output is not None:
            actuator_update(output)
        else:
            logger.error("Could not calculate PID update")

    except:
        logger.error(f"Error processing setpoint message: {message}")


def on_sensor_message(ws, message):
    """
    WebSocket callback for handling sensor messages.

    Parameters
    ----------
    ws : WebSocket
        WebSocket connection instance
    message : str
        Received message containing sensor reading data

    Returns
    -------
    None
    """
    global sensor_reading
    logger.debug(f"Received sensor message: {message}")
    try:
        sensor_reading = SensorReading(**json.loads(message))
        logger.debug(f"Sensor Reading: {sensor_reading}")
        update = calculate_pid_update(sensor_reading)
        logger.debug(f"PID Update {update}")
        if update is not None:
            actuator_update(update)
    except:
        logger.error(f"Error processing sensor message: {message}")


def on_setpoint_error(ws, error):
    logger.error(f"Setpoint WebSocket Error: {error}")


def on_sensor_error(ws, error):
    logger.error(f"Sensor WebSocket Error: {error}")


def on_setpoint_close(ws, close_status_code, close_msg):
    logger.info("Setpoint WebSocket Closed")


def on_sensor_close(ws, close_status_code, close_msg):
    logger.info("Sensor WebSocket Closed")


# Establish WebSocket connections in separate threads to avoid blocking
def establish_ws_connections():
    """
    Establish WebSocket connections for setpoint and sensor data.

    Creates and starts two daemon threads for handling WebSocket connections:
    - Setpoint WebSocket: receives target values
    - Sensor WebSocket: receives current sensor readings

    Returns
    -------
    None
    """
    global setpoint_ws, sensor_ws

    def run_setpoint_ws():
        logger.info("Connecting to setpoint WebSocket...")
        setpoint_ws = websocket.WebSocketApp(
            f"ws://{config.BACKEND_BASE}/v1/sensors/flowmeters/ws/setpoint/0",
            on_message=on_setpoint_message,
            on_error=on_setpoint_error,
            on_close=on_setpoint_close,
        )
        setpoint_ws.run_forever()

    def run_sensor_ws():
        logger.info("Connecting to sensor WebSocket...")
        sensor_ws = websocket.WebSocketApp(
            f"ws://{config.BACKEND_BASE}/v1/sensors/flowmeters/ws/0",
            on_message=on_sensor_message,
            on_error=on_sensor_error,
            on_close=on_sensor_close,
        )
        sensor_ws.run_forever()

    setpoint_thread = threading.Thread(target=run_setpoint_ws)
    sensor_thread = threading.Thread(target=run_sensor_ws)

    setpoint_thread.daemon = True
    sensor_thread.daemon = True

    setpoint_thread.start()
    sensor_thread.start()


thread = threading.Thread(target=establish_ws_connections)
thread.daemon = True
thread.start()


# Health check endpoint
@app.get("/health")
def read_health():
    """
    Health check endpoint.

    Returns
    -------
    dict
        Dictionary containing service status
    """
    return {"status": "ok"}


# Optional: PID Output endpoint (if you want to expose the PID output via API)
@app.get("/pid/components", response_model=PIDComponents)
def get_pid_output():
    """
    Endpoint to retrieve current PID controller components.

    Returns
    -------
    PIDComponents
        Object containing current P, I, and D components
    """
    components = pid.components
    return PIDComponents.new(components)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
