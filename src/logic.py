from __future__ import annotations

import datetime
from typing import Tuple, List, TYPE_CHECKING

if TYPE_CHECKING:
    from data_structures import ImageData

import numpy as np


class ShapeDetection:
    def __init__(self, **kwargs):
        pass

    def hough_circle_detector(self, image: np.ndarray, **kwargs) -> Tuple[int, int, int]:
        """ Detect circle and return (x, y, r) """
        circle_found = True
        if circle_found:
            x, y, r = 1, 1, 1
            return x, y, r
        else:
            return 0, 0, 0

    def hough_ellipse_detector(self, image: np.ndarray, **kwargs) -> Tuple[int, int, int, int]:
        """ Detect circle and return (x, y, r0, r1) """
        pass


class ImageFilter(ShapeDetection):
    def __init__(self, image_shape: Tuple[int, int], **kwargs):
        super().__init__(**kwargs)
        self.image_shape = image_shape

    def filter_background(self, **kwargs) -> np.ndarray:
        return np.zeros(self.image_shape)

    def filter_coordinates(self, **kwargs) -> np.ndarray:
        pass


class LLPSDetection:
    def __init__(self, **kwargs):
        pass

    def has_phase_separated(self, **kwargs) -> bool:
        pass

    def number_edges_in_droplet(self, **kwargs) -> int:
        pass

    @staticmethod
    def time_point_of_phase_separation(images: List[ImageData], edge_delta: float) -> datetime.datetime:
        time_point = None
        for idx in range(len(images) - 1):
            if (images[idx + 1].droplet.num_edges - images[idx].droplet.num_edges) > edge_delta:
                time_point = images[idx + 1].timestamp
                break
        return time_point
