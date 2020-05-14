from Submit import tools

# iii jjj, only for test
def extract_data(c, p, pe_optimal, location_map, location_map_index,iii,jjj):
    #this bug
    c.sort()
    cmax = c[len(c) - 1]
    cmin = c[0]
    cmean = (cmax + cmin) // 2

    b = 0
    find = False

    # location map
    # todo to test
    if location_map_index[0] < len(location_map) and (p == 255 or p == 0):
        if int(location_map[location_map_index[0]]) == 1:
            location_map_index[0] += 1
            # print('-------------------------0--------------------------------------')
            # print(iii,jjj)
            # print("")

            return False, 0, p


    if cmax != cmin:
        # when negative, change pe when cannot discriminate
        if pe_optimal < 0:

            if cmax - abs(pe_optimal) <= cmin + abs(pe_optimal):
                if (cmax - cmin) % 2 == 1:
                    pe_optimal = -((cmax - cmin) // 2)
                else:
                    pe_optimal = -((cmax - cmin) // 2) + 1

                #print(pe_optimal)
        # extract b
        if (p >= cmean + 1 and p - cmax == pe_optimal) or (p <= cmean and cmin - p == pe_optimal):

            b = 0

            find = True
        elif (p >= cmean + 1 and p - cmax == pe_optimal + 1) or (p <= cmean and cmin - p == pe_optimal + 1):
            b = 1

            find = True
        else:
            find = False

        # recover p
        # when p does not change
        if (p >= cmean + 1 and p - cmax <= pe_optimal) or (p <= cmean and cmin - p <= pe_optimal):
            p = p
        # p
        elif p >= cmean + 1 and p - cmax >= pe_optimal + 1:
            p -= 1
        # p
        else:
            p += 1

    else:
        # cmax == cmin
        if (p > cmax and p - (cmax+1) == pe_optimal) or (p <= cmin and cmin - p == pe_optimal):

            b = 0

            find = True
        elif (p > cmax and p - (cmax+1) == pe_optimal + 1) or (p <= cmin and cmin - p == pe_optimal + 1):
            b = 1

            find = True

        if (p > cmax and p - (cmax+1) <= pe_optimal) or (p <= cmin and cmin - p <= pe_optimal):
            p = p
        # p
        elif p > cmax and p - (cmax+1) >= pe_optimal + 1:
            p -= 1
        # p
        else:
            p += 1

    # todo to test
    if location_map_index[0] < len(location_map) and (p == 1 or p == 254):
        # print('-------------------------1--------------------------------------')
        # print(iii, jjj)
        # print("")
        location_map_index[0] += 1

    return find, b, p


def extracting(extract_img, starter):
    # first get information

    image_x, image_y = extract_img.shape



    num_ST = 1
    num_pe_optimal = 8
    num_theta = 8
    num_end_position_1 = 9
    num_end_position_2 = 9
    num_lm_size = 18
    num_lm_actual_size = 18

    aux_size_without_map = num_ST + num_pe_optimal + num_theta + num_end_position_1 + num_end_position_2 + num_lm_size + num_lm_actual_size

    # get info
    info_str = ''
    aux_index = 0
    info_i = 0
    info_j = 0
    for i in range(0, image_x):
        for j in range(starter, image_y, 2):

            if aux_index == aux_size_without_map:
                break
            aux_index += 1
            info_str += bin(extract_img[i][j])[-1]

            if aux_index == aux_size_without_map:
                info_i = i
                info_j = j
                break

        starter = 1 - starter



    # print('info i j')
    # print(info_i, info_j)

    # get auxiliary information
    num_items = [num_ST, num_pe_optimal, num_theta, num_end_position_1, num_end_position_2, num_lm_size, num_lm_actual_size]
    items_ = [0, 1, 2, 0, 0, 0,0]
    aux = list()
    tools.get_auxiliary_information(aux, num_items, info_str, items_)
    # print(aux)
    ST, pe_optimal, theta, end_position_1, end_position_2, lm_size, lm_actual_size = aux
    # print(end_position_1, end_position_2)

    aux_size = aux_size_without_map + lm_size

    '''
    info_i and info_j are the last pos
    get location map
    '''
    lm_size_cnt = lm_size
    location_map = list()
    lm_i = info_i
    lm_j = info_j
    while lm_size_cnt > 0:
        lm_j += 2
        if lm_j > 511:
            lm_j = [0, 1][lm_j == 512]
            lm_i += 1
        location_map.append(bin(extract_img[lm_i][lm_j])[-1])
        lm_size_cnt -= 1

    # todo  decompress location map
    # todo check   the last postion of auxiliary information
    info_i = lm_i
    info_j = lm_j

    location_map_index = [0]
    # print(location_map)
    location_map = location_map[:lm_actual_size]
    location_map.reverse()
    # print(location_map)

    i = end_position_1
    j = end_position_2
    # print("===========================================")
    # print(i , j)

    extract_info = ''

    extract_cnt = 0
    pixels = 0
    while i >= 0:
        while j >= 0:


            c = tools.get_context(extract_img, i, j, image_x, image_y, theta)
            # if i == 214 and j == 398:
            #     print('hhhh')
            if c is None:
                if extract_img[i][j] == 0 or extract_img[i][j] == 1 or extract_img[i][j] == 254 or extract_img[i][j] == 255:
                    location_map_index[0] += 1
                    # print('-------------------------------------------------')
                j -= 2
                continue
            find, b, p = extract_data(c, extract_img[i][j], pe_optimal, location_map, location_map_index,i,j)


            # if i == 181 and j == 459:
            #
            #     print("hhhhhhhhhhhhhh")

            if find:
                # if i > 173:
                #     print('++++++++++++++++++++++')
                #     print(i, j)
                #     print('++++++++++++++++++++++')
                extract_cnt += 1
                if extract_cnt > aux_size:
                    extract_info = str(b) + extract_info
                else:
                    tools.recover_lsb(extract_img, info_i, info_j, b)
                    info_j -= 2
                    if info_j < 0:
                        info_j =  [image_y-1, image_y-2][info_j == -1]
                        info_i -= 1

            extract_img[i][j] = p
            j -= 2
            #print(i, j)
        j = [image_y - 1, image_y - 2][j == -1]
        i -= 1
    # print(extract_cnt)
    return extract_info







