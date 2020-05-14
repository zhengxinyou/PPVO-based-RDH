from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator

"""
paper 5 realize
2019.12.06
utils


"""

directions = [(-1, 0), (0, -1), (0, 1), (1, 0), (1, -1), (1, 1), (0, 2), (2, 0), (-1, 2), (2, -1), (2, 1), (1, 2),
              (2, 2)]
direction_length = len(directions)

x_major_locator=MultipleLocator(0.5)
x_major_locator2=MultipleLocator(1000)
y_major_locator=MultipleLocator(1)



def draw_res():
    fig = plt.figure()

    allres = [[[64.22801857727448, 2, 0, 0], [60.60889313481713, 7, 1, 0], [58.6208902687826, 7, 1, 0],
               [57.4031463059863, 7, 1, 0], [55.94571075203925, 17, 1, 0], [54.75935948967159, 7, -1, -1],
               [53.83209455035353, 10, -1, -1], [52.84093437788978, 15, 0, -3]],
              [[66.277184510879, 2, 1, 1], [63.58939675667642, 2, 0, -4], [61.77237074514095, 2, 0, 1],
               [60.239051490140056, 2, 0, 0], [58.96182442384789, 2, 0, -1], [57.77248070400727, 7, 1, 0]],
              [[64.2673153819718, 7, 1, -4], [61.25565442725786, 7, 1, 1], [59.02344470583117, 7, 1, 0],
               [57.171123755175316, 17, 1, 0], [55.60725329299362, 7, -1, -2], [54.534111303650604, 7, -1, -3]],
              [[61.93318110620047, 7, 1, 1], [58.94200958489898, 7, 1, 0], [56.514596993995916, 7, -1, -1],
               [54.500300432457394, 12, -1, -1], [52.74842154418963, 17, -1, -3]]]

    titles = ['Lena','Airplane','Baboon','Barbara','Boat']

    # 1 Lena
    ax1 = fig.add_subplot(111)
    ax1.xaxis.set_major_locator(x_major_locator)
    ax1.yaxis.set_major_locator(y_major_locator)
    ax1.set(xlim=[0.5, 4], ylim=[52, 66], title=titles[0], ylabel='PSNR', xlabel='capacity (*10000)')
    res = allres[0]


    psnr = [i[0] for i in res]
    capacity = [i * 0.5 for i in range(1, len(res)+1)]
    ax1.plot(capacity, psnr, 'bo-', linewidth=2, markersize=8)
    plt.grid()
    plt.show()

    # 2 Airplane
    fig = plt.figure()
    ax2 = fig.add_subplot(111)
    ax2.xaxis.set_major_locator(x_major_locator)
    ax2.yaxis.set_major_locator(y_major_locator)
    ax2.set(xlim=[0.5, 3], ylim=[52, 68], title=titles[1], ylabel='PSNR', xlabel='capacity (*10000)')
    res = allres[1]


    psnr = [i[0] for i in res]
    capacity = [i * 0.5 for i in range(1, len(res)+1)]
    ax2.plot(capacity, psnr, 'bo-', linewidth=2, markersize=8)
    plt.grid()


    plt.show()


    # 3 Baboon
    size3 = np.array([10094,11095,12096,13097])
    psnr3 = [[55.760785,	20, -1, -3],[55.039245,	20 ,-3, -3],[54.354485,	20, -4, -4],[53.811272,	20 ,-5, -5]]
    fig = plt.figure()
    ax3 = fig.add_subplot(111)
    ax3.xaxis.set_major_locator(x_major_locator2)
    ax3.yaxis.set_major_locator(y_major_locator)
    ax3.set(xlim=[5000, 14000], ylim=[51, 60], title=titles[2], ylabel='PSNR', xlabel='capacity ')
    res = psnr3

    psnr = [i[0] for i in res]
    capacity = size3
    ax3.plot(capacity, psnr, 'bo-', linewidth=2, markersize=8)
    plt.grid()

    plt.show()


    # 4 Barbara
    fig = plt.figure()
    ax4 = fig.add_subplot(111)
    ax4.xaxis.set_major_locator(x_major_locator)
    ax4.yaxis.set_major_locator(y_major_locator)
    ax4.set(xlim=[0.5, 3.5], ylim=[52, 66], title=titles[3], ylabel='PSNR', xlabel='capacity (*10000)')
    res = allres[2]

    psnr = [i[0] for i in res]
    capacity = [i * 0.5 for i in range(1, len(res) + 1)]
    ax4.plot(capacity, psnr, 'bo-', linewidth=2, markersize=8)
    plt.grid()

    plt.show()

    # 4 Boat
    fig = plt.figure()
    ax4 = fig.add_subplot(111)
    ax4.xaxis.set_major_locator(x_major_locator)
    ax4.yaxis.set_major_locator(y_major_locator)
    ax4.set(xlim=[0.5, 2.5], ylim=[50, 64], title=titles[4], ylabel='PSNR', xlabel='capacity (*10000)')
    res = allres[3]

    psnr = [i[0] for i in res]
    capacity = [i * 0.5 for i in range(1, len(res) + 1)]
    ax4.plot(capacity, psnr, 'bo-', linewidth=2, markersize=8)
    plt.grid()

    plt.show()



