
import time
import cv2
import numpy as np
import math
from PIL import Image
import re

import functools
import operator

'''matchTemplate Vs regex
conclusion (Final): opencv is more compatible to use
(it can detect monster behind questbar)
but regex is faster than opencv about 2 time'''


def opencvFindSubImage(raw_img, sub_img, threshold=0.95,
                       drawRectangle=True, flip=True):
    def matching(gray_img, sub_img):
        res = cv2.matchTemplate(gray_img, sub_img,
                                cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)
        positionList = []
        w, h = sub_img.shape[::-1]
        for pt in zip(*loc[::-1]):
            positionList.append(pt)
            if drawRectangle is True:
                cv2.rectangle(raw_img, pt, (pt[0] + w, pt[1] + h),
                              (255, 0, 255), 2)
        return positionList
    gray_img = cv2.cvtColor(raw_img, cv2.COLOR_BGR2GRAY)
    gray_sub_img = cv2.cvtColor(sub_img, cv2.COLOR_BGR2GRAY)
    positionList = matching(gray_img, gray_sub_img)
    if flip is True:
        sub_img_fliped = cv2.flip(gray_sub_img, 1)
        positionFlipedList = matching(gray_img, sub_img_fliped)
    else:
        positionFlipedList = []
    return positionList, positionFlipedList


def subimg_location(haystack, needle):
    haystack_str = (str(haystack.tobytes("hex"))[2:])[:-1]\
        .replace('\\n', "")
    needle_str = (str(needle.tobytes("hex"))[2:])[:-1]\
        .replace('\\n', "")
    gap_size = (haystack.size[0]-needle.size[0])*2
    gap_regex = '.{' + str(gap_size) + '}'
    chunk_size = needle.size[0]*2
    split = [needle_str[i:i+chunk_size]
             for i in range(0, len(needle_str), chunk_size)]
    regex = re.escape(split[0])
    for i in range(1, len(split)):
        regex += gap_regex + re.escape(split[i])
    match_list = []
    for match in re.finditer(regex, haystack_str):
        match_list.append(match.start())
    positionList = []
    for x in match_list:
        left = round(haystack.size[0]-1) \
               if round(((x+2)/2) % haystack.size[0])-1 == -1 \
               else round(((x+2)/2) % haystack.size[0])-1
        top = math.ceil((x+2)/2/haystack.size[0])-1
        positionList.append((left, top))
    return positionList


def regexFindSubImage(raw_img, sub_img, drawRectangle=True, flip=True):
    def matching(raw_img, sub_img):
        pil_raw_img = Image.fromarray(cv2.cvtColor(raw_img,
                                                   cv2.COLOR_BGR2GRAY))
        pil_sub_img = Image.fromarray(cv2.cvtColor(sub_img,
                                                   cv2.COLOR_BGR2GRAY))
        positionList = subimg_location(pil_raw_img, pil_sub_img)
        if positionList is not None and drawRectangle is True:
            for x, y in positionList:
                cv2.rectangle(raw_img, (x, y),
                              ((x, y)[0] + pil_sub_img.size[0],
                              (x, y)[1] + pil_sub_img.size[1]),
                              (0, 0, 255), 2)
        return positionList
    positionList = matching(raw_img, sub_img)
    if flip is True:
        sub_img_fliped = cv2.flip(sub_img, 1)
        positionFlipedList = matching(raw_img, sub_img_fliped)
    else:
        positionFlipedList = []
    return positionList, positionFlipedList


def findsubimg(img, sub_img, method="regex", drawRectangle=True, flip=True):
    if method == "regex":
        lst, lstf = opencvFindSubImage(img, sub_img,
                                       drawRectangle=True, flip=True)
    else:
        lst, lstf = regexFindSubImage(img, sub_img,
                                      drawRectangle=True, flip=True)
    return lst, lstf


def list_fast_flat(lst):
    return functools.reduce(operator.iconcat, lst, [])


def character_direction(pos_lst):
    if len(pos_lst[0]) == 0 and len(pos_lst[1]) == 1:
        direction = "right >"
    elif len(pos_lst[0]) == 1 and len(pos_lst[1]) == 0:
        direction = "left <"
    else:
        direction = "no data"
    return direction


def mask_roi(src, pic_lst):
    mask = np.zeros((src.shape[0], src.shape[1]), dtype=np.uint8)
    xoffset = 50
    yoffset = 25
    for pos_lst in pic_lst:
        if pos_lst is not None:
            for pos in pos_lst:
                # print(pos[0],lst)
                x_data = np.array([[[pos[0]-xoffset, pos[1]-yoffset],
                                  [pos[0]-xoffset, pos[1]+yoffset],
                                  [pos[0]+xoffset, pos[1]+yoffset],
                                  [pos[0]+xoffset, pos[1]-yoffset]]],
                                  dtype=np.int32)
                cv2.fillPoly(mask, x_data, 255)

    rescale_img = cv2.bitwise_and(src, src, mask=mask)
    return rescale_img


def quantization(pos_lst, width, height, img=None, color=(0, 255, 0)):
    x_section_num = 10  # 0-9
    y_section_num = 10  # 0-9
    quantize_width = int(width/x_section_num)
    quantize_height = int(height/y_section_num)
    for i in range(len(pos_lst)):
        pos_lst[i] = (pos_lst[i][0] // quantize_width,
                      pos_lst[i][1] // quantize_height)
    if img is not None:
        for i in range(len(pos_lst)):
            x = pos_lst[i][0]*quantize_width
            y = pos_lst[i][1]*quantize_height
            w = quantize_width
            h = quantize_height
            img = cv2.rectangle(img,
                                (x, y), (x+w, y+h), color, 9)
    return pos_lst


def quantization_table_drawing(img, width, height):
    x_section_num = 10  # 0-9
    y_section_num = 10  # 0-9
    quantize_width = int(width/x_section_num)
    quantize_height = int(height/y_section_num)
    for i in range(x_section_num-1):
        cv2.line(img, (int(quantize_width*(i+1)), 0),
                 (int(quantize_width*(i+1)), height), (255, 0, 0), 1)
    for i in range(y_section_num-1):
        cv2.line(img, (0, (int(quantize_height*(i+1)))),
                 (width, (int(quantize_height*(i+1)))), (255, 0, 0), 1)


def main():
    # convert and read 0 not same, should have same src and same method
    sub_img = cv2.imread(r'data\pink_neko.png')

    # sub_img = cv2.imread(r'data\pink_neko.png', 0)
    c = time.time()
    #a = opencvFindSubImage(rescale_img, sub_img)
    d = time.time()

    e = time.time()
    #b = regexFindSubImage(rescale_img, sub_img)
    f = time.time()

    print(d-c, f-e)

if __name__ == '__main__':
    main()
