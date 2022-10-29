from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from PIL import ImageChops
import numpy as np



def trim(im):
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

# An image generator that takes in two matrices and a string and outputs an image
def image_genA(matrixA, text, matrixB ):
    # Load font, this will crash on linux if you don't have the font installed
    font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf", 32, encoding="unic")
    # Set an arbitrary size for the image, trim() will resize it later
    canvas = Image.new('RGB', (1200, 1200), "white")
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw = ImageDraw.Draw(canvas)
    # Draw the text to the image, increment right to keep up spacing.
    right = 0
    draw.text((right, 5), f'{matrixA}', 'black', font=font)
    right += (len(matrixA) * 36) + 30
    draw.text((right, len(matrixA) * 15), text , 'black', font=font)
    right += (len(text) * 13) + 30
    draw.text((right, 5), f'{matrixB}', 'black', font=font)
    canvas = trim(canvas)
    canvas.save('result.png', 'PNG')


# An image generator that takes a matrix and a string and outputs an image
def image_genB(matrixA, text):
    # Load font, this will crash on linux if you don't have the font installed
    font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf", 32, encoding="unic")
    # Set an arbitrary size for the image, trim() will resize it later
    canvas = Image.new('RGB', (1200, 1200), "white")
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw = ImageDraw.Draw(canvas)
    # Draw the text to the image, increment right to keep up spacing.
    right = 0
    draw.text((right, 5), f'{matrixA}', 'black', font=font)
    right += (len(matrixA) * 36) + 30
    draw.text((right, len(matrixA) * 15), text , 'black', font=font)
    canvas = trim(canvas)
    canvas.save('result.png', 'PNG')


# An image generator that takes in two matrices and a string and outputs an image
def image_genC(matrixA, matrixB, text, matrixC):
    # Load font, this will crash on linux if you don't have the font installed
    font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/Arial.ttf", 32, encoding="unic")
    # Set an arbitrary size for the image, trim() will resize it later
    canvas = Image.new('RGB', (1500, 1500), "white")
    # draw.text((x, y),"Sample Text",(r,g,b))
    draw = ImageDraw.Draw(canvas)
    # Draw the text to the image, increment right to keep up spacing.
    right = 0
    draw.text((right, 5), f'{matrixA} ,', 'black', font=font)
    right += (len(matrixA) * 36) + 30
    draw.text((right, 5), f'{matrixB}' , 'black', font=font)
    right += (len(matrixB) * 18) + 30
    draw.text((right, len(matrixA) * 15), text , 'black', font=font)
    right += (len(text) * 12) + 30
    draw.text((right, 5), f'{matrixC}', 'black', font=font)
    canvas = trim(canvas)
    canvas.save('result.png', 'PNG')