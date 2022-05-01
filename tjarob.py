import mosaic
from PIL import Image
import os, sys
import Image
import logic
from copy import deepcopy
import sys

im = Image.open("im1.jpg")
pix = im.load()
#print(pix[1919, 1199])

def compare_pixel(pixel1, pixel2):
    # distance between pixels
    dist_btwn_pxls = abs(pixel1[0] - pixel2[0]) + abs(pixel1[1] - pixel2[1])\
                     + abs(pixel1[2] - pixel2[2])
    return dist_btwn_pxls

def compare(image1, image2):
    min_image_rows = min(len(image1), len(image2))  # minimum num of rows
    min_image_cols = min(len(image1[0]), len(image2[0]))  # minimum num of cols
    dist_sum = 0
    for row in range(min_image_rows):
        for col in range(min_image_cols):
            dist_sum += compare_pixel(image1[row][col], image2[row][col])
    return dist_sum

"""
image0 = [[(255, 255, 255), (100, 20, 10)],
          [(255, 255, 255), (255, 255, 255)],
          [(0, 0, 0), (255, 255, 255)]]


#mosaic.show(image0)

print("image0 cols ", len(image0[0]))  # cols
print("image0 rows ", len(image0))    # rows




image1 = [[(255, 255, 255), (255, 255, 255), (255, 255, 255)]]



#mosaic.show(image1)
print("image1 cols ", len(image1[0]))  # cols
print("image1 rows ", len(image1))    # rows
"""

### tjrbe function 3 (get_piece)
########################################
image_original = [[(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255)],
                  [(255, 255, 255), (0, 255, 0), (255, 0, 0), (255, 0, 0)],
                  [(255, 255, 255), (0, 255, 0), (255, 0, 0), (255, 0, 0)]]

#print("image_original cols ", len(image_original[0]))  # cols
#print("image_original rows ", len(image_original))    # rows
#mosaic.show(image_original)


def get_piece(image, upper_left, size):
    piece = []
    max_row_len = min(size[0], len(image)-upper_left[0])
    max_col_len = min(size[1], len(image[0])-upper_left[1])
    for row in range(upper_left[0], upper_left[0] + max_row_len):
        pixel = []
        for col in range(upper_left[1], upper_left[1] + max_col_len):
            pixel.append(image[row][col])
        piece.append(pixel)
    return piece

#new_piece_image = get_piece(image_original, upper_left=(1, 1), size=(2,3))
#mosaic.show(new_piece_image)
#print(new_piece_image)
#print(image_original)
##########################################


### tjrbe function 4 (set_piece)
########################################


def set_piece(image, upper_left, piece):
    max_row_len = min(len(image)-upper_left[0], len(piece))
    max_col_len = min(len(image[0])-upper_left[1], len(piece[0]))
    for row in range(upper_left[0], upper_left[0] + max_row_len):
        for col in range(upper_left[1], upper_left[1] + max_col_len):
            image[row][col] = piece[row-upper_left[0]][col-upper_left[1]]
    return image


image_test = [[(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),(255, 255, 255)],
              [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255,255),(255, 255, 255)],
              [(255, 255, 255), (255, 255, 255), (255, 255, 255), (255, 255, 255),(255, 255, 255)]]
#print("image_test cols ", len(image_test[0]))  # cols
#print("image_test rows ", len(image_test))    # rows


piece_test = [[(0, 255, 0), (0, 255, 0), (0, 255, 0)],
              [(0, 255, 0), (0, 255, 0), (0, 255, 0)]]

#x= deepcopy(piece_test)
#x[0]=[(0, 0, 0), (0, 0, 0), (0, 0, 0)]
#print(piece_test)
#print(x)

#print("piece_test cols ", len(piece_test[0]))  # cols
#print("piece_test rows ", len(piece_test))    # rows

#upper_left=  (1,2)
#image_changed = set_piece(image_test, upper_left, piece_test)

#mosaic.show(image_changed)

##########################################


def average(image):
    sum_red = 0
    sum_green = 0
    sum_blue = 0
    pixel_count = 0
    for row in range(len(image)):
        for col in range(len(image[0])):
            pixel_count += 1
            sum_red += image[row][col][0]
            sum_green += image[row][col][1]
            sum_blue += image[row][col][2]
    avr_red = sum_red / pixel_count
    avr_green = sum_green / pixel_count
    avr_blue = sum_blue / pixel_count
    return avr_red, avr_green, avr_blue

#print(average(piece_test))
#print(average(image_test))
#print(average(image_original))

