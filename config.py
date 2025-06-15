import os

# Base directory of the project (root folder)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input and output directories relative to BASE_DIR
ORIGINAL_IMAGES_DIR = os.path.join(BASE_DIR, "images", "original_images")
MODIFIED_IMAGES_DIR = os.path.join(BASE_DIR, "images", "modified_images")

# Input image filename
INPUT_IMAGE_NAME = "smurf.jpg"

# Image manipulation constants
VERTICAL_STRIP_COUNT = 30      # Number of vertical strips to split image into

# JPEG save quality (1-100)
JPEG_QUALITY = 90
