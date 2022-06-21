import datetime
import json
import os
from dataclasses import dataclass
from typing import List, Tuple

from dataclasses_json import dataclass_json

from src.data_structures import ImageData, Droplet
from src.helpers import extract_metadata_from_filename
from src.logic import ImageFilter, LLPSDetection, ShapeDetection


@dataclass_json
@dataclass(frozen=True)
class Parameters:
    """ Dump to store all static parameters """
    folder_path: str = "data/"
    image_shape: Tuple[int, int] = (100, 100)
    concentration: float = 1.0
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

    def save(self, filepath: str):
        """ Save dataclass to JSON file. Note: mutable data like lists, arrays etc. cannot be saved"""
        with open(filepath, "w") as f:
            f.write(self.to_json(indent=4))

    def load(self, filepath: str) -> dataclass_json:
        """ Load dataclass from JSON file """
        with open(filepath, "r") as f:
            data = json.load(f)
        return self.from_json(json.dumps(data))


if __name__ == "__main__":
    params = Parameters()

    # Read folder and save each image as an instance of ImageData
    images: List[ImageData] = []
    for file in os.listdir(params.folder_path):
        well_number, timestamp = extract_metadata_from_filename(file)
        # Write data into list of dataclass ImageData
        images.append(
            ImageData(
                filepath=file,
                well_number=well_number,
                timestamp=timestamp,
                params=params
            )
        )

    # Run image filter
    image_filter = ImageFilter(image_shape=params.image_shape)
    for image in images:
        image.filtered_image = image_filter.filter_background()

    # Run droplet detection
    shape_detector = ShapeDetection()
    for image in images:
        (x, y, r) = shape_detector.hough_circle_detector(image=image.filtered_image)
        if x and y and r:
            image.droplet = Droplet(
                center_x=x,
                center_y=y,
                radius=r
            )

    # Check for LLPS
    llps_detector = LLPSDetection()
    for image in images:
        image.droplet.phase_separation = llps_detector.has_phase_separated()

    # Save parameters to JSON for each run
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_path = f"{timestamp}_data.json"
    params.save(filepath=file_path)

    # Reload parameters from previous run
    previous_parameters = Parameters().load(filepath=file_path)
    print(previous_parameters)
