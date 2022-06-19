import datetime
from dataclasses import dataclass, field

import cv2
import numpy as np

from parameters import Parameters


@dataclass()
class Droplet:
    """ Data about the droplet """
    radius: int
    center_x: int
    center_y: int
    phase_separation: bool = False


@dataclass()
class ImageData:
    """ Data about the image """
    filepath: str
    well_number: int
    concentration: float
    timestamp: datetime.datetime
    filtered_image: np.ndarray = field(default=None)
    droplet: Droplet = field(default=None)

    @property
    def raw_image(self) -> np.ndarray:
        """ Load image from filepath (lazy loading for improved performance) """
        return cv2.imread(self.filepath)

    @property
    def gray_image(self) -> np.ndarray:
        """ Convert image to grayscale, can also do additional pre-processing """
        gray = cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2GRAY)
        gray = cv2.convertScaleAbs(gray, alpha=Parameters.convertScaleAbs_alpha, beta=Parameters.convertScaleAbs_beta)
        return gray

    @property
    def adjusted_gray_image(self) -> np.ndarray:
        """ Adjust brightness and contrast """
        return self.gray_image

    @property
    def first_derivative_image(self) -> np.ndarray:
        """ Take first derivative of image """
        scale = Parameters.first_derivate_scale
        delta = Parameters.first_derivate_delta
        ddepth = cv2.CV_16S

        grad_x = cv2.Sobel(self.gray_image, ddepth, 1, 0, ksize=3, scale=scale, delta=delta,
                           borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(self.gray_image, ddepth, 0, 1, ksize=3, scale=scale, delta=delta,
                           borderType=cv2.BORDER_DEFAULT)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad
