import numpy as np


class ShapeDetection:
    def __init__(self, **kwargs):
        pass

    def hough_circle_detector(self, **kwargs) -> np.ndarray:
        pass

    def hough_ellipse_detector(self, **kwargs) -> np.ndarray:
        pass


class ImageFilter(ShapeDetection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def filter_background(self, **kwargs) -> np.ndarray:
        pass

    def filter_coordinates(self, **kwargs) -> np.ndarray:
        pass


class LLPSDetection:
    def __init__(self, **kwargs):
        pass

    def has_phase_separated(self, **kwargs) -> np.ndarray:
        pass

    def time_point_of_phase_separation(self) -> float:
        pass
