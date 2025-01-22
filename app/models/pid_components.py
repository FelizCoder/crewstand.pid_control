from typing import Tuple
from pydantic import BaseModel


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

    @classmethod
    def new(cls, components: Tuple[float, float, float]):
        """
        Create a new PIDComponents instance with the specified components.

        Args:
            components (Tuple[float, float, float]): A tuple containing the P, I, and D components.

        Returns:
            PIDComponents: A new instance of PIDComponents with the specified P, I, and D values.
        """
        return PIDComponents(P=components[0], I=components[1], D=components[2])
