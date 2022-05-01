import os
from PIL import Image

def pil_image_from_lists(image_as_lists):
    """ Generate an Image obj from list of lists """
    height = len(image_as_lists)
    width = min([len(image_as_lists[i]) for i in range(height)])
    im = Image.new("RGB", (width, height))
    for i in range(width):
        for j in range(height):
            im.putpixel((i, j), image_as_lists[j][i])
    return im


def lists_from_pil_image(image):
    """ Turn an Image obj to a list of lists """
    width, height = image.size
    pixels = list(image.getdata())
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]
    return pixels


def build_tile_base(tiles_dir, tile_height):
    """ Create a list of images(as list of lists) from the images found in
    tiles_dir, resized such that all the images in the list are of equal
    size, with the height being tile_height """
    tiles = []
    widths = []
    for file in os.listdir(tiles_dir):
        try:
            img = Image.open(os.path.join(tiles_dir, file) )
            if img.mode != 'RGB':
                img = img.convert(mode = 'RGB')
            img_ratio = img.size[0] / img.size[1]
            img = img.resize( (int(img_ratio*tile_height), tile_height), Image.ANTIALIAS)
            tiles.append(lists_from_pil_image(img))
            widths.append(img.size[0])
        except IOError:
            pass
    #now alligning the tiles by cropping to same width
    min_width = min(widths)
    cropped_tiles = []

    for tile in tiles:
        cropped = []
        for row in range(tile_height):
            new_row = tile[row][:min_width]
            cropped += [new_row]
        cropped_tiles += [cropped]

    return cropped_tiles


def load_image(image_filename):
    """  load an image from an image file and return it as a list of lists """
    img = Image.open(image_filename)
    image = lists_from_pil_image(img)
    return image


def save(image, filename):
    """ save an image (as list of lists) to a file """

    mosaic = pil_image_from_lists(image)
    output_dir = os.path.dirname(filename)

    if os.path.exists(filename):
        print("Error: can not save to file: ", filename, ". File already exists.")
        return
    if output_dir != "" and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    mosaic.save(filename)


def show(image):
    """ display an image (as list of lists) """
    mosaic = pil_image_from_lists(image)
    mosaic.show()




