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

def extract_text(image_path, template_path, white_text=True):
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

    # Get text from image
    print(pytesseract.image_to_string(text_image))
    text_image.show()

def main():
    extract_text(r'./sample_images/dino2.png', r'./sample_images/dino-template.jpg')

if __name__ == '__main__':
    main()