def preprocess_tiles(tiles):
    avg_lst = []
    for tile in range(len(tiles)):
        avg = average(tiles[tile])
        avg_lst.append(avg)
    return avg_lst
#print(preprocess_tiles(tiles=[image_original]))
averages = preprocess_tiles(tiles=[piece_test, image_test])
#print(averages)

#######


def get_best_tiles(objective, tiles, averages , num_candidates):

    # assuming every item in tiles and averages lists matches each other as
    #  done in preprocess_tiles function

    # **************** et2kd mn elmola7da hay eda tiles w averages mrtbat zy
    #  b3d wela lazim nst3ml preprocess_tiles function ??

    objective_avg = average(objective)
    #print(objective)
    #print(objective_avg)
    #print(averages)
    compare_avg_lst = []
    best_tiles_lst = []
    for idx_average in range(len(averages)):
        compare_avg_lst.append(compare_pixel(averages[idx_average],
                                             objective_avg))
    # now we have compare_avg_lst that has all the distances of all averages
    #  compared to the objective average
    # compare_avg_lst matches averages and tiles lists in indexes

    #print(compare_avg_lst)

    for idx_candidate in range(num_candidates):
        candidate_index = compare_avg_lst.index(min(compare_avg_lst))
        best_tiles_lst.append(tiles[candidate_index])
        compare_avg_lst[candidate_index] = 766  # this replaces the value of
        # the candidate distance in compare_avg_lst to the a value that can
        #  never be chosen again (like removing an item from list but i
        #   still want to keep the indexes sorted as before to match the
        #    other lists)

    return best_tiles_lst


def choose_tile(piece, tiles):
    compare_tiles_lst = []
    for tile in range(len(tiles)):
        compare_tiles_lst.append(compare(tiles[tile], piece))

    # the following line gets the same index in tiles list that matches the
    #  index of the minimum distance of piece
    min_dist_indix = compare_tiles_lst.index(min(compare_tiles_lst))
    tile = tiles[min_dist_indix]
    return tile


def make_mosaic(image, tiles, num_candidates):
    mosaic_img = deepcopy(image)
    img_height = len(mosaic_img)
    img_width = len(mosaic_img[0])
    tile_height = len(tiles[0])
    tile_width = len(tiles[0][0])
    tiles_averages = preprocess_tiles(tiles)

    for row in range(0, img_height, tile_height):  # assuming all tiles same size
        for col in range(0, img_width, tile_width):
            upper_left = mosaic_img[row][col]
            orginal_image_piece = get_piece(mosaic_img, upper_left,
                                            size=(tile_height, tile_width))
            best_tiles = get_best_tiles(orginal_image_piece, tiles,
                                        tiles_averages, num_candidates)
            chosen_tile = choose_tile(orginal_image_piece, best_tiles)
            set_piece(orginal_image_piece, upper_left, chosen_tile)
    return mosaic_img


NUMBER_OF_ARGUMENTS = 5

if __name__ == "__main__":
    if len(sys.argv) == NUMBER_OF_ARGUMENTS+1:
        script_name = sys.argv[0]
        image_source = sys.argv[1]
        images_dir = sys.argv[2]
        output_name = sys.argv[3]
        tile_height = int(sys.argv[4])
        num_candidates = int(sys.argv[5])

        loaded_image = mosaic.load_image(image_source)
        tiles = mosaic.build_tile_base(images_dir, tile_height)
        mosaic_result = make_mosaic(loaded_image, tiles, num_candidates)
        mosaic.save(mosaic_result, output_name)

    else:
        print("message = msh hek el usage")




"""
def get_best_tiles(objective, tiles, averages , num_candidates):
    #averages_lst = averages  # copy averages to new list
    #best_tiles_lst = [0]*num_candidates
    candidate_lst = []
    best_tiles_lst = []
    objective_avg = average(objective)
    for idx_candidate in range(num_candidates):
        candidate = closest(averages_lst, objective_avg)

    # now we have candidate list contains averages

    return best_tiles_lst
"""


print(get_best_tiles(image_original, tiles=[piece_test, image_test],
                     averages=averages, num_candidates=2))



"""
def compare(image0, image1):
    max_image_rows = min(len(image0), len(image1))  # number of rows
    max_image_cols = min(len(image0[0]), len(image1[0]))  # number of cols


    dist_sum = 0
    for row in range(max_image_rows):
        for col in range(max_image_cols):
            dist_sum += logic.compare_pixel(image0[row][col], image1[row][col])
            print(dist_sum)
    return dist_sum

compare(image0, image1)
"""


############################################

