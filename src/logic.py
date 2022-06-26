from __future__ import annotations

import datetime
from typing import Tuple, List, TYPE_CHECKING

import cv2

if TYPE_CHECKING:
    from data_structures import ImageData
    from parameters import Parameters

import numpy as np


class ShapeDetection:
    def __init__(self, params: Parameters):
        self.params = params

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


class ImageFilter:
    def __init__(self, params: Parameters):
        self.params = params

    def filter_background(self, image: np.ndarray) -> np.ndarray:
        """ Filter image background """
        return image

    def filter_coordinates(self, **kwargs) -> np.ndarray:
        return np.zeros(self.params.image_shape)

    def brightness_adjustment(self, image: np.ndarray) -> np.ndarray:
        brightness = self.params.brightness
        contrast = self.params.contrast
        return image

    def first_derivative(self, image: np.ndarray) -> np.ndarray:
        """ Take first derivative of image """
        scale = self.params.first_derivate_scale
        delta = self.params.first_derivate_delta
        ddepth = cv2.CV_16S

        grad_x = cv2.Sobel(image, ddepth, 1, 0, ksize=3, scale=scale, delta=delta,
                           borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(image, ddepth, 0, 1, ksize=3, scale=scale, delta=delta,
                           borderType=cv2.BORDER_DEFAULT)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad


class LLPSDetection:
    def __init__(self, params: Parameters):
        self.params = params

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
