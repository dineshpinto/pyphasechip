import os.path


def get_sorted_filepaths_from_folder(folder_path: str, ext: str) -> list:
    file_paths = []

    for file in os.listdir(folder_path):
        if os.path.splitext(file)[1] == ext:
            file_paths.append(os.path.join(folder_path, file))

    file_paths.sort(key=lambda f: os.path.getmtime(f))

    return file_paths
