"""
test
"""

import bpy

def get_image_paths():
    """
    get all the image paths
    """
    image_paths = []
    # get the images and their paths
    # NOTE: note written by admin @ 2017-10-26 04:59:17
    # Make sure they are only tex not screen images and other stuff 
    images = bpy.data.images

    # get the actual path
    for image in images:
        image_path = image.filepath_from_user()
        if image_path and image_path != '':
            print (image_path)
            image_paths.append(image_path)
    return image_paths

def resize_images():
    """resize them to the percentage specified
    """
    # get blender ffmpeg path
    # launch a parallel subprocess to resize them
    # 
    # only shaders ? all images ??
    # have an interface to get the 
    # uniform size or scale
    # if uniform > width height
    # if scale > %
    # exclude images ???
    