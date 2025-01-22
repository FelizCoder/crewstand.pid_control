from fastapi import FastAPI

from app.actuators.proportional_valve import ProportionalValveActuator
from app.controllers.pid_controller import PIDController

from app.services.websocket_service import WebSocketService
from app.utils.config import config

from app.routes.api import create_api_router

from app.swncrew_backend_client import Client


app = FastAPI(
    version=config.VERSION,
    title=config.PROJECT_NAME,
    debug=config.DEBUG_LEVEL == "DEBUG",
)

# Setup Dependencies
pid = PIDController()
rest_client = Client(base_url=f"http://{config.BACKEND_BASE}", timeout=0.5)
proportional = ProportionalValveActuator(client=rest_client)
ws_service = WebSocketService(controller=pid, actuator=proportional)

ws_service.start()

api_router = create_api_router(controller=pid)
app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
