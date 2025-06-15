import os
import numpy as np
from PIL import Image
import config


def ensure_dirs():
    # Create necessary folders if they don't exist
    os.makedirs(config.ORIGINAL_IMAGES_DIR, exist_ok=True)
    os.makedirs(config.MODIFIED_IMAGES_DIR, exist_ok=True)


def load_image(path):
    # Load image
    try:
        img = Image.open(path)
        return img.convert('RGB') if img.mode != 'RGB' else img
    except FileNotFoundError:
        print(f"Error: '{path}' not found. Place input image in '{config.ORIGINAL_IMAGES_DIR}'.")
        raise
    except Exception as e:
        print(f"Error loading image: {e}")
        raise


def rearrange_vertical_strips(img):
    # Rearrange vertical strips: odd-index strips first, then even-index strips
    arr = np.array(img)
    height, width, channels = arr.shape
    strip_width = width // config.VERTICAL_STRIP_COUNT

    strips = [arr[:, i * strip_width:(i + 1) * strip_width] for i in range(config.VERTICAL_STRIP_COUNT)]
    odd_strips = [strips[i] for i in range(0, config.VERTICAL_STRIP_COUNT, 2)]
    even_strips = [strips[i] for i in range(1, config.VERTICAL_STRIP_COUNT, 2)]

    reordered = np.hstack(odd_strips + even_strips)
    return Image.fromarray(reordered)


def stack_odd_even_horizontal_groups(img):
    # Split image horizontally, stack odd strips vertically, even strips vertically,
    # then place both groups side by side
    arr = np.array(img)
    height, width, channels = arr.shape
    strip_height = height // config.VERTICAL_STRIP_COUNT

    strips = [arr[i * strip_height:(i + 1) * strip_height, :] for i in range(config.VERTICAL_STRIP_COUNT)]
    odd_group = [strips[i] for i in range(0, config.VERTICAL_STRIP_COUNT, 2)]
    even_group = [strips[i] for i in range(1, config.VERTICAL_STRIP_COUNT, 2)]

    odd_stack = np.vstack(odd_group)
    even_stack = np.vstack(even_group)

    final_arr = np.hstack([odd_stack, even_stack])
    return Image.fromarray(final_arr)


def process():
    # Main processing function
    ensure_dirs()

    base_name, ext = os.path.splitext(config.INPUT_IMAGE_NAME)
    input_path = os.path.join(config.ORIGINAL_IMAGES_DIR, config.INPUT_IMAGE_NAME)
    rearranged_path = os.path.join(config.MODIFIED_IMAGES_DIR, f"{base_name}_rearranged{ext}")
    final_path = os.path.join(config.MODIFIED_IMAGES_DIR, f"{base_name}_final{ext}")

    try:
        original = load_image(input_path)
        rearranged = rearrange_vertical_strips(original)
        rearranged.save(rearranged_path, quality=config.JPEG_QUALITY)

        final_img = stack_odd_even_horizontal_groups(rearranged)
        final_img.save(final_path, quality=config.JPEG_QUALITY)

        print("Processing complete. Files saved:")
        print(f" - Rearranged vertical strips: {rearranged_path}")
        print(f" - Final stacked image: {final_path}")

    except Exception as e:
        print(f"Error during processing: {e}")
