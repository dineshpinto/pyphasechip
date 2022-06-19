from dataclasses import dataclass


@dataclass(frozen=True)
class Parameters:
    """ Dump to store all static parameters """
    # ImageData
    convertScaleAbs_alpha: float = 0.9
    convertScaleAbs_beta: float = 50
    brightness: int = 252
    contrast: int = 148
    first_derivative_scale: int = 1
    first_derivative_delta: int = 0
