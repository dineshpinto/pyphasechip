import json
import os
from dataclasses import dataclass
from typing import Tuple

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class Parameters:
    """ Dump to store all static parameters """
    folder_path: str = os.path.join(os.getcwd(), "data")
    file_ext: str = "png"
    image_shape: Tuple[int, int] = (100, 100)
    concentration: float = 1.0
    num_wells: int = 10
    # convert to absolute scale
    alpha: float = 0.9
    beta: float = 50
    # adjust brightness and contrast
    brightness: int = 252
    contrast: int = 148
    # first derivative
    scale: int = 1
    delta: int = 0
    # well diameter filtering
    diameter: int = 238
    min_radius: int = round((diameter / 2) * 0.7)
    max_radius: int = round((diameter / 2) * 1.3)
    # edge delta for time point of phase separation
    edge_delta: float = 1

    def save(self, filepath: str):
        """ Save dataclass to JSON file. Note: mutable data like lists, arrays etc. cannot be saved"""
        with open(filepath, "w") as f:
            f.write(self.to_json(indent=4))

    def load(self, filepath: str) -> dataclass_json:
        """ Load dataclass from JSON file """
        with open(filepath, "r") as f:
            data = json.load(f)
        return self.from_json(json.dumps(data))
