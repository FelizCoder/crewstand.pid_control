from fastapi import APIRouter
from app.models.pid_components import PIDComponents
from app.controllers.pid_controller import PIDController

def create_api_router(controller: PIDController) -> APIRouter:
    api_router = APIRouter()

    @api_router.get("/health")
    def read_health():
        """
        Check the health status of the application.

        Returns:
            dict: A dictionary containing the health status of the application.
        """
        return {"status": "ok"}

    @api_router.get("/pid/components", response_model=PIDComponents)
    def get_pid_components():
        """
        Retrieve the PID components from the given PID controller.

        Args:
            controller (PIDController): The PID controller instance, injected by dependency.

        Returns:
            PIDComponents: A new instance of PIDComponents containing the PID components.
        """
        components = controller.pid.components
        return PIDComponents.new(components)

    return api_router
