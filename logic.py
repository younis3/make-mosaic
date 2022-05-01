import mosaic
from copy import deepcopy
import sys


# The images mentioned in my program documentary are actually lists of lists
#  as explained in the exercise instructions


def compare_pixel(pixel1, pixel2):
    """This function gets two pixels and returns the distance between them
    """
    # distance between pixels
    dist_btwn_pxls = abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])\
                     + abs(pixel1[2] - pixel2[2])
    return dist_btwn_pxls


def compare(image1, image2):
    """This function gets two images and returns the distance between them
    using compare_pixel function
    """
    min_image_rows = min(len(image1), len(image2))  # minimum num of rows
    min_image_cols = min(len(image1[0]), len(image2[0]))  # minimum num of cols
    dist_sum = 0
    for row in range(min_image_rows):
        for col in range(min_image_cols):
            dist_sum += compare_pixel(image1[row][col], image2[row][col])
    return dist_sum


def get_piece(image, upper_left, size):
    """This function gets the image and return a piece of it by a given size
    (height, width)
    """
    piece = []
    max_row_len = min(size[0], len(image)-upper_left[0])
    max_col_len = min(size[1], len(image[0])-upper_left[1])
    # So that we don't go out of range in the following loop

    for row in range(upper_left[0], upper_left[0] + max_row_len):
        pixel = []
        for col in range(upper_left[1], upper_left[1] + max_col_len):
            pixel.append(image[row][col])
        piece.append(pixel)  # add the pixel to the image (piece)
    return piece


def set_piece(image, upper_left, piece):
    """This function gets the original image (in this program it gets a deep
    copy of the original image) and sets the piece's pixels in this image
    """
    max_row_len = min(len(image)-upper_left[0], len(piece))
    max_col_len = min(len(image[0])-upper_left[1], len(piece[0]))
    # So that we don't go out of range in the following loop

    for row in range(upper_left[0], upper_left[0] + max_row_len):
        for col in range(upper_left[1], upper_left[1] + max_col_len):
            # the following line sets the piece's pixels in the image
            image[row][col] = piece[row-upper_left[0]][col-upper_left[1]]


def average(image):
    """This function gets an image and returns the averages of its rgb
    colors in matching tuple (red average, green average, blue average)
    """
    sum_red = 0
    sum_green = 0
    sum_blue = 0
    pixel_count = 0  # pixel count always over 0 so we can't divide by zero
    for row in range(len(image)):
        for col in range(len(image[0])):
            pixel_count += 1
            sum_red += image[row][col][0]
            sum_green += image[row][col][1]
            sum_blue += image[row][col][2]
    # The following lines calculate the average of the RGB colors
    avr_red = sum_red / pixel_count
    avr_green = sum_green / pixel_count
    avr_blue = sum_blue / pixel_count
    return avr_red, avr_green, avr_blue  # RGB averages tuple


def preprocess_tiles(tiles):
    """This function gets the list of tiles and returns a list of averages so
    that every average index in this list matches the index of the tile of
    that average
    """
    avg_lst = []
    for tile in range(len(tiles)):
        avg = average(tiles[tile])
        avg_lst.append(avg)  # adds the average to average list
    return avg_lst


def get_best_tiles(objective, tiles, averages, num_candidates):
    """This function returns a list of the best tiles that their color average
    is the closest to the objective image's color average.
    best tiles list's length is equal to num_candidates.
    """
    objective_avg = average(objective)
    compare_avg_lst = []
    best_tiles_lst = []
    for idx_average in range(len(averages)):
        compare_avg_lst.append(compare_pixel(averages[idx_average],
                                             objective_avg))
    # now we have compare_avg_lst that has all the distances of all averages
    #  compared to the objective average
    # compare_avg_lst matches averages and tiles lists in indexes

    for idx_candidate in range(num_candidates):
        candidate_index = compare_avg_lst.index(min(compare_avg_lst))
        best_tiles_lst.append(tiles[candidate_index])
        compare_avg_lst[candidate_index] = 766  # this random large
        # number replaces the value of the candidate distance in
        #  compare_avg_lst to the a value that can never be chosen again
        #   (like removing an item from list but i still want to keep the
        #    indexes sorted as before to match the other lists)
    return best_tiles_lst


def choose_tile(piece, tiles):
    """This function chooses the closest tile to the image we want to replace
    by comparing the distance between the two images using the compare function
    """
    compare_tiles_lst = []
    for tile in range(len(tiles)):
        compare_tiles_lst.append(compare(tiles[tile], piece))

    # the following line gets the same index in tiles list that matches the
    #  index of the minimum distance of piece
    min_dist_indix = compare_tiles_lst.index(min(compare_tiles_lst))
    tile = tiles[min_dist_indix]  # choosing the tile
    return tile


def make_mosaic(image, tiles, num_candidates):
    """This function use the previous functions in order to make and return
    the final photomosaic image
    """
    mosaic_img = deepcopy(image)  # creates a deepcopy of the original image
    # mosaic_img is the image we want to be replaced by the matching best tiles

    img_height = len(mosaic_img)
    img_width = len(mosaic_img[0])
    tile_height = len(tiles[0])
    tile_width = len(tiles[0][0])
    tiles_averages = preprocess_tiles(tiles)  # gets the averages of the tiles

    for row in range(0, img_height, tile_height):  # all tiles same size
        for col in range(0, img_width, tile_width):
            upper_left = row, col
            orginal_image_piece = get_piece(mosaic_img, upper_left,
                                            size=(tile_height, tile_width))
            best_tiles = get_best_tiles(orginal_image_piece, tiles,
                                        tiles_averages, num_candidates)
            chosen_tile = choose_tile(orginal_image_piece, best_tiles)
            set_piece(mosaic_img, upper_left, chosen_tile)

    return mosaic_img  # return the final result of the photomosaic image


NUMBER_OF_ARGUMENTS = 5


if __name__ == "__main__":
    """The main function of the program that load an image, make a mosaic of it
    then save it.
    """
    if len(sys.argv) == NUMBER_OF_ARGUMENTS+1:
        script_name = sys.argv[0]
        image_source = sys.argv[1]
        images_dir = sys.argv[2]
        output_name = sys.argv[3]
        tile_height = int(sys.argv[4])
        num_candidates = int(sys.argv[5])

        loaded_image = mosaic.load_image(image_source)  # LOAD
        tiles = mosaic.build_tile_base(images_dir, int(tile_height))
        mosaic_result = make_mosaic(loaded_image, tiles, num_candidates)
        mosaic.save(mosaic_result, output_name)  # SAVE

    else:  # wrong arguments input
        print("Wrong number of parameters. The correct usage is:\n"
              "ex6.py <image_source> <images_dir><output_name> \n"
              "<tile_height> <num_candidates>")