def read_image(img_path):
    i = Image.open(img_path)
    # i.show()
    x = np.array(i, dtype=np.int32)
    return x


def check_in(i, j, k, image_x, image_y):
    """
    check whether a neighbour is in the image or not

    :param image_y:
    :param image_x:
    :param i:
    :param j:
    :param k:
    :return:
    """
    neighbour_i = i + directions[k][0]
    neighbour_j = j + directions[k][1]
    flag = False
    if 0 <= neighbour_i < image_x and 0 <= neighbour_j < image_y:
        flag = True

    return flag, neighbour_i, neighbour_j


def compute_delta(c):
    cave = np.mean(c)
    delta = np.sqrt(np.mean(np.square(c - cave)))
    return delta


def choose_n(theta, delta):
    if delta <= theta * 4 / 13:
        n = 4
    elif delta > theta:
        n = 0
    else:
        n = math.ceil(delta * 13 / theta)
    return n


def get_context(x, i, j, image_x, image_y, theta):
    # get its context
    cur_neighs = list()
    for k in range(direction_length):
        flag, neighbour_x, neighbour_y = check_in(i, j, k, image_x, image_y)
        if flag:
            cur_neighs.append(x[neighbour_x][neighbour_y])



    # determine n
    n = choose_n(theta, compute_delta(cur_neighs))
    if n == 0:
        c = None
    elif n < len(cur_neighs):
        # todo to check before is '>'
        c = cur_neighs[:n]  # change current context
    else:
        c = cur_neighs[:]

    return c


def encode(s):

    s_list = [ ]

    for ch in s:
        bin_ch = bin(ord(ch)).replace('0b', '')
        while len(bin_ch) < 7:
            bin_ch = '0' + bin_ch
        s_list.append(bin_ch)

    return ''.join(s_list)

def decode(s):
    return ''.join([chr(i) for i in [int(s[7*b:7*(b+1)], 2) for b in range(len(s)//7)]])

def compute_psnr(img1, img2, bits=255):
    mse = np.mean(np.square(img1 - img2))
    psnr = 10*np.log10(bits*bits/mse)
    return psnr


def build_auxiliary_information(aux, item, num_item, items_):

    item_str = bin(item).replace('0b','')
    len_bin = len(item_str)

    if items_ == 1 and item_str[0] == '-':

        aux.append(1)
        item_str = item_str[1:]



    head_zeros = num_item - len_bin
    while head_zeros > 0:
        aux.append(0)
        head_zeros -= 1

    for ll in item_str:
        aux.append(int(ll))




def get_auxiliary_information(aux, num_item, item_str,  items_):
    cur = 0
    negative = False
    for i,num in enumerate(num_item):
        if item_str[cur] == '1' and items_[i] == 1:
            bin_item = '0b' + item_str[cur+1: cur + num]
            negative = True
        else:
            bin_item = '0b' + item_str[cur: cur+num]
        cur += num
        item = int(bin_item, 2)
        if negative:

            aux.append(-item)
            negative = False
        else:
            aux.append(item)


def recover_lsb(extract_img, i, j, b):
    origin_lsb = extract_img[i][j]
    bin_origin_lsb = bin(origin_lsb)
    bin_origin_lsb = bin_origin_lsb[:-1] + str(b)

    new_lsb = int(bin_origin_lsb, 2)
    extract_img[i][j] = new_lsb


# auxiliary information (bit length)
def compute_aux_size(lmap):
    num_ST = 1
    num_pe_optimal = 8
    num_theta = 8
    num_end_position_1 = 9
    num_end_position_2 = 9
    num_lm_size = 18
    num_lm_actual_size = 18

    lm_size = len(lmap)

    aux_size = num_ST + num_pe_optimal + num_theta + num_end_position_1 + num_end_position_2 + num_lm_size + num_lm_actual_size + lm_size

    return aux_size


def build_location_map(img, ST):
    location_map = list()

    width, height = img.shape
    for i in range(0, height):
        for j in range(ST, width, 2):
            # print(i,j)
            if img[i][j] == 0 or img[i][j] == 255:
                # print(i, j)
                location_map.append(1)
            elif img[i][j] == 1 or img[i][j] == 254:
                # print(i,j)
                location_map.append(0)


        ST = 1-ST

    # todo compress location map

    return location_map