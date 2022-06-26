from __future__ import annotations

import datetime
import os.path
from typing import List, TYPE_CHECKING

from data_structures import ImageData

if TYPE_CHECKING:
    from parameters import Parameters


def get_sorted_filepaths_from_folder(folder_path: str, ext: str) -> list:
    file_paths = []

    for file in os.listdir(folder_path):
        if os.path.splitext(file)[1] == ext:
            file_paths.append(os.path.join(folder_path, file))

    file_paths.sort(key=lambda f: os.path.getmtime(f))

    return file_paths


def load_images_into_dataclass_list(sorted_filepaths: list, params: Parameters) -> List[ImageData]:
    images: List[ImageData] = []

    well_number = 0
    for idx, filepath in enumerate(sorted_filepaths):
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
    return images
