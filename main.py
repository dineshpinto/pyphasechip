from src.data_structures import ImageData
from src.logic import ImageFilter, LLPSDetection, ShapeDetection
from typing import List


if __name__ == "main":
    # Read folder and save each image as an instance of ImageData
    images: List[ImageData] = []

    # Run image filter
    image_filter = ImageFilter()
    for image in images:
        image.filtered_image = image_filter.filter_background()

    # Run droplet detection
    shape_detector = ShapeDetection()
    for image in images:
        image.droplet.radius = shape_detector.hough_circle_detector()

    # Check for LLPS
    llps_detector = LLPSDetection()
    for image in images:
        image.droplet.phase_separation = llps_detector.has_phase_separated()
