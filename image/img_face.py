# -*- coding: utf-8 -*-

import cv2
import os.path
import anime


def getface(filename, cascade_file="lbpcascade_animeface.xml"):
    if not os.path.isfile(cascade_file):
        raise RuntimeError("%s: not found" % cascade_file)

    faces = anime.face(filename, cascade_file)

    if len(faces) > 0:
        img = cv2.imread(filename)
        for rect in faces:
            x = rect[0]
            y = rect[1]
            width = rect[2]
            height = rect[3]
            dst = img[y:y + height, x:x + width]
            return dst

    return None


for path, subdirs, files in os.walk('/home/zero/pixiv_image/full/'):
    for name in files:
        print name[:-4]
        filename = os.path.join(path, name)
        dst = getface(filename)
        if dst is not  None:
            cv2.imwrite('/home/zero/detect/' + name[:-4] + "_face.png", dst)
