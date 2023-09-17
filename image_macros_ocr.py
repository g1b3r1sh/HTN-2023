import numpy as np
from PIL import Image, ImageChops, ImageFilter
import pytesseract
import math
import numpy as np

# Convert RGB image to grayscale image where the value for each pixel is the norm of RGB values for normalized to grayscale format
def convert_image_rgb_to_norm(image):
    image_array = np.asarray(image).copy()
    norm_array = np.empty((image_array.shape[0], image_array.shape[1]), dtype=np.int8)
    for i in range(len(image_array)):
        for j in range(len(image_array[i])):
            norm_array[i][j] = np.linalg.norm(image_array[i][j]) / math.sqrt(3*math.pow(255, 2)) * 255
    gs = Image.fromarray(norm_array, mode='L')
    return gs

def filter_for_text_color(image, text_color_filter=lambda p: p > 200):
    # Square values to exaggerate differences
    square_fn = lambda p: (p / 255) ** 2 * 255
    image = image.point(square_fn)

    # Filter for text color pixels
    image = image.point(text_color_filter, mode='1')

    return image

def isolate_image_text(image_path, template_path, white_text=True):
    # Open images using Pillow and remove alpha channel
    image = Image.open(image_path).convert('RGB')
    template = Image.open(template_path).convert('RGB')

    # Set resize size to smaller size between two images
    resize_size = image.size if sum(image.size) <= sum(template.size) else template.size

    # Resize images to same size
    image = image.resize(resize_size)
    template = template.resize(resize_size)

    # Invert color of images if text is black so that text becomes white
    if not white_text:
        image = ImageChops.invert(image)
        template = ImageChops.invert(template)

    # Convert images to norm format
    gs_template = convert_image_rgb_to_norm(template)
    gs_image = convert_image_rgb_to_norm(image)

    # Filter images for text color
    bw_template = filter_for_text_color(gs_template)
    bw_image = filter_for_text_color(gs_image)

    # Keep pixels which are in bw_image and not in bw_template
    text_image = ImageChops.logical_and(bw_image, bw_template.point(lambda p: not p))

    return text_image

# Returns text in tuple (top text, bottom text). If one of the outputs cannot be found, returns empty string in its place.
def extract_top_bottom_text(text_image):
    ocr_data = pytesseract.image_to_data(text_image, output_type=pytesseract.Output.DICT)
    n_rows = len(ocr_data['level'])

    # Group row indices by block
    blocks = []
    for i in range(n_rows):
        if ocr_data['block_num'][i] >= len(blocks):
            blocks.append([])
        blocks[-1].append(i)

    # Generate string represented by each block
    lines = []
    for indices in blocks:
        lines.append(" ".join(ocr_data['text'][i] for i in indices if ocr_data['conf'][i] > 50))

    # Remove empty strings
    lines = list(line.strip() for line in lines if line and not line.isspace())

    if len(lines) < 2:
        print("Warning: Could not find top and bottom text in image")

    return (lines[0] if len(lines) > 0 else "", lines[1] if len(lines) > 1 else "")

EXAMPLE_IMAGE_PATH = r'./sample_images/mallard1.jpg'
EXAMPLE_TEMPLATE_PATH = r'./sample_images/mallard-template.png'
def main():
    text_image = isolate_image_text(EXAMPLE_IMAGE_PATH, EXAMPLE_TEMPLATE_PATH)
    print(extract_top_bottom_text(text_image))

if __name__ == '__main__':
    main()
