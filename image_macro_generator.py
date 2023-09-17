from PIL import Image, ImageFont, ImageDraw
import textwrap

FONT_PATH = r'C:\Windows\Fonts\impact.ttf'
FONT_SIZE = 35
STROKE_WIDTH = 2
FONT_AVE_CHAR_WIDTH = 20
TEXT_MARGINS = 20

def split_macro_text(template_width, text, max_lines=3):
    # Calculate max characters per line, accounting for padding
    max_chars = (template_width - TEXT_MARGINS) // FONT_AVE_CHAR_WIDTH
    return '\n'.join(textwrap.wrap(text, max_chars, max_lines=max_lines))

def generate_macro(template, top_text, bottom_text, max_lines=2):
    image = template.copy()
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    draw = ImageDraw.Draw(image)

    top_text = split_macro_text(image.width, top_text, max_lines)
    bottom_text = split_macro_text(image.width, bottom_text, max_lines)

    # Draw top text
    draw.text((image.width // 2, 0), top_text, font=font, fill=(255, 255, 255), stroke_width=STROKE_WIDTH, stroke_fill=(0, 0, 0), anchor='ma', align='center')

    # Draw bottom text
    draw.text((image.width // 2, image.height), bottom_text, font=font, fill=(255, 255, 255), stroke_width=STROKE_WIDTH, stroke_fill=(0, 0, 0), anchor='md', align='center')

    return image

def main():
    template = Image.open(r'./sample_images/dino-template.jpg')
    generate_macro(template, "THE NIGHT BEFORE, PLACE THINGS YOU DON\'T WANT TO FORGET THE NEXT MORNING...", "CN TOP OF YOUR SHOES").show()

if __name__ == '__main__':
    main()