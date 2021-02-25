
import time
import cv2
import numpy as np
import math
from PIL import Image
import re

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
