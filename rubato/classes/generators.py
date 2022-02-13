# @staticmethod
# def import_image_folder(dictionary: dict, rel_path: str):
#     """
#     Imports a folder of images, creating rubato.Image for each one and
#     placing it in a dictionary by its file name.

#     Args:
#         dictionary: A dictionary that all the images will be written to.
#         rel_path: The relative path to the folder you wish to import
#     """
#     for _, _, files in walk(rel_path):
#         # walk to directory path and ignore name and subdirectories
#         for image_path in files:
#             path_to_image = path.join(rel_path, image_path)
#             image = Image({
#                 "image_location": path_to_image,
#             })
#             dictionary[image_path.split(".")[0]] = image

# @staticmethod
# def import_animation_folder(rel_path: str) -> list:
#     """
#     Imports a folder of images, creating rubato.Image for each one and
#     placing it in a list by order in directory. Directory must be
#     solely comprised of images.

#     Args:
#         rel_path: The relative path to the folder you wish to import

#     Returns:
#         list: a list of rubato.Image s. Filled with all images in
#         given directory.
#     """
#     ret_list = []
#     for _, _, files in walk(rel_path):
#         # walk to directory path and ignore name and subdirectories
#         for image_path in files:
#             path_to_image = path.join(rel_path, image_path)
#             image = Image({
#                 "image_location": path_to_image,
#             })
#             ret_list.append(image)
#     return ret_list
