import threading
from typing import Optional
import json
import websocket

from app.interfaces.actuator import ActuatorInterface
from app.interfaces.controller import ControllerInterface
from app.utils.config import config
from app.utils.logger import logger
from app.swncrew_backend_client.models.sensor_reading import SensorReading


class WebSocketService:
    """
    Service handling WebSocket connections for setpoint and sensor data.

    Parameters
    ----------
    controller : ControllerInterface
        Controller implementation for processing setpoint and sensor data
    actuator : ActuatorInterface
        Actuator implementation for applying controller updates

    Attributes
    ----------
    sensor_reading : Optional[SensorReading]
        Latest sensor reading received
    setpoint_ws : Optional[websocket.WebSocketApp]
        WebSocket connection for setpoint data
    sensor_ws : Optional[websocket.WebSocketApp]
        WebSocket connection for sensor data
    """

    def __init__(self, controller: ControllerInterface, actuator: ActuatorInterface):
        """
        Initialize WebSocket service with controller and actuator.

        Parameters
        ----------
        controller : ControllerInterface
            Controller implementation for processing setpoint and sensor data
        actuator : ActuatorInterface
            Actuator implementation for applying controller updates
        """
        self.actuator = actuator
        self.controller = controller
        self.sensor_reading: Optional[SensorReading] = None
        self.setpoint_ws: Optional[websocket.WebSocketApp] = None
        self.sensor_ws: Optional[websocket.WebSocketApp] = None

    def start(self):
        """Start WebSocket connections in daemon threads"""
        self._establish_connections()

    def _establish_connections(self):
        """Create and start WebSocket connection threads"""
        setpoint_thread = threading.Thread(target=self._run_setpoint_ws)
        sensor_thread = threading.Thread(target=self._run_sensor_ws)

        setpoint_thread.daemon = True
        sensor_thread.daemon = True

        setpoint_thread.start()
        sensor_thread.start()

    def _run_setpoint_ws(self):
        """Run setpoint WebSocket connection"""
        while True:
            try:
                self.setpoint_ws = websocket.WebSocketApp(
                    f"ws://{config.BACKEND_BASE}/v1/sensors/flowmeters/ws/setpoint/{config.SENSOR_ID}",
                    on_message=self._on_setpoint_message,
                    on_error=self._on_setpoint_error,
                    on_close=self._on_setpoint_close,
                    on_open=self._on_setpoint_open,
                )
                self.setpoint_ws.run_forever()
            except Exception as e:
                logger.error(f"Setpoint WS error: {e}")
                threading.Event().wait(5)  # Wait before reconnecting

    def _run_sensor_ws(self):
        """Run sensor WebSocket connection"""
        while True:
            try:
                self.sensor_ws = websocket.WebSocketApp(
                    f"ws://{config.BACKEND_BASE}/v1/sensors/flowmeters/ws/{config.SENSOR_ID}",
                    on_message=self._on_sensor_message,
                    on_error=self._on_sensor_error,
                    on_close=self._on_sensor_close,
                    on_open=self._on_sensor_open,
                )
                self.sensor_ws.run_forever()
            except Exception as e:
                logger.error(f"Sensor WS error: {e}")
                threading.Event().wait(5)  # Wait before reconnecting

    def _on_setpoint_message(self, _ws, message: str) -> None:
        """Handle setpoint messages"""
        logger.debug(f"Received setpoint message: {message}")
        try:
            setpoint = json.loads(message)
            self.controller.set_setpoint(setpoint)

            if self.sensor_reading:
                update = self.controller.calculate_update(self.sensor_reading)
                if update is not None:
                    self.actuator.update(update)

        except Exception as e:
            logger.error(f"Error processing setpoint message: {e}")

    def _on_sensor_message(self, _ws, message: str) -> None:
        """Handle sensor messages"""
        logger.debug(f"Received sensor message: {message}")
        try:
            self.sensor_reading = SensorReading(**json.loads(message))
            update = self.controller.calculate_update(self.sensor_reading)
            if update is not None:
                self.actuator.update(update)
        except Exception as e:
            logger.error(f"Error processing sensor message: {e}")

    # WebSocket event handlers
    def _on_setpoint_open(self, _ws):
        logger.info("Setpoint WebSocket opened")

    def _on_sensor_open(self, _ws):
        logger.info("Sensor WebSocket opened")

    def _on_setpoint_error(self, _ws, error):
        logger.error(f"Setpoint WebSocket error: {error}")

    def _on_sensor_error(self, _ws, error):
        logger.error(f"Sensor WebSocket error: {error}")

    def _on_setpoint_close(self, _ws, code, msg):
        logger.info(f"Setpoint WebSocket closed: {code} - {msg}")

    def _on_sensor_close(self, _ws, code, msg):
        logger.info(f"Sensor WebSocket closed: {code} - {msg}")
