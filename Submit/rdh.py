import numpy as np
from Submit import tools


def compute_pe(p, c):
    """

    :param p: current pixel
    :param c: context vector c
    :return: predict value
    """
    c.sort()
    cmin = c[0]
    cmax = c[len(c) - 1]
    # predict_value = 0
    # predict_error = 0

    if cmin != cmax:
        if p >= (cmax + cmin) // 2 + 1:
            predict_value = cmax
            predict_error = p - predict_value
        else:
            predict_value = cmin
            predict_error = predict_value - p

    else:

        if p >= cmax + 1:
            predict_value = cmax + 1
            predict_error = p - predict_value
        else:
            predict_value = cmin
            predict_error = predict_value - p

    return predict_value, predict_error


def compute_p_image(c, p, pe_optimal, pe, cur_embed_index, to_embed_binary_message):
    """

    :param c:
    :param p:
    :param pe_optimal:
    :param pe:
    :param cur_embed_index:
    :param to_embed_binary_message:
    :return:
    """
    cmax = c[len(c) - 1]
    cmin = c[0]
    insert = False

    p_ori = p

    if cmax != cmin:
        #  when cmax != cmin
        if pe_optimal >= 0:
            # when pe_optimal is postive, compute p_image
            if p >= cmax:
                if pe == pe_optimal:
                    p += int(to_embed_binary_message[cur_embed_index[0]])
                    cur_embed_index[0] += 1
                    insert = True
                elif pe > pe_optimal:
                    p += 1
            elif p <= cmin:
                if pe == pe_optimal:
                    p -= int(to_embed_binary_message[cur_embed_index[0]])
                    cur_embed_index[0] += 1
                    insert = True
                elif pe > pe_optimal:
                    p -= 1
        else:
            # when pe_optimal is negitive, compute p_image
            # in this case, we need to change pe_optimal (when cause intersection) at first
            if cmax - abs(pe_optimal) <= cmin + abs(pe_optimal):
                if (cmax - cmin) % 2 == 1:
                    pe_optimal = -((cmax - cmin) // 2)
                else:
                    pe_optimal = -((cmax - cmin) // 2) + 1
                # print(pe_optimal)

            if p >= (cmax + cmin) // 2 + 1:
                if pe == pe_optimal:
                    p += int(to_embed_binary_message[cur_embed_index[0]])
                    cur_embed_index[0] += 1
                    insert = True
                elif pe > pe_optimal:
                    p += 1
            elif p <= (cmax + cmin) // 2:
                if pe == pe_optimal:
                    p -= int(to_embed_binary_message[cur_embed_index[0]])
                    cur_embed_index[0] += 1
                    insert = True
                elif pe > pe_optimal:
                    p -= 1
    else:
        # when cmax == cmin
        # print('hihihi')
        # print(pe)

        if p >= cmax + 1:
            if pe == pe_optimal:
                p += int(to_embed_binary_message[cur_embed_index[0]])
                cur_embed_index[0] += 1
                print('here!')
                insert = True
            elif pe > pe_optimal:
                p += 1
        elif p <= cmin:
            if pe == pe_optimal:
                p -= int(to_embed_binary_message[cur_embed_index[0]])
                cur_embed_index[0] += 1
                print('here!')
                insert = True
            elif pe > pe_optimal:
                p -= 1
    # todo test
    # if not insert:
    #     print('p_ori', p_ori)
    #     print('pe',pe)
    #     print('pe_optimal',pe_optimal)
    #     print('c',c)
    #     print("")

    return p, insert


def embedding(x, image_x, image_y, ST, pe_optimal, theta, lmap, to_embed_binary_message, cur_embed_index, stflag):
    """
   :param x:
   :param image_x:
   :param image_y:
   :param theta:
   :param pe_optimal:
   :param to_embed_binary_message:
   :param cur_embed_index:
   :return:

   head form:  53 + lm_size bits
   ST 1
   pe_optimal bin 8
   theta 8
   end position 18
   lm_size 18
   lm lm_size
   """
    end_position = 0

    new_x = x.copy()
    starter = ST % 2

    num_ST = 1
    num_pe_optimal = 8
    num_theta = 8
    num_end_position_1 = 9
    num_end_position_2 = 9
    num_lm_size = 18
    num_lm_actual_size = 18

    lm_size = len(lmap)

    aux_size = num_ST + num_pe_optimal + num_theta + num_end_position_1 + num_end_position_2 + num_lm_size + num_lm_actual_size + lm_size
    aux_cnt = 0
    i_end = 0
    j_end = 0

    # todo add
    lmap_cnt = 0

    enough = False
    pixels = 0
    insert_cnt = 0
    for i in range(0, image_x):
        for j in range(starter, image_y, 2):

            # print(cur_embed_index[0])
            # if all the message has been embedded
            if cur_embed_index[0] == len(to_embed_binary_message):
                break

            if new_x[i][j] == 0 or new_x[i][j] == 1 or new_x[i][j] == 254 or new_x[i][j] == 255:
                lmap_cnt += 1

            pixels += 1
            # just skip when encounter 0 or 255 because of overflow or underflow
            if x[i][j] == 0 or x[i][j] == 255:
                if aux_cnt < aux_size:
                    to_embed_binary_message.append(bin(new_x[i][j])[-1])
                    aux_cnt += 1

                continue

            # to get its adaptive context
            c = tools.get_context(new_x, i, j, image_x, image_y, theta)
            if c is None:
                if aux_cnt < aux_size:
                    to_embed_binary_message.append(bin(new_x[i][j])[-1])
                    aux_cnt += 1
                continue

            # if i == 396 and j == 487:
            #     print('hhhh')

            #  according its context to compute  and get p_predict
            p = new_x[i][j]
            p_predict, pe = compute_pe(p, c)

            #  embed
            p_image, insert = compute_p_image(c, p, pe_optimal, pe, cur_embed_index, to_embed_binary_message)
            if insert:
                insert_cnt += 1
                # print(i,j)

            # if i == 175 and j == 415:
            #     print('==========================================')
            #     print(new_x[175][415])
            new_x[i][j] = p_image
            # if i == 175 and j == 415:
            #
            #     print(new_x[175][415])
            #     print('==========================================')

            # push first |aux| LSBs to the end
            # todo remember i have convert string to list      list()

            if aux_cnt < aux_size:
                to_embed_binary_message.append(bin(new_x[i][j])[-1])
                aux_cnt += 1

            if cur_embed_index[0] == len(to_embed_binary_message):

                if not enough:
                    i_end = i
                    j_end = j
                    enough = True
                break

        # chess
        starter = 1 - starter

    # here we assume even
    if not enough:
        i_end = image_x - 1
        j_end = image_y - 1 - (ST % 2)

    # print(i_end, j_end)
    # print('-------------------insert cnt')
    # print(insert_cnt)

    # build auxiliary info
    num_items = [num_ST, num_pe_optimal, num_theta, num_end_position_1, num_end_position_2, num_lm_size,
                 num_lm_actual_size]



    items = [stflag, pe_optimal, theta, i_end, j_end, lm_size, lmap_cnt]

    items_ = [0, 1, 2, 0, 0, 0, 0]
    aux = list()
    for index in range(7):
        tools.build_auxiliary_information(aux, items[index], num_items[index], items_[index])

    # todo lm
    for lm_item in lmap:
        aux.append(lm_item)

    # replace LSB
    replace_index = 0
    for i in range(0, image_x):
        for j in range(starter, image_y, 2):
            if replace_index == aux_cnt:
                break

            # new lsb
            to_replace_lsb = aux[replace_index]
            # change
            origin_lsb = new_x[i][j]
            bin_origin_lsb = bin(origin_lsb)
            bin_origin_lsb = bin_origin_lsb[:-1] + str(to_replace_lsb)
            new_lsb = int(bin_origin_lsb, 2)
            new_x[i][j] = new_lsb
            # replace one
            replace_index += 1

        starter = 1 - starter

    # todo  change return value

    # print('embed pixels %d' % pixels)
    return new_x, enough




