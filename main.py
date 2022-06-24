import datetime
import os
from typing import List

from parameters import Parameters
from src.data_structures import ImageData, Droplet
from src.helpers import get_sorted_filepaths_from_folder
from src.logic import ImageFilter, LLPSDetection, ShapeDetection

if __name__ == "__main__":
    params = Parameters()

    # Read folder and save each image as an instance of ImageData
    images: List[ImageData] = []

    filepaths = get_sorted_filepaths_from_folder(params.folder_path, params.file_ext)

    well_number = 0
    for idx, filepath in enumerate(filepaths):
        # Extract well number
        if idx % params.num_wells == 0:
            well_number = 0
        else:
            well_number += 1

        # Extract local timestamp from file
        timestamp = datetime.datetime.fromtimestamp(
            os.path.getmtime(filepath),
            tz=datetime.datetime.now().astimezone().tzinfo
        )

        # Write data into list of dataclass ImageData
        images.append(
            ImageData(
                filepath=filepath,
                well_number=well_number,
                timestamp=timestamp,
                params=params,
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
            image.droplet = Droplet(x=x, y=y, r=r)

    # Check for LLPS
    llps_detector = LLPSDetection()
    for image in images:
        image.droplet.num_edges = llps_detector.number_edges_in_droplet()
        image.droplet.phase_separation = llps_detector.has_phase_separated()

    # Time point of phase separation
    time_point = llps_detector.time_point_of_phase_separation(images, edge_delta=params.edge_delta)

    # Save parameters to JSON for each run
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filepath = f"{timestamp}_params.json"
    params.save(filepath=filepath)

    # Reload parameters from previous run
    previous_parameters = Parameters().load(filepath=filepath)
    print(previous_parameters)
