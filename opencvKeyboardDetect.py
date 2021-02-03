import cv2
import numpy


def waitKeyFunc():
    img = numpy.zeros([5, 5, 3])
    img[:, :, 0] = numpy.ones([5, 5])*64/255.0
    img[:, :, 1] = numpy.ones([5, 5])*128/255.0
    img[:, :, 2] = numpy.ones([5, 5])*192/255.0
    cv2.imshow('img', img)
    waitKey = cv2.waitKey(33)
    return waitKey


def main():
    while True:
        key = waitKeyFunc()
        print(key)
        if key == "27":  # esc
            break


if __name__ == '__main__':
    main()
