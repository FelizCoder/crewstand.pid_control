import json
from fastapi import FastAPI
from typing import Optional
import websocket
import threading
from pydantic import BaseModel
from simple_pid import PID

from .swncrew_backend_client import Client
from .swncrew_backend_client.models.sensor_reading import SensorReading

backend_base = "localhost:5000"  # TODO: implement pydantic settings
# Sensor ID for the sensor WebSocket connection (UPDATE THIS TO MATCH YOUR SENSOR ID)
sensor_id = 0  # Update this to the actual sensor ID you're connecting to

rest_client = Client(base_url=f"http://{backend_base}", timeout=0.5)

app = FastAPI()

# PID Controller constants
KP = 1.0  # Proportional gain
KI = 0.1  # Integral gain
KD = 0.05  # Derivative gain

pid = PID(KP, KI, KD, output_limits=(0, 100), auto_mode=False)

# State variables
setpoint: Optional[float] = None
sensor_reading: Optional[float] = None


# Pydantic model for PID output (optional, for API responses if needed)
class PIDComponents(BaseModel):
    P: float
    I: float
    D: float


# PID Controller function
def calculate_pid_output():
    global sensor_reading, setpoint

    output = pid(sensor_reading)
    print(f"Calculated PID output: {output}")

    return output


# WebSocket connections
setpoint_ws = None
sensor_ws = None


def on_setpoint_message(ws, message):
    global setpoint, sensor_reading
    print(f"Received setpoint message: {message}")

    try:
        if message == "null":
            setpoint = None
            pid.set_auto_mode(False)
            print("PID set to manual mode")
            return
        elif setpoint is None:
            setpoint = float(message)
            pid.set_auto_mode(True, last_output=0)
            pid.setpoint = setpoint
            print(f"PID set to auto mode with setpoint: {pid.setpoint}")
        else:
            setpoint = float(message)
            pid.setpoint = setpoint
            print(f"Setpoint updated to: {pid.setpoint}")

        output = calculate_pid_output()
        # TODO: Send the output to the actuator (e.g., via another WebSocket or API call)
        print(f"PID Output: {output}")
    except:
        print(f"Error processing setpoint message: {message}")


def on_sensor_message(ws, message):
    global sensor_reading
    print(f"Received sensor message: {message}")
    try:
        sensor_reading = SensorReading(**json.loads(message)).value
        print(f"Sensor Reading: {sensor_reading}")
        output = calculate_pid_output()
        if output is not None:
            # TODO: Send the output to the actuator (e.g., via another WebSocket or API call)
            print(f"PID Output: {output}")
    except:
        print(f"Error processing sensor message: {message}")


def on_setpoint_error(ws, error):
    print(f"Setpoint WebSocket Error: {error}")


def on_sensor_error(ws, error):
    print(f"Sensor WebSocket Error: {error}")


def on_setpoint_close(ws, close_status_code, close_msg):
    print("Setpoint WebSocket Closed")


def on_sensor_close(ws, close_status_code, close_msg):
    print("Sensor WebSocket Closed")


# Establish WebSocket connections in separate threads to avoid blocking
def establish_ws_connections():
    global setpoint_ws, sensor_ws

    def run_setpoint_ws():
        print("Connecting to setpoint WebSocket...")
        setpoint_ws = websocket.WebSocketApp(
            f"ws://{backend_base}/v1/sensors/flowmeters/ws/setpoint/0",
            on_message=on_setpoint_message,
            on_error=on_setpoint_error,
            on_close=on_setpoint_close,
        )
        setpoint_ws.run_forever()

    def run_sensor_ws():
        print("Connecting to sensor WebSocket...")
        sensor_ws = websocket.WebSocketApp(
            f"ws://{backend_base}/v1/sensors/flowmeters/ws/0",
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
    return {"status": "ok"}


# Optional: PID Output endpoint (if you want to expose the PID output via API)
@app.get("/pid/components", response_model=PIDComponents)
def get_pid_output():
    (p, i, d) = pid.components
    return PIDComponents(P=p, I=i, D=d)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
