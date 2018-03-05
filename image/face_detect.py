# -*- coding: utf-8 -*-

import cv2
import animeface
import PIL.Image


def detect(filename, cascade_file="lbpcascade_animeface.xml"):
    cascade = cv2.CascadeClassifier(cascade_file)

    img = cv2.imread(filename)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=1,
                                     minSize=(24, 24))

    if len(faces) > 0:
        return faces

    return None


def detect_f(filename):
    im = PIL.Image.open(filename)
    faces = animeface.detect(im)
    return faces