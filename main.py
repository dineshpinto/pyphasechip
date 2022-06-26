import datetime

from parameters import Parameters
from src.data_structures import Droplet
from src.io import get_sorted_filepaths_from_folder, load_images_into_dataclass_list
from src.logic import ImageFilter, LLPSDetection, ShapeDetection

if __name__ == "__main__":
    params = Parameters()

    # Read folder and load each image as an instance of ImageData into a list
    sorted_filepaths = get_sorted_filepaths_from_folder(params.folder_path, params.file_ext)
    images = load_images_into_dataclass_list(sorted_filepaths, params)

    # Run background filter
    image_filter = ImageFilter(params=params)
    for image in images:
        image.filtered_image = image_filter.filter_background(image.gray_image)

    # Run droplet detection
    shape_detector = ShapeDetection(params=params)
    for image in images:
        (x, y, r) = shape_detector.hough_circle_detector(image=image_filter.first_derivative(image.filtered_image))
        if x and y and r:
            image.droplet = Droplet(x=x, y=y, r=r)

    # Check for LLPS
    llps_detector = LLPSDetection(params=params)
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
