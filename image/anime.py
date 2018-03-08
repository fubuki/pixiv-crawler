# -*- coding: utf-8 -*-

import cv2


def face(filename, cascade_file="lbpcascade_animeface.xml"):
    cascade = cv2.CascadeClassifier(cascade_file)

    img = cv2.imread(filename)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gray = cv2.equalizeHist(gray)

    faces = cascade.detectMultiScale(gray,
                                     scaleFactor=1.1,
                                     minNeighbors=1,
                                     minSize=(24, 24))
    return face


    return None


def img_sift(filename):
    img = cv2.imread(filename, 0)

    sift = cv2.xfeatures2d.SIFT_create()
    kp, des = sift.detectAndCompute(img, None)

    return kp, des


def compare(img1, img2):

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)

    matches = flann.knnMatch(img1.des, img2.des, k=2)
    matches_mask = [[0, 0] for i in xrange(len(matches))]

    for i, (m, n) in enumerate(matches):
        if m.distance < 0.7 * n.distance:
            matches_mask[i] = [1, 0]

    draw_params = dict(matchColor=(0, 255, 0),
                       singlePointColor=(255, 0, 0),
                       matchesMask=matches_mask,
                       flags=0)

    img3 = cv2.drawMatchesKnn(img1.img, img1.kp, img2.img, img2.kp, matches, None, **draw_params)
    return img3
