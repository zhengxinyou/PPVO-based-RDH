import numpy as np
from Submit import tools
from Submit import rdh
from Submit import extract
import sys
from PIL import Image

def embed_extract(origin_img, to_embed_info, pe_1, theta_1, pe_2):

    # to embed message

    psnr = 0

    image_x, image_y = origin_img.shape

    ST = 0
    pe_optimal = pe_1
    theta = theta_1

    lmap = tools.build_location_map(origin_img, 0)

    to_embed_binary_message = tools.encode(to_embed_info)
    to_embed_binary_message = list(to_embed_binary_message)

    cur_embed_index = [0]

    # embed
    extract_img, enough = rdh.embedding(origin_img, image_x, image_y,
                                        ST, pe_optimal, theta, lmap,
                                        to_embed_binary_message, cur_embed_index, 0)
    print(len(to_embed_binary_message))

    if enough:
        # just embed once
        # extract
        print('only use embedding one time')
        to_extract_img = extract_img.copy()
        psnr = tools.compute_psnr(origin_img, extract_img)

        return True, to_extract_img, psnr, 1

    else:
        # embed twice
        print('one stage not enough')
        # stage 1 capacity
        print('stage 1 capacity: %d' % cur_embed_index[0])
        stage_capacity_1 = cur_embed_index[0]
        aux_len_1 = tools.compute_aux_size(lmap)

        to_embed_info = tools.encode(to_embed_info)

        cur_embed_index_1 = [0]
        to_embed_binary_message_1 = list(to_embed_info[:stage_capacity_1-aux_len_1])

        cur_embed_index_2 = [0]
        to_embed_binary_message_2 = list(to_embed_info[stage_capacity_1 - aux_len_1:])

        ST2 = 1
        pe_optimal_2 = pe_2
        theta_2 = theta_1

        embed_once_img, enough = rdh.embedding(origin_img, image_x, image_y, ST, pe_optimal, theta, lmap,
                                            to_embed_binary_message_1, cur_embed_index_1,
                                               1)

        embed_once_img_ = embed_once_img.copy()

        lmap_2 = tools.build_location_map(embed_once_img_, 1)

        embed_twice_img, enough2 = rdh.embedding(embed_once_img_, image_x, image_y, ST2, pe_optimal_2, theta_2, lmap_2,
                                               to_embed_binary_message_2, cur_embed_index_2,
                                                 1)

        print('stage 1 capacity: %d' % cur_embed_index_1[0])
        print('stage 2 capacity: %d' % cur_embed_index_2[0])
        print('all %d' % (cur_embed_index_1[0] + cur_embed_index_2[0]))

        if enough2:
            embed_twice_img_ = embed_twice_img.copy()
            psnr = tools.compute_psnr(origin_img, embed_twice_img)

            return True, embed_twice_img_, psnr, 2

        else:
            return False, None, None, 0




def embed_main(origin_img, p1, p2, theta, embed_info):
    # to_embed_info = 2 * 'hello world  hhhhhhhhhhhhhhhhhhhhhhhh yzx yzx 2020 2020 01234567890123456789asdfghjkl01234567890123456789asdfghjkl01234567890123456789asdfghjkl'

    embed_success, extract_img, psnr, embed_stages = embed_extract(origin_img, embed_info, p1, theta, p2)

    return embed_success, extract_img, psnr, embed_stages



def extract_main(extract_img):
    to_extract_img = extract_img.copy()

    img_first = to_extract_img[0][0]
    bin_lsb = bin(img_first)
    if bin_lsb[-1] == '0':
        info = extract.extracting(to_extract_img, 0)
    else:
        info2 = extract.extracting(to_extract_img, 1)
        info1 = extract.extracting(to_extract_img, 0)
        info = info1+info2

    return info, to_extract_img





def test():
    img_path = '../test_img/'
    for i in range(1,7):
        origin_img = tools.read_image(img_path + str(i) + '.bmp')
        #print(origin_img.shape)
        height,width = origin_img.shape
        cnt = 0
        for j in range(height):
            for k in range(width):
                if origin_img[j][k] == 255 or origin_img[j][k] == 0 or origin_img[j][k] == 254 or origin_img[j][k] == 1:
                    cnt += 1
                    # print(origin_img[j][k])
                    # print(j,k)

        print(i)
        print(cnt)
        print("")


