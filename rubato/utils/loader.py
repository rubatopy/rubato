"""
util file that helps load things such as images folders etc.
"""
from os import walk, path
from rubato.sprite.image import Image


def import_image_folder(dictionary: dict, rel_path: str):
    """
    Imports a folder of images, creating rubato.Image for each one and
    placing it in a dictionary by its file name.

    Args:
        dictionary: A dictionary that all the images will be written to.
        rel_path: The relative path to the folder you wish to import
    """
    for _, _, files in walk(rel_path):
        # walk to directory path and ignore name and subdirectories
        for image_path in files:
            path_to_image = path.join(rel_path, image_path)
            image = Image({
                "image_location": path_to_image,
            })
            dictionary[image_path.split(".")[0]] = image
