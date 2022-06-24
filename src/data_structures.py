from __future__ import annotations

import datetime
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

import cv2
import numpy as np

if TYPE_CHECKING:
    from main import Parameters


@dataclass()
class Droplet:
    """ Data about the droplet """
    x: int
    y: int
    r: int
    phase_separation: bool = False
    num_edges: int = None


@dataclass()
class ImageData:
    """ Data about the image """
    filepath: str
    well_number: int
    timestamp: datetime.datetime
    params: Parameters
    # Make list if detecting more than one droplet per well is necessary
    droplet: Droplet = field(default=None)
    # Declare arrays here only if memory is not constrained
    # otherwise lazy load them from disk when needed
    # NOTE: Only use @property if needed, it is approx 40ns slower
    _raw_image: np.ndarray = field(default=None)
    _gray_image: np.ndarray = field(default=None)
    _filtered_image: np.ndarray = field(default=None)

    @property
    def raw_image(self) -> np.ndarray:
        """ Load image from filepath (lazy loading for improved performance) """
        if not isinstance(self._raw_image, np.ndarray):
            self._raw_image = cv2.imread(self.filepath)
        return self._raw_image

    @property
    def gray_image(self) -> np.ndarray:
        """ Convert image to grayscale, can also do additional pre-processing """
        if not isinstance(self._gray_image, np.ndarray):
            self._gray_image = cv2.convertScaleAbs(
                cv2.cvtColor(self.raw_image, cv2.COLOR_BGR2GRAY),
                alpha=self.params.alpha,
                beta=self.params.beta
            )
        return self._gray_image

    @property
    def filtered_image(self) -> np.ndarray:
        if not isinstance(self._filtered_image, np.ndarray):
            raise Exception("Filtered image not set")
        return self._filtered_image

    @filtered_image.setter
    def filtered_image(self, image: np.ndarray):
        """ Checks if the passed data has correct size """
        if image.shape != self.params.image_shape:
            raise ValueError(f"Image sizes don't match {image.size} != {self.params.image_shape}")
        else:
            self._filtered_image = image

    @property
    def adjusted_gray_image(self) -> np.ndarray:
        """ Adjust brightness and contrast """
        # Do something
        return self.gray_image

    @property
    def first_derivative_image(self) -> np.ndarray:
        """ Take first derivative of image """
        scale = self.params.first_derivate_scale
        delta = self.params.first_derivate_delta
        ddepth = cv2.CV_16S

        grad_x = cv2.Sobel(self.gray_image, ddepth, 1, 0, ksize=3, scale=scale, delta=delta,
                           borderType=cv2.BORDER_DEFAULT)
        grad_y = cv2.Sobel(self.gray_image, ddepth, 0, 1, ksize=3, scale=scale, delta=delta,
                           borderType=cv2.BORDER_DEFAULT)

        abs_grad_x = cv2.convertScaleAbs(grad_x)
        abs_grad_y = cv2.convertScaleAbs(grad_y)

        grad = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)

        return grad
